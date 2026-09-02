"""C01 · Fill the sentence-boundary rule.  Replace each ____ .

Run:  python scripts/lab.py run C01
"""
from __future__ import annotations

import re

# A boundary is: a terminator, then whitespace, then the start of a sentence.
TERMINATORS = ____          # the three characters that can end a sentence, as a str
STARTS = ____               # the regex character class for what can BEGIN one: A-Z0-9


def _boundary() -> re.Pattern:
    return re.compile(
        r"(?<=[" + re.escape(TERMINATORS) + r"])"   # look behind: just after a terminator
        r"\s+"                                        # the whitespace between sentences
        r"(?=[" + STARTS + r"])"                      # look ahead: a sentence start
    )


def split_sentences(text: str) -> list[str]:
    parts = _boundary().split(text.strip())
    return [p.strip() for p in parts if p.strip()]     # drop empties


def chunk(text: str, max_sentences: int = ____) -> list[str]:
    """Group sentences into chunks of at most `max_sentences`. Default is 3."""
    sents = split_sentences(text)
    return [" ".join(sents[i:i + max_sentences]) for i in range(0, len(sents), max_sentences)]
