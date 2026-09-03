"""Reference for C06."""
from __future__ import annotations


def expected_agreement(h: float, j: float) -> float:
    return h * j + (1 - h) * (1 - j)
