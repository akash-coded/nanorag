"""Reference solution for C02."""
from __future__ import annotations

import re

_SPLIT = re.compile(r"[^a-z0-9_-]+")


def tokenize(text: str) -> list[str]:
    text = text.lower()
    return [t for t in _SPLIT.split(text) if t]
