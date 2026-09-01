"""L03 · BM25's IDF, by hand.

Run:  python scripts/lab.py run L03
"""
from __future__ import annotations

import math
import re


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-alphanumerics, drop empties."""
    return [t for t in re.split(r"[^a-z0-9_]+", text.lower()) if t]


def df_from_corpus(docs: list[str]) -> dict[str, int]:
    """Document frequency: how many DOCUMENTS contain each term.

    A term appearing five times in one document has df 1, not 5.
    """
    # TODO
    raise NotImplementedError


def idf(n_docs: int, df: int) -> float:
    """Robertson-Sparck Jones IDF.

        log( (N - df + 0.5) / (df + 0.5) )

    Use the natural log. Do NOT floor the result at zero — the sign is the lesson.
    """
    # TODO
    raise NotImplementedError
