from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

ROWS = {"recall_at_n": 0.938, "full_chain_at_n": 0.871, "full_chain": 0.469}


def answered(m):
    expect(repr(m.ANSWER) != "____", "ANSWER is still the ____ blank")
    expect(m.ANSWER in ("retrieval", "packing", "generation"), f"one of three words, got {m.ANSWER!r}")


def correct(m):
    drop_retrieval = ROWS["recall_at_n"] - ROWS["full_chain_at_n"]
    drop_packing = ROWS["full_chain_at_n"] - ROWS["full_chain"]
    biggest = "packing" if drop_packing > drop_retrieval else "retrieval"
    expect(m.ANSWER == biggest,
           f"pool→packed drops {drop_packing:.3f}; retrieval's own drop is {drop_retrieval:.3f}. "
           "The stage between the two rows with the biggest gap is the bottleneck")
    return Measured(f"packing loss {drop_packing:.3f} vs retrieval loss {drop_retrieval:.3f}")


def not_generation(m):
    """Hidden: nothing in the table measures generation, so it cannot be the answer."""
    expect(m.ANSWER != "generation", "no row in the table measures the generator; you cannot pick a stage the data does not observe")


CHECKS = [
    Check("an answer is set", "One of three", answered),
    Check("the stage is right", "Biggest gap between adjacent rows", correct),
    Check("not a stage the table cannot see", "Only pick what is measured", not_generation, public=False),
]
