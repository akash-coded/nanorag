"""C02 · The tokenizer has a bug.  Fix it with the smallest change you can.

Run:  python scripts/lab.py run C02
"""
from __future__ import annotations

import re

# Split on anything that is not a letter, digit, or one of the characters that
# belong INSIDE an identifier.
_SPLIT = re.compile(r"[^a-z0-9_-]+")


def tokenize(text: str) -> list[str]:
    text = text.lower().replace("_", " ")          # normalise identifiers
    return [t for t in _SPLIT.split(text) if t]
