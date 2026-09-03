#!/usr/bin/env python3
"""Record one attempt at a lab or challenge on the Hands-on Tracker board.

One row per (learner, item), titled "<learner> · <item>" to match the sibling
board. Outcome moves forward and never backward:

    Assigned  ->  Attempted  ->  Retrying  ->  Passed | Passed after retry

A learner who re-posts after passing bumps Attempts and keeps Passed; the
board answers "how many tries did it take" and "who is stuck", and a pass must
not turn back into Retrying because somebody was curious.

Called by the workflows with GH_TOKEN=secrets.PROJECT_TOKEN, because a
workflow-issued token cannot write to a user-owned project.

    python scripts/tracker.py --learner alice --item C03 --passed --thread URL
    python scripts/tracker.py --learner alice --item L01 --thread URL          # a failed attempt
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import boards  # noqa: E402

from labs import _registry  # noqa: E402

LEVEL = {"easy": "foundational", "medium": "intermediate", "hard": "advanced", "boss": "advanced"}


def track_option(board: boards.Board, code: str) -> str | None:
    """Board options read 'T1 corpus'; the registry says 'T1'. Match on prefix."""
    for name in board.fields["Track"]["options"]:
        if name.split()[0] == code:
            return name
    return None


def record(learner: str, item_id: str, passed: bool, thread: str = "",
           source: str = "discussion") -> dict:
    labs = _registry.load()
    item = labs.get(item_id.upper())
    if item is None:
        raise SystemExit(f"unknown item {item_id!r}")

    board = boards.Board(boards.TRACKER)
    title = f"{learner} · {item.id}"
    row = board.find(title, tries=2)   # a duplicate learner x item row would matter
    attempts_before = int(boards.field_value(row, "Attempts") or 0) if row else 0
    outcome_before = (boards.field_value(row, "Outcome") or "") if row else ""
    today = dt.date.today()

    if outcome_before.startswith("Passed"):
        outcome = outcome_before                      # never downgrade a pass
    elif passed:
        outcome = "Passed" if attempts_before == 0 else "Passed after retry"
    else:
        outcome = "Attempted" if attempts_before == 0 else "Retrying"

    fields = {
        "Learner": learner, "Item": item.id,
        "Track": track_option(board, item.track), "Level": LEVEL[item.difficulty],
        "Outcome": outcome, "Attempts": attempts_before + 1, "Thread": thread or None,
    }
    if not row or not boards.field_value(row, "First attempt"):
        fields["First attempt"] = today
    if passed and not outcome_before.startswith("Passed"):
        fields["Passed on"] = today

    item_pk, created = board.upsert(title, **fields)
    result = {"title": title, "created": created, "outcome": outcome,
              "attempts": attempts_before + 1, "source": source}
    print(" ".join(f"{k}={v}" for k, v in result.items()))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--learner", required=True)
    ap.add_argument("--item", required=True)
    ap.add_argument("--passed", action="store_true")
    ap.add_argument("--thread", default="")
    ap.add_argument("--source", default="discussion", choices=["discussion", "pr"])
    a = ap.parse_args()
    record(a.learner, a.item, a.passed, a.thread, a.source)
    return 0


if __name__ == "__main__":
    sys.exit(main())
