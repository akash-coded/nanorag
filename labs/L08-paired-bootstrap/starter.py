"""L08 · The paired bootstrap.

Run:  python scripts/lab.py run L08
"""
from __future__ import annotations

import random


def paired_bootstrap(before: dict[str, float], after: dict[str, float],
                     n_boot: int = 2000, seed: int = 11) -> dict:
    """Resample QUESTIONS with replacement, keeping both arms paired.

    `before` and `after` map qid -> metric value. Use only the qids present in
    BOTH; a question missing from one arm cannot be paired.

    Procedure:
      1. common = sorted qids in both arms  (sort so the result is reproducible)
      2. delta = mean(after) - mean(before) over `common`
      3. n_boot times: draw len(common) qids WITH replacement using
         random.Random(seed), recompute the delta on that draw
      4. sort the resampled deltas; lo = index int(0.025 * n_boot),
         hi = index int(0.975 * n_boot) - 1

    Return {"delta": float, "ci": (lo, hi), "n": int, "n_boot": int}
    With no common qids, return delta 0.0, ci (0.0, 0.0), n 0.
    """
    # TODO
    raise NotImplementedError


def verdict(ci: tuple[float, float]) -> str:
    """"real" if the whole interval is above zero,
    "regression" if the whole interval is below zero,
    "inside the noise band" if it straddles zero.
    """
    # TODO
    raise NotImplementedError
