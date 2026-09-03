from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

WANT = {"generation_tokens": "recurring", "initial_backfill": "one-off",
        "reembed_on_drift": "recurring", "vector_cluster": "recurring",
        "reranker_inference": "recurring", "encoder_upgrade": "one-off"}


def no_blanks(m):
    got = m.classify()
    left = [k for k, v in got.items() if repr(v) == "____"]
    expect(not left, f"still blank: {', '.join(left)}")
    expect(all(v in ("recurring", "one-off") for v in got.values()), f"each must be 'recurring' or 'one-off': {got}")


def the_obvious_ones(m):
    got = m.classify()
    expect(got["generation_tokens"] == "recurring", "tokens are paid on every query")
    expect(got["initial_backfill"] == "one-off", "the first backfill happens once")


def the_trap(m):
    got = m.classify()
    expect(got["reembed_on_drift"] == "recurring",
           "re-embedding on drift feels like a rebuild and is a monthly bill — the corpus keeps changing")
    return Measured("re-embed on drift: recurring (it is 14% of a real bill and nobody budgets it)")


def the_cluster(m):
    """Hidden."""
    expect(m.classify()["vector_cluster"] == "recurring", "the cluster is fixed AND monthly — it does not scale down to zero")


def four_and_two(m):
    """Hidden."""
    got = m.classify()
    rec = sum(1 for v in got.values() if v == "recurring")
    expect(rec == 4, f"expected 4 recurring and 2 one-off, got {rec} recurring")
    expect(got == WANT, "one classification is still wrong")


CHECKS = [
    Check("no blanks, valid words", "Fill all six", no_blanks),
    Check("tokens recur, first backfill does not", "The obvious two", the_obvious_ones),
    Check("re-embed on drift is recurring", "The trap", the_trap),
    Check("the cluster recurs", "Fixed is not one-off", the_cluster, public=False),
    Check("four recurring, two one-off", "All six", four_and_two, public=False),
]
