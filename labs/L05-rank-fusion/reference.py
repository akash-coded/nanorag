"""Reference solution for L05."""
from __future__ import annotations


def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for position, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + position)
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


def _normalise(leg: dict[str, float]) -> dict[str, float]:
    if not leg:
        return {}
    lo, hi = min(leg.values()), max(leg.values())
    if hi == lo:
        return dict.fromkeys(leg, 0.0)
    return {key: (value - lo) / (hi - lo) for key, value in leg.items()}


def weighted_fusion(dense: dict[str, float], lexical: dict[str, float],
                    alpha: float = 0.2) -> list[tuple[str, float]]:
    d, l = _normalise(dense), _normalise(lexical)
    scores = {
        key: alpha * d.get(key, 0.0) + (1 - alpha) * l.get(key, 0.0)
        for key in set(d) | set(l)
    }
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
