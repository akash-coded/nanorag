"""L05 · Rank fusion.

Run:  python scripts/lab.py run L05
"""
from __future__ import annotations


def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Reciprocal rank fusion.

    `rankings` is a list of ranked id lists, best first. Ranks are 1-based.
    Score each id as sum of 1/(k + rank) over the rankings it appears in;
    an id absent from a ranking contributes nothing from it.

    Return (id, score) sorted by score descending. Break ties by id ascending,
    so the output is deterministic.
    """
    # TODO
    raise NotImplementedError


def weighted_fusion(dense: dict[str, float], lexical: dict[str, float],
                    alpha: float = 0.2) -> list[tuple[str, float]]:
    """Score-based fusion, after min-max normalising each leg to [0, 1].

        score = alpha * dense_norm + (1 - alpha) * lexical_norm

    - Normalise each leg independently: (x - min) / (max - min).
    - If a leg's scores are all equal, normalise every one of them to 0.0
      (there is no signal in a flat leg; do not divide by zero).
    - An id missing from a leg contributes 0.0 from that leg.
    - Return (id, score) sorted by score descending, ties by id ascending.
    """
    # TODO
    raise NotImplementedError
