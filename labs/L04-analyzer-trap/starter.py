"""L04 · The analyzer trap.

Run:  python scripts/lab.py run L04
"""
from __future__ import annotations

import re

# Characters we have decided to keep INSIDE tokens rather than split on.
TOKEN_CHARS = "_-/"


def separator_census(chunks: list[str]) -> dict[str, int]:
    """Count how many CHUNKS contain each non-alphanumeric, non-space character.

    Chunk counts, not occurrence counts — the decision is about blast radius.
    Ignore whitespace entirely.
    """
    # TODO
    raise NotImplementedError


def analyzer_tokenize(text: str, token_chars: str = TOKEN_CHARS) -> list[str]:
    """Lowercase and split on any character that is NOT alphanumeric and NOT in
    `token_chars`.

        "ERR_CONN_RESET timed out."  ->  ["err_conn_reset", "timed", "out"]
        "see docs/adr and v2.1.4"    ->  ["see", "docs/adr", "and", "v2", "1", "4"]

    Note the second example: '.' is deliberately NOT a token char, so version
    strings still split. That is the trade this lab is about.

    Drop empty tokens, and strip any leading/trailing token_chars so that a
    trailing hyphen in prose does not become part of the term.
    """
    # TODO
    raise NotImplementedError
