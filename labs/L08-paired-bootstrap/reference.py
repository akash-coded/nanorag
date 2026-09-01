"""Reference solution for L08."""
from __future__ import annotations

import random


def paired_bootstrap(before: dict[str, float], after: dict[str, float],
                     n_boot: int = 2000, seed: int = 11) -> dict:
    common = sorted(set(before) & set(after))
    if not common:
        return {"delta": 0.0, "ci": (0.0, 0.0), "n": 0, "n_boot": n_boot}

    def mean_delta(keys):
        return sum(after[k] - before[k] for k in keys) / len(keys)

    observed = mean_delta(common)
    rng = random.Random(seed)
    deltas = []
    for _ in range(n_boot):
        draw = [common[rng.randrange(len(common))] for _ in common]
        deltas.append(mean_delta(draw))
    deltas.sort()
    lo = deltas[int(0.025 * n_boot)]
    hi = deltas[int(0.975 * n_boot) - 1]
    return {"delta": observed, "ci": (lo, hi), "n": len(common), "n_boot": n_boot}


def verdict(ci: tuple[float, float]) -> str:
    lo, hi = ci
    if lo > 0:
        return "real"
    if hi < 0:
        return "regression"
    return "inside the noise band"
