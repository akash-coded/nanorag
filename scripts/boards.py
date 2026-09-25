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

import atexit
import datetime as dt
import json
import os
import subprocess
import sys
import time

OWNER = "akash-coded"

# Board numbers are the one thing that is stable, and they are the public URL.
TRACKER, PULSE, LIFECYCLE = 11, 12, 13


# The GraphQL quota is 5,000 points an hour, shared by every session on the
# account, and Projects item-list is priced by nodes returned -- a few big lists
# plus a polling loop can spend it in minutes. `gh api rate_limit` does NOT show
# this; the headers on a real GraphQL response do. On refusal: if the reset is
# close, wait for it once; if it is far, stop and say when, rather than sleeping
# through the hour in 90-second pieces.
_WAIT_UP_TO_MIN = 3
_PACE = 0.4                      # seconds between writes


_baseline: tuple[int, int] | None = None


def _note_baseline() -> None:
    """Read the budget once, before the first real call, and report the spend at
    exit. Two header reads, so a batch can be accounted step by step instead of
    discovered spent. Set BOARDS_SPEND=0 to silence it."""
    global _baseline
    if _baseline is not None or os.environ.get("BOARDS_SPEND", "1") == "0":
        return
    try:
        _baseline = graphql_budget()
    except Exception:  # noqa: BLE001  -- no gh, no token: never the script's problem
        _baseline = (-1, -1)
        return
    atexit.register(_report_spend)


def _report_spend() -> None:
    try:
        remaining, mins = graphql_budget()
    except Exception:  # noqa: BLE001
        return
    spent = (_baseline or (remaining, 0))[0] - remaining
    print(f"boards: spent {spent} GraphQL points; {remaining} remain, reset in ~{mins} min",
          file=sys.stderr)


def _gh(*args: str) -> str:
    _note_baseline()
    for attempt in (1, 2):
        proc = subprocess.run(["gh", *args], capture_output=True, text=True)
        if proc.returncode == 0 and "RATE_LIMIT" not in proc.stdout[:400]:
            if args[:2] in (("project", "item-edit"), ("project", "item-create"),
                            ("project", "item-archive"), ("project", "item-delete")):
                time.sleep(_PACE)
            return proc.stdout
        text = (proc.stdout + proc.stderr).strip()
        if "rate limit" not in text.lower():
            raise RuntimeError(f"gh {' '.join(args[:3])}...: {text[:300]}")
        remaining, mins = graphql_budget()
        if attempt == 1 and mins <= _WAIT_UP_TO_MIN:
            print(f"    GraphQL quota spent; reset in ~{mins} min, waiting", file=sys.stderr)
            time.sleep(mins * 60 + 15)
            continue
        raise RateLimited(f"GraphQL quota spent (remaining={remaining}); resets in ~{mins} min. "
                          "Stop and rerun after the reset.")
    raise RateLimited("GraphQL quota still spent after waiting for the reset")


class RateLimited(RuntimeError):
    """GraphQL points are exhausted. Projects queries are priced by nodes returned,
    so one item-list over a large board can cost hundreds of the hourly 5,000 --
    this is why bulk scripts check the budget first and why item-list is capped."""


def graphql_budget() -> tuple[int, int]:
    """(remaining points, minutes until reset), read from the HEADERS of one real
    GraphQL call.

    `gh api rate_limit` reports graphql 5000/5000 while the actual quota is fully
    spent -- it is a different accounting, and it misled every guard built on it
    here. The X-Ratelimit-* headers on a GraphQL response are the only gauge that
    agrees with what the API is about to do. One point per read."""
    proc = subprocess.run(["gh", "api", "graphql", "-i", "-f", "query={viewer{login}}"],
                          capture_output=True, text=True)
    remaining, reset = -1, 0
    for line in (proc.stdout + proc.stderr).splitlines():
        low = line.lower()
        if low.startswith("x-ratelimit-remaining:"):
            remaining = int(line.split(":", 1)[1].strip() or -1)
        elif low.startswith("x-ratelimit-reset:"):
            reset = int(line.split(":", 1)[1].strip() or 0)
    mins = max(0, int((reset - time.time()) // 60)) if reset else 0
    return remaining, mins


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


_SCHEMA_QUERY = """
query($o:String!,$n:Int!){
  user(login:$o){ projectV2(number:$n){ id title
    fields(first:40){ nodes{
      ... on ProjectV2FieldCommon{ id name dataType }
      ... on ProjectV2SingleSelectField{ options{ id name } } } } } } }
"""

# GraphQL dataType -> the kind names the edit path has always used.
_KIND = {"TEXT": "Text", "NUMBER": "Number", "DATE": "Date",
         "SINGLE_SELECT": "SingleSelect", "ITERATION": "Iteration"}

_ROWS_QUERY = """
query($id:ID!,$n:Int!,$f:Int!,$after:String){
  node(id:$id){ ... on ProjectV2{ items(first:$n, after:$after){
    pageInfo{ hasNextPage endCursor }
    nodes{ id
      content{ __typename
        ... on DraftIssue{ id title body }
        ... on Issue{ id title number url }
        ... on PullRequest{ id title number url } }
      fieldValues(first:$f){ nodes{ __typename
        ... on ProjectV2ItemFieldTextValue{ text
          field{ ... on ProjectV2FieldCommon{ name } } }
        ... on ProjectV2ItemFieldNumberValue{ number
          field{ ... on ProjectV2FieldCommon{ name } } }
        ... on ProjectV2ItemFieldDateValue{ date
          field{ ... on ProjectV2FieldCommon{ name } } }
        ... on ProjectV2ItemFieldSingleSelectValue{ name
          field{ ... on ProjectV2FieldCommon{ name } } }
      } } } } } } }
"""


def flatten_item(item: dict) -> dict:
    """One GraphQL project item -> the row gh's item-list would print for it: `id`,
    `content`, `title`, and each field under its lowercased name. Numbers that are
    whole come back as ints, as gh prints them; unset fields are simply absent."""
    row: dict = {"id": item["id"], "content": item.get("content") or {}}
    for fv in item.get("fieldValues", {}).get("nodes", []):
        name = (fv.get("field") or {}).get("name")
        if not name:
            continue                                   # a type this query does not read
        value = next((fv[k] for k in ("text", "date", "number", "name") if k in fv), None)
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        row[name.lower()] = value
    row.setdefault("title", row["content"].get("title"))
    return row


class Board:
    """One project, with its fields and options resolved by name."""

    def __init__(self, number: int):
        """One query for id, title, fields and options: about 2 points. The
        `gh project view` + `field-list` pair it replaces cost about 104, more than
        the listing itself, on every construction -- so every tracker write from CI
        paid it."""
        self.number = number
        proj = json.loads(_gh("api", "graphql", "-f", f"query={_SCHEMA_QUERY}",
                              "-f", f"o={OWNER}", "-F", f"n={number}"))
        proj = proj["data"]["user"]["projectV2"]
        self.id = proj["id"]
        self.title = proj["title"]
        self._known: dict[str, str] = {}   # title -> item id, this process only
        self._rows: dict[str, dict] | None = None   # title -> row, listed once
        self.fields: dict[str, dict] = {}
        for f in proj["fields"]["nodes"]:
            if not f.get("name"):
                continue
            self.fields[f["name"]] = {
                "id": f["id"],
                "type": _KIND.get(f.get("dataType", ""), ""),
                "options": {o["name"]: o["id"] for o in f.get("options", [])},
            }

    # ── reading ────────────────────────────────────────────────────────────
    def items(self, limit: int = 100) -> list[dict]:
        """Rows in the shape `gh project item-list --format json` gives -- id, title,
        content, one lowercased key per field -- at a fraction of its price.

        gh asks for fieldValues(first:100) on every item, so a page of 100 costs about
        100 GraphQL points whatever the board holds (measured 102 on a 31-row board),
        and every write that first finds its row cost about 105. This asks for exactly
        the board's own fields: about 1 + fields points a page, 14 on the tracker."""
        rows: list[dict] = []
        after = None
        want = len(self.fields) + 2          # every field, with headroom for built-ins
        while len(rows) < limit:
            n = min(100, limit - len(rows))
            args = ["api", "graphql", "-f", f"query={_ROWS_QUERY}", "-f", f"id={self.id}",
                    "-F", f"n={n}", "-F", f"f={want}"]
            if after:
                args += ["-f", f"after={after}"]
            page = json.loads(_gh(*args))["data"]["node"]["items"]
            rows += [flatten_item(it) for it in page["nodes"]]
            if not page["pageInfo"]["hasNextPage"]:
                break
            after = page["pageInfo"]["endCursor"]
        return rows

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
