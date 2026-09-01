from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

BM25 = ["chunk-A", "chunk-B", "chunk-C", "chunk-D", "chunk-E"]
DENSE = ["chunk-C", "chunk-A", "chunk-F", "chunk-B", "chunk-G"]


def rrf_scores_correctly(m):
    got = dict(m.rrf([BM25, DENSE], k=60))
    expect(abs(got["chunk-A"] - (1/61 + 1/62)) < 1e-9,
           f"chunk-A is rank 1 and rank 2, so 1/61 + 1/62; got {got['chunk-A']}")
    expect(abs(got["chunk-E"] - 1/65) < 1e-9,
           f"chunk-E appears in one ranking at rank 5, so 1/65; got {got['chunk-E']}")
    return Measured(f"chunk-A {got['chunk-A']:.5f} vs chunk-C {got['chunk-C']:.5f}")


def agreement_beats_confidence(m):
    """A doc ranked well by both should beat one ranked 1st by only one."""
    ranked = [d for d, _ in m.rrf([["solo"] + BM25, DENSE], k=60)]
    expect(ranked.index("chunk-A") < ranked.index("solo"),
           f"chunk-A (ranks 2 and 2) should beat 'solo' (rank 1, once). Got {ranked[:4]}. "
           "If 'solo' wins, k is too small and one retriever's confidence dominates")
    return Measured("agreement across legs beat a single top-1 — the whole point of a large k")


def k_damps(m):
    """Small k lets one confident retriever win; large k does not.

    'solo' is rank 1 in one leg only.  'both' is rank 2 and rank 3.
      k=0   solo = 1/1 = 1.000   both = 1/2 + 1/3 = 0.833   -> solo leads
      k=60  solo = 1/61 = 0.016  both = 1/62 + 1/63 = 0.032 -> both leads
    """
    legs = [["solo", "both"], ["p", "q", "both"]]
    small = [d for d, _ in m.rrf(legs, k=0)]
    large = [d for d, _ in m.rrf(legs, k=60)]
    expect(small.index("solo") < small.index("both"),
           f"at k=0 rank 1 outweighs two lower ranks, so 'solo' should beat 'both'; got {small}")
    expect(large.index("both") < large.index("solo"),
           f"at k=60 appearing in both legs should beat one rank-1; got {large}")
    return Measured("k=0 → solo beats both; k=60 → both beats solo. k decides confidence vs agreement")


def weighted_respects_alpha(m):
    dense = {"x": 1.0, "y": 0.0}
    lexical = {"x": 0.0, "y": 1.0}
    low = dict(m.weighted_fusion(dense, lexical, alpha=0.2))
    high = dict(m.weighted_fusion(dense, lexical, alpha=0.8))
    expect(low["y"] > low["x"], f"at alpha=0.2 the lexical leg should dominate; got {low}")
    expect(high["x"] > high["y"], f"at alpha=0.8 the dense leg should dominate; got {high}")


def deterministic_ties(m):
    """Hidden: identical scores must order deterministically."""
    got = [d for d, _ in m.rrf([["b", "a"], ["a", "b"]], k=60)]
    expect(got == ["a", "b"],
           f"tied scores must break by id ascending for a reproducible run; got {got}")


def flat_leg_does_not_divide_by_zero(m):
    """Hidden: a leg with no spread."""
    got = m.weighted_fusion({"x": 0.5, "y": 0.5}, {"x": 1.0, "y": 0.0}, alpha=0.5)
    scores = dict(got)
    expect(all(isinstance(v, float) and v == v for v in scores.values()),
           f"a flat dense leg produced NaN or non-float: {scores}")
    expect(scores["x"] > scores["y"],
           f"with dense flat, lexical should decide; got {scores}")


def missing_ids_contribute_nothing(m):
    """Hidden: legs need not agree on the candidate set."""
    got = dict(m.weighted_fusion({"only-dense": 1.0}, {"only-lex": 1.0}, alpha=0.5))
    expect(set(got) == {"only-dense", "only-lex"},
           f"the union of both legs should appear; got {sorted(got)}")


def empty_input(m):
    """Hidden: no candidates is a valid state, not a crash."""
    expect(m.rrf([]) == [], "rrf([]) should be []")
    expect(m.rrf([[], []]) == [], "rrf of empty rankings should be []")
    expect(m.weighted_fusion({}, {}) == [], "weighted_fusion({}, {}) should be []")


def output_is_the_union(m):
    """Hidden: every candidate from every leg must appear exactly once."""
    got = m.rrf([BM25, DENSE], k=60)
    ids = [d for d, _ in got]
    expect(len(ids) == len(set(ids)), f"an id appears twice in the output: {ids}")
    expect(set(ids) == set(BM25) | set(DENSE),
           f"output should be the union of both legs; missing {set(BM25) | set(DENSE) - set(ids)}")
    expect(all(a >= b for a, b in zip([s for _, s in got], [s for _, s in got][1:])),
           "output is not sorted by score descending")
    return Measured(f"{len(ids)} unique candidates from two legs of 5")


CHECKS = [
    Check("rrf sums 1/(k+rank) across legs", "The formula", rrf_scores_correctly),
    Check("agreement beats a single confident hit", "Why k is large", agreement_beats_confidence),
    Check("k damps rank-1 dominance", "k=0 vs k=60", k_damps),
    Check("weighted fusion respects alpha", "The other option", weighted_respects_alpha),
    Check("tied scores order deterministically", "Reproducible runs", deterministic_ties, public=False),
    Check("a flat leg does not divide by zero", "Degenerate normalisation", flat_leg_does_not_divide_by_zero, public=False),
    Check("legs need not share a candidate set", "Union, not intersection", missing_ids_contribute_nothing, public=False),
    Check("empty input returns empty", "Not a crash", empty_input, public=False),
    Check("output is the deduplicated union, sorted", "No lost or doubled candidates", output_is_the_union, public=False),
]
