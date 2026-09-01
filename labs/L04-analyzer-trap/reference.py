"""Reference solution for L04."""
from __future__ import annotations

import re

TOKEN_CHARS = "_-/"


def separator_census(chunks: list[str]) -> dict[str, int]:
    census: dict[str, int] = {}
    for chunk in chunks:
        for ch in {c for c in chunk if not c.isalnum() and not c.isspace()}:
            census[ch] = census.get(ch, 0) + 1
    return census


def analyzer_tokenize(text: str, token_chars: str = TOKEN_CHARS) -> list[str]:
    keep = re.escape(token_chars)
    raw = re.split(rf"[^a-z0-9{keep}]+", text.lower())
    out = []
    for token in raw:
        token = token.strip(token_chars)
        if token:
            out.append(token)
    return out
