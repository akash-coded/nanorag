"""L10 · Cost and cache.

Run:  python scripts/lab.py run L10
"""
from __future__ import annotations

PRICE = {"input_per_1k": 0.003, "output_per_1k": 0.015, "embed_per_1k": 0.00002}


def query_cost(prompt_tokens: int, output_tokens: int, price: dict = PRICE) -> float:
    """Cost of one generation call, in dollars."""
    # TODO
    raise NotImplementedError


def monthly_tco(chunks: int, avg_chunk_tokens: int, queries_per_month: int,
                prompt_tokens: int, output_tokens: int, change_rate: float,
                cluster_monthly: float, price: dict = PRICE) -> dict:
    """Total cost of ownership for one month.

    Line items, all in dollars:
      generation  = queries_per_month * query_cost(prompt, output)
      backfill    = chunks * avg_chunk_tokens / 1000 * embed_per_1k
                    (a one-off, but it lands in month one, so include it)
      reembed     = backfill * change_rate
      cluster     = cluster_monthly  (fixed; does not scale down)

    Return {"generation", "backfill", "reembed", "cluster", "total",
            "generation_share"} where generation_share is generation/total.
    """
    # TODO
    raise NotImplementedError


def pick_threshold(pairs: list[tuple[float, bool]], min_precision: float = 0.99) -> dict:
    """Choose a semantic-cache threshold, precision-first.

    `pairs` is (similarity, is_really_the_same_question) for candidate hits.
    A hit is served when similarity >= theta.

    Sweep theta over the observed similarities (each value, descending). Choose
    the LOWEST theta whose precision on served hits is >= min_precision --
    lowest, because among thresholds that are safe enough you want the most
    hits.

    Return {"theta", "precision", "hit_rate", "false_hits"} where hit_rate is
    served / len(pairs). If NO theta reaches min_precision, return theta 1.1
    (serve nothing) with precision 1.0 and hit_rate 0.0.
    """
    # TODO
    raise NotImplementedError
