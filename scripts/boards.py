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


def _gh(*args: str) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"gh {' '.join(args[:3])}...: {proc.stderr.strip()[:300]}")
    return proc.stdout


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
        self.fields: dict[str, dict] = {}
        for f in raw:
            self.fields[f["name"]] = {
                "id": f["id"],
                "type": f.get("type", "").replace("ProjectV2", "").replace("Field", ""),
                "options": {o["name"]: o["id"] for o in f.get("options", [])},
            }

    # ── reading ────────────────────────────────────────────────────────────
    def items(self, limit: int = 500) -> list[dict]:
        out = json.loads(_gh("project", "item-list", str(self.number), "--owner", OWNER,
                             "--format", "json", "--limit", str(limit)))
        return out.get("items", [])

    def find(self, title: str, tries: int = 4, wait: float = 1.5) -> dict | None:
        """Projects v2 item-list can lag a create by a second or two. Retrying is
        what makes upsert idempotent under a burst of workflow runs; without it,
        two comments ten seconds apart produce two rows."""
        for attempt in range(tries):
            for it in self.items():
                if it.get("title") == title:
                    return it
            if attempt < tries - 1:
                time.sleep(wait)
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
            args += ["--date", value.isoformat()[:10] if hasattr(value, "isoformat") else str(value)]
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
