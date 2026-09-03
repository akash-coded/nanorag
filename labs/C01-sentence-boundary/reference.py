"""Reference solution for C01."""
from __future__ import annotations

import re

TERMINATORS = ".!?"
STARTS = "A-Z0-9"


def _boundary() -> re.Pattern:
    return re.compile(
        r"(?<=[" + re.escape(TERMINATORS) + r"])"
        r"\s+"
        r"(?=[" + STARTS + r"])"
    )


def split_sentences(text: str) -> list[str]:
    parts = _boundary().split(text.strip())
    return [p.strip() for p in parts if p.strip()]


def chunk(text: str, max_sentences: int = 3) -> list[str]:
    sents = split_sentences(text)
    return [" ".join(sents[i:i + max_sentences]) for i in range(0, len(sents), max_sentences)]
