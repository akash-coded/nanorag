#!/usr/bin/env python3
"""Assign labs or challenges to learners for a session.

Creates one Tracker row per (learner, item) with Outcome=Assigned, the session
name, who assigned it, and the due date. When the learner attempts it, the
lab-submission workflow moves the same row forward, so "assigned but never
tried" is visible on the board as a row that is still Assigned after the due
date -- which is the thing an instructor actually needs to see.

    python scripts/assign.py --session 2026-09-08 --items C01,C03,L01 \\
        --to alice,bob --due 2026-09-10 --by akash-coded

Add --announce to also post a thread in Announcements listing who has what.
Posting is opt-in: the board is the record, the thread is the reminder.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import boards  # noqa: E402
from tracker import LEVEL, track_option  # noqa: E402

from labs import _registry  # noqa: E402

R = "https://github.com/akash-coded/nanorag"
TRACKER_URL = f"https://github.com/users/akash-coded/projects/{boards.TRACKER}"


def assign(session: str, items: list[str], learners: list[str], due: dt.date,
           by: str) -> list[str]:
    labs = _registry.load()
    unknown = [i for i in items if i.upper() not in labs]
    if unknown:
        raise SystemExit(f"unknown items: {unknown}")
    board = boards.Board(boards.TRACKER)
    made = []
    for learner in learners:
        for item_id in items:
            item = labs[item_id.upper()]
            title = f"{learner} · {item.id}"
            existing = board.find(title, tries=1)
            outcome = boards.field_value(existing, "Outcome") if existing else None
            fields = {"Learner": learner, "Item": item.id,
                      "Track": track_option(board, item.track), "Level": LEVEL[item.difficulty],
                      "Session": session, "Assigned by": by, "Due": due,
                      "Thread": f"{R}/blob/main/labs/{item.dirname}/brief.md"}
            if not outcome:                       # do not reset a row already in progress
                fields["Outcome"] = "Assigned"
            board.upsert(title, **fields)
            made.append(title)
            print(f"  {title:<28} {outcome or 'Assigned':<20} due {due}")
    return made


def announce(session: str, items: list[str], learners: list[str], due: dt.date, by: str) -> str:
    labs = _registry.load()
    def row(i: str) -> str:
        it = labs[i.upper()]
        return (f"| {it.badge} [`{it.id}`]({R}/blob/main/labs/{it.dirname}/brief.md)"
                f" | {it.title} | {it.minutes} min |")
    rows = "\n".join(row(i) for i in items)
    who = " ".join(f"@{u}" for u in learners)
    body = f"""> **Hands-on for session {session}.** Due **{due}**. Assigned by @{by}.

{who}

| | Item | | Time |
|---|---|---|---:|
{rows}

## How to do them

Open a Codespace, or a clone, and:

```bash
python scripts/lab.py next        # your queue, in order
python scripts/lab.py open C01    # brief beside the starter
python scripts/lab.py run C01 --hidden
```

Submit in the item's **arena** or **submit** thread — a sandbox grades it and replies. Every
attempt is counted, not only the first; **retrying is the exercise**.

## Where this is tracked

[The Hands-on Tracker]({TRACKER_URL}) —
one row per person per item. Yours moves from *Assigned* to *Attempted* to *Passed* as you go.
Still *Assigned* after the due date means you have not tried it yet, which is fine to be honest
about in the session.
"""
    spec = {"category": "announcements", "labels": ["cohort", "office-hours"],
            "title": f"[session · {session}] Hands-on: {', '.join(i.upper() for i in items)}",
            "body": body}
    path = ROOT / "threads" / "sessions" / f"{session}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "create_thread.py"), str(path)],
                   check=True)
    return str(path)


def main() -> int:
    boards.require_budget(300, 'an assignment run')
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True, help="a label, usually the date")
    ap.add_argument("--items", required=True, help="comma-separated, e.g. C01,C03,L01")
    ap.add_argument("--to", required=True, help="comma-separated GitHub logins")
    ap.add_argument("--due", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--by", default="akash-coded")
    ap.add_argument("--announce", action="store_true", help="also post the session thread")
    a = ap.parse_args()
    items = [i.strip() for i in a.items.split(",") if i.strip()]
    learners = [u.strip().lstrip("@") for u in a.to.split(",") if u.strip()]
    assign(a.session, items, learners, a.due, a.by)
    if a.announce:
        announce(a.session, items, learners, a.due, a.by)
    return 0


if __name__ == "__main__":
    sys.exit(main())
