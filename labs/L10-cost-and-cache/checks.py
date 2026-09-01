from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

SHAPE = {"chunks": 2_000_000, "avg_chunk_tokens": 180, "queries_per_month": 300_000,
         "prompt_tokens": 4_000, "output_tokens": 350, "change_rate": 0.15,
         "cluster_monthly": 4_200.0}


def per_query_cost(m):
    got = m.query_cost(4000, 350)
    expected = 4.0 * 0.003 + 0.35 * 0.015
    expect(abs(got - expected) < 1e-9, f"expected {expected:.6f}, got {got:.6f}")
    return Measured(f"one query: ${got:.5f} — the number everyone quotes")


def tco_has_all_the_lines(m):
    got = m.monthly_tco(**SHAPE)
    for key in ("generation", "backfill", "reembed", "cluster", "total", "generation_share"):
        expect(key in got, f"missing line item {key!r}; got {sorted(got)}")
    expect(abs(got["total"] - (got["generation"] + got["backfill"] + got["reembed"]
                               + got["cluster"])) < 1e-6,
           "total must be the sum of the line items")


def generation_is_a_minority(m):
    got = m.monthly_tco(**SHAPE)
    expect(got["generation_share"] < 0.6,
           f"generation is {got['generation_share']:.0%} of this bill. If it is most of the "
           "total you have dropped a line item — the cluster and the embedding cycle are the "
           "ones people forget")
    return Measured(f"generation is {got['generation_share']:.0%} of ${got['total']:,.0f}/month")


def change_rate_moves_the_total(m):
    static = m.monthly_tco(**{**SHAPE, "change_rate": 0.0})
    churny = m.monthly_tco(**{**SHAPE, "change_rate": 2.0})
    expect(churny["total"] > static["total"],
           "a corpus that churns 2x a month must cost more than a static one — the re-embed "
           "cycle is the input nobody volunteers")
    return Measured(f"change_rate 0.0 → ${static['total']:,.0f}; 2.0 → ${churny['total']:,.0f}")


def threshold_is_precision_first(m):
    pairs = [(0.99, True), (0.98, True), (0.97, True), (0.96, False),
             (0.95, True), (0.94, False), (0.80, False)]
    got = m.pick_threshold(pairs, min_precision=0.99)
    expect(got["precision"] >= 0.99,
           f"chosen precision {got['precision']:.3f} is below the floor — a false hit is a "
           "confidently wrong answer, not a missed saving")
    expect(got["false_hits"] == 0, f"at 99% precision on 7 pairs, expect 0 false hits, got {got['false_hits']}")
    return Measured(f"theta {got['theta']:.2f} → hit rate {got['hit_rate']:.0%}, "
                    f"{got['false_hits']} false hits")


def picks_the_lowest_safe_theta(m):
    """Hidden: among safe thresholds, take the most hits."""
    pairs = [(0.99, True), (0.98, True), (0.97, True), (0.60, False)]
    got = m.pick_threshold(pairs, min_precision=0.99)
    expect(abs(got["theta"] - 0.97) < 1e-9,
           f"0.97 is the lowest theta that still serves only true hits, so it should be chosen "
           f"for the extra hit rate; got theta {got['theta']}")


def no_safe_threshold_serves_nothing(m):
    """Hidden: sometimes the answer is 'do not cache'."""
    pairs = [(0.99, False), (0.98, False), (0.97, True)]
    got = m.pick_threshold(pairs, min_precision=0.99)
    expect(got["hit_rate"] == 0.0,
           f"when the most similar pairs are false hits, no threshold is safe and the cache "
           f"should serve nothing; got hit_rate {got['hit_rate']}")
    expect(got["theta"] > 1.0, f"theta should be above any similarity; got {got['theta']}")


def zero_queries_does_not_divide_by_zero(m):
    """Hidden: a month with no traffic still has a cluster bill."""
    got = m.monthly_tco(**{**SHAPE, "queries_per_month": 0})
    expect(got["generation"] == 0.0, "no queries means no generation cost")
    expect(got["total"] > 0, "the cluster is fixed — it does not scale down to zero")
    expect(got["generation_share"] == 0.0, f"share should be 0.0, got {got['generation_share']}")
    return Measured(f"zero traffic still costs ${got['total']:,.0f}/month — that is what fixed means")


def empty_pairs(m):
    """Hidden: no cache candidates at all."""
    got = m.pick_threshold([], min_precision=0.99)
    expect(got["hit_rate"] == 0.0, f"no candidates means no hits; got {got}")


CHECKS = [
    Check("per-query generation cost", "The number everyone quotes", per_query_cost),
    Check("TCO carries every line item", "Not just tokens", tco_has_all_the_lines),
    Check("generation is a minority of the bill", "The 31%", generation_is_a_minority),
    Check("change rate moves the total", "The input nobody volunteers", change_rate_moves_the_total),
    Check("cache threshold is precision-first", "Asymmetric costs", threshold_is_precision_first),
    Check("picks the lowest safe threshold", "Most hits among the safe ones", picks_the_lowest_safe_theta, public=False),
    Check("serves nothing when nothing is safe", "'Do not cache' is an answer", no_safe_threshold_serves_nothing, public=False),
    Check("zero traffic still has a fixed bill", "Fixed means fixed", zero_queries_does_not_divide_by_zero, public=False),
    Check("no cache candidates is handled", "Degenerate input", empty_pairs, public=False),
]
