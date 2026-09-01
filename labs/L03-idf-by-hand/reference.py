"""Reference solution for L03."""
from __future__ import annotations

import math
import re


def tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9_]+", text.lower()) if t]


def df_from_corpus(docs: list[str]) -> dict[str, int]:
    df: dict[str, int] = {}
    for doc in docs:
        for term in set(tokenize(doc)):
            df[term] = df.get(term, 0) + 1
    return df


def idf(n_docs: int, df: int) -> float:
    return math.log((n_docs - df + 0.5) / (df + 0.5))
