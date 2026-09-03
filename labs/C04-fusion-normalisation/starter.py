"""C04 · One expression is wrong.  Fix it.

Run:  python scripts/lab.py run C04
"""
from __future__ import annotations


def _normalise(leg: dict[str, float]) -> dict[str, float]:
    if not leg:
        return {}
    lo, hi = min(leg.values()), max(leg.values())
    if hi == lo:
        return dict.fromkeys(leg, 0.0)
    return {k: (v - lo) / hi for k, v in leg.items()}


def weighted_fusion(dense: dict[str, float], lexical: dict[str, float],
                    alpha: float = 0.5) -> list[tuple[str, float]]:
    d, l = _normalise(dense), _normalise(lexical)
    scores = {k: alpha * d.get(k, 0.0) + (1 - alpha) * l.get(k, 0.0) for k in set(d) | set(l)}
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
