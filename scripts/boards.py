#!/usr/bin/env python3
"""Read and write GitHub Projects (v2) boards by NAME, not by id.

Field ids and option ids are looked up on every call. That costs one extra API
round trip and buys the only thing that matters for code that runs unattended
for months: nothing here goes stale when someone renames an option or rebuilds
a board. Every script that touches a board -- tracker, pulse, assign, lifecycle
-- goes through this module.

Writes to a user-owned project need a classic PAT with the `project` scope;
the workflow-issued GITHUB_TOKEN cannot do it. Set GH_TOKEN (the workflows pass
secrets.PROJECT_TOKEN) or rely on `gh auth login`, which is what runs locally.
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import time

OWNER = "akash-coded"

# Board numbers are the one thing that is stable, and they are the public URL.
TRACKER, PULSE, LIFECYCLE = 11, 12, 13


# GitHub applies a SECONDARY rate limit to Projects mutations and to bursts of
# GraphQL that `gh api rate_limit` never shows: the primary gauge can read 5000/5000
# while calls are being refused. The budget is also shared by every session on the
# account. So every call backs off on refusal, and every write is paced.
_BACKOFF = (20, 45, 90)          # seconds, on successive refusals
_PACE = 0.4                      # seconds between writes


def _gh(*args: str) -> str:
    for attempt, wait in enumerate((*_BACKOFF, None)):
        proc = subprocess.run(["gh", *args], capture_output=True, text=True)
        if proc.returncode == 0:
            if args[:2] in (("project", "item-edit"), ("project", "item-create"),
                            ("project", "item-archive"), ("project", "item-delete")):
                time.sleep(_PACE)
            return proc.stdout
        err = proc.stderr.strip()
        if "rate limit" in err.lower() and wait is not None:
            print(f"    rate limited; backing off {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        if "rate limit" in err.lower():
            raise RateLimited(err[:200])
        raise RuntimeError(f"gh {' '.join(args[:3])}...: {err[:300]}")
    raise RateLimited("gave up after backoff")


class RateLimited(RuntimeError):
    """GraphQL points are exhausted. Projects queries are priced by nodes returned,
    so one item-list over a large board can cost hundreds of the hourly 5,000 --
    this is why bulk scripts check the budget first and why item-list is capped."""


def graphql_budget() -> tuple[int, int]:
    """(remaining points, minutes until reset). REST, so it never costs GraphQL points."""
    out = json.loads(_gh("api", "rate_limit"))["resources"]["graphql"]
    import time as _t
    return out["remaining"], max(0, int((out["reset"] - _t.time()) // 60))


def require_budget(points: int, what: str = "this run") -> None:
    """Abort BEFORE a bulk operation if it would exhaust the hour's GraphQL points.
    Failing halfway through leaves a board half-updated and a budget spent."""
    remaining, mins = graphql_budget()
    if remaining < points:
        raise SystemExit(f"{what} needs ~{points} GraphQL points; {remaining} remain, "
                         f"reset in {mins} min. Wait, or run with fewer rows.")
    # The primary gauge is necessary, not sufficient: a secondary limit on bursts
    # is invisible here and is handled by backoff in _gh(). This check only stops
    # the obviously-doomed run.


class Board:
    """One project, with its fields and options resolved by name."""

    def __init__(self, number: int):
        self.number = number
        view = json.loads(_gh("project", "view", str(number), "--owner", OWNER, "--format", "json"))
        self.id = view["id"]
        self.title = view["title"]
        raw = json.loads(_gh("project", "field-list", str(number), "--owner", OWNER,
                             "--format", "json", "--limit", "100"))["fields"]
        self._known: dict[str, str] = {}   # title -> item id, this process only
        self._rows: dict[str, dict] | None = None   # title -> row, listed once
        self.fields: dict[str, dict] = {}
        for f in raw:
            self.fields[f["name"]] = {
                "id": f["id"],
                "type": f.get("type", "").replace("ProjectV2", "").replace("Field", ""),
                "options": {o["name"]: o["id"] for o in f.get("options", [])},
            }

    # ── reading ────────────────────────────────────────────────────────────
    def items(self, limit: int = 100) -> list[dict]:
        out = json.loads(_gh("project", "item-list", str(self.number), "--owner", OWNER,
                             "--format", "json", "--limit", str(limit)))
        return out.get("items", [])

    def _index(self, refresh: bool = False) -> dict[str, dict]:
        """title -> row, fetched once per instance. Every find() used to re-list the
        whole board up to four times; assign.py called find() twice per row. A
        class of twenty on three items burned the GraphQL budget in seconds. Now a
        board is listed once, and again only on a miss."""
        if self._rows is None or refresh:
            self._rows = {it.get("title"): it for it in self.items()}
        return self._rows

    def find(self, title: str, tries: int = 1, wait: float = 1.5) -> dict | None:
        """A hit costs no API call. A miss lists once by default; pass tries=2 or 3
        where a duplicate row would matter (tracker.py, one row per learner x item)
        to re-list after a short wait, because item-list can lag a create by a
        second or two across processes. Bulk seeders leave it at 1 -- a re-list on
        every miss is what exhausted the budget."""
        row = self._index().get(title)
        if row:
            return row
        for attempt in range(1, tries):
            time.sleep(wait)
            row = self._index(refresh=True).get(title)
            if row:
                return row
        return None

    # ── writing ────────────────────────────────────────────────────────────
    def _set(self, item_id: str, field: str, value) -> None:
        meta = self.fields.get(field)
        if meta is None:
            raise KeyError(f"board #{self.number} has no field {field!r}; "
                           f"has {sorted(self.fields)}")
        args = ["project", "item-edit", "--id", item_id, "--project-id", self.id,
                "--field-id", meta["id"]]
        kind = meta["type"]
        if kind == "SingleSelect":
            opt = meta["options"].get(str(value))
            if opt is None:
                raise KeyError(f"{field!r} has no option {value!r}; "
                               f"has {sorted(meta['options'])}")
            args += ["--single-select-option-id", opt]
        elif kind == "Date" or isinstance(value, (dt.date, dt.datetime)):
            iso = value.isoformat()[:10] if hasattr(value, "isoformat") else str(value)
            args += ["--date", iso]
        elif kind == "Number" or isinstance(value, (int, float)):
            args += ["--number", str(value)]
        else:
            args += ["--text", str(value)]
        _gh(*args)

    def upsert(self, title: str, **fields) -> tuple[str, bool]:
        """Create a draft item titled `title` if absent, then set every field.

        Returns (item_id, created). Idempotent: run it twice, get one row.
        """
        # A fast path for the common case: one process upserting the same title
        # repeatedly (a pulse run touching a thread twice) never re-lists.
        item_id = self._known.get(title)
        created = False
        if item_id is None:
            existing = self.find(title)
            if existing:
                item_id = existing["id"]
            else:
                made = json.loads(_gh("project", "item-create", str(self.number), "--owner",
                                      OWNER, "--title", title, "--format", "json"))
                item_id, created = made["id"], True
                if self._rows is not None:
                    self._rows[title] = {"id": item_id, "title": title}
            self._known[title] = item_id
        for name, value in fields.items():
            if value is None:
                continue
            self._set(item_id, name, value)
        return item_id, created

    def archive(self, item_id: str) -> None:
        _gh("project", "item-archive", str(self.number), "--owner", OWNER, "--id", item_id)

    def delete(self, item_id: str) -> None:
        _gh("project", "item-delete", str(self.number), "--owner", OWNER, "--id", item_id)


def field_value(item: dict, name: str):
    """Read a field off an item-list row. gh flattens fields into the row, keyed
    by a lowercased, space-stripped version of the field name."""
    key = name.lower().replace(" ", "")
    for k, v in item.items():
        if k.lower().replace(" ", "") == key:
            return v
    return None


if __name__ == "__main__":
    # `python scripts/boards.py 11` prints a board's resolved schema -- the
    # quickest way to confirm the fields exist before a workflow depends on them.
    n = int(sys.argv[1]) if len(sys.argv) > 1 else TRACKER
    b = Board(n)
    print(f"#{b.number} {b.title}")
    for name, meta in b.fields.items():
        opts = f"  {sorted(meta['options'])}" if meta["options"] else ""
        print(f"  {name:<20} {meta['type']:<12}{opts}")
