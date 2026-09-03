from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

import math

from labs._harness import Check, Measured, expect  # noqa: E402


def answered(m):
    expect(hasattr(m, "ANSWER"), "set ANSWER in starter.py")
    expect(repr(m.ANSWER) != "____", "ANSWER is still the ____ blank")
    expect(m.ANSWER in ("positive", "negative", "zero"),
           f"ANSWER should be one of three words, got {m.ANSWER!r}")


def correct(m):
    actual = math.log((1000 - 620 + 0.5) / (620 + 0.5))
    want = "negative" if actual < 0 else "positive" if actual > 0 else "zero"
    expect(m.ANSWER == want,
           f"IDF here is {actual:+.3f}. A term in 620 of 1,000 documents has fewer documents "
           "WITHOUT it than with it, so the ratio is below 1 and its log is below 0")
    return Measured(f"IDF(service) = {actual:+.3f}")


def understands_the_pivot(m):
    """Hidden: the same reasoning at df=400 flips."""
    actual = math.log((1000 - 400 + 0.5) / (400 + 0.5))
    expect(actual > 0, "sanity: at df=400 IDF is positive")
    expect(m.ANSWER == "negative", "the answer is about df=620, above the N/2 pivot")


CHECKS = [
    Check("an answer is set", "One of three words", answered),
    Check("the sign is right", "Read the fraction", correct),
    Check("the pivot is at N/2", "Why 620 and not 400", understands_the_pivot, public=False),
]
