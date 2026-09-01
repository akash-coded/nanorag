from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

ROWS = [
    # found, then dropped during packing
    {"qid": "q1", "gold": ["a", "b"], "pool": ["a", "b", "z"], "packed": ["a", "z"]},
    {"qid": "q2", "gold": ["c", "d"], "pool": ["c", "d"],      "packed": ["c", "d"]},
    # never retrieved at all
    {"qid": "q3", "gold": ["e", "f"], "pool": ["e"],           "packed": ["e"]},
    {"qid": "q4", "gold": ["g"],      "pool": ["g", "h"],      "packed": ["h"]},
]


def evidence_is_continuous(m):
    expect(m.evidence_recall(["a", "b"], ["a"]) == 0.5,
           f"1 of 2 gold items should be 0.5, got {m.evidence_recall(['a','b'], ['a'])}")
    expect(abs(m.evidence_recall(["a", "b", "c"], ["a", "b"]) - 2/3) < 1e-9,
           "2 of 3 should be 2/3 — evidence recall gives partial credit")


def full_chain_is_binary(m):
    expect(m.full_chain_recall(["a", "b"], ["a"]) == 0.0,
           "missing one gold item makes full-chain recall 0, not 0.5. It is a conjunction")
    expect(m.full_chain_recall(["a", "b"], ["a", "b", "z"]) == 1.0,
           "all gold present should be 1.0, extra chunks are irrelevant")


def the_two_disagree(m):
    """The same row scores differently, and that is the point."""
    gold, packed = ["a", "b", "c"], ["a", "b"]
    er = m.evidence_recall(gold, packed)
    fcr = m.full_chain_recall(gold, packed)
    expect(er > 0 and fcr == 0.0,
           f"evidence recall {er} should be positive while full-chain is 0 — one gives partial "
           "credit and the other does not")
    return Measured(f"same row: evidence {er:.2f}, full-chain {fcr:.2f} — different questions")


def diagnostic_finds_packing_loss(m):
    got = m.found_then_dropped(ROWS)
    expect(got == ["q1", "q4"],
           f"expected ['q1', 'q4'] and got {got}. Both had every gold item in the pool and lost "
           "some during packing. q2 packed everything; q3 was never retrieved at all — that is a "
           "retrieval miss, a different bucket with a different fix")
    return Measured("2 of 4 rows are packing loss, 1 is a retrieval miss — different owners")


def pool_and_packed_are_different_stages(m):
    """Hidden: at_n must read the pool, not the packed set."""
    row = {"gold": ["a", "b"], "pool": ["a", "b"], "packed": ["a"]}
    at_n = m.full_chain_recall_at_n(row["gold"], row["pool"])
    packed = m.full_chain_recall(row["gold"], row["packed"])
    expect(at_n == 1.0, f"the pool contains both gold items, so at_n should be 1.0, got {at_n}")
    expect(packed == 0.0, f"packing kept one, so full_chain should be 0.0, got {packed}")


def empty_gold_does_not_divide_by_zero(m):
    """Hidden: null questions have no gold."""
    for fn in (m.evidence_recall, m.full_chain_recall, m.full_chain_recall_at_n):
        got = fn([], ["a"])
        expect(got == 0.0, f"{fn.__name__}([], ['a']) should be 0.0, got {got}")


def duplicates_do_not_inflate(m):
    """Hidden: a chunk listed twice must not count twice."""
    got = m.evidence_recall(["a", "b"], ["a", "a", "a"])
    expect(got == 0.5,
           f"a duplicated chunk must not count twice; expected 0.5, got {got}")


def order_does_not_matter(m):
    """Hidden: recall is a set operation."""
    expect(m.full_chain_recall(["a", "b"], ["b", "a"]) == 1.0,
           "recall must not depend on the order gold or packed are listed in")


def diagnostic_handles_all_buckets(m):
    """Hidden: q4's pool has the gold and packing lost it — it counts too."""
    rows = [
        {"qid": "x", "gold": ["g"], "pool": ["g", "h"], "packed": ["h"]},
        {"qid": "y", "gold": ["g"], "pool": ["h"],      "packed": ["h"]},
    ]
    got = m.found_then_dropped(rows)
    expect(got == ["x"],
           f"only 'x' is found-then-dropped ('y' was never retrieved); got {got}")


CHECKS = [
    Check("evidence recall gives partial credit", "Continuous", evidence_is_continuous),
    Check("full-chain recall is a conjunction", "Binary, no partial credit", full_chain_is_binary),
    Check("the two metrics disagree on the same row", "Different questions", the_two_disagree),
    Check("the diagnostic isolates packing loss", "84 vs 27 on the real corpus", diagnostic_finds_packing_loss),
    Check("at_n reads the pool, not the packed set", "Different denominators", pool_and_packed_are_different_stages, public=False),
    Check("no gold does not divide by zero", "Null questions", empty_gold_does_not_divide_by_zero, public=False),
    Check("duplicates do not inflate recall", "Set semantics", duplicates_do_not_inflate, public=False),
    Check("order does not matter", "Set semantics", order_does_not_matter, public=False),
    Check("the diagnostic separates all four buckets", "Not just the obvious one", diagnostic_handles_all_buckets, public=False),
]
