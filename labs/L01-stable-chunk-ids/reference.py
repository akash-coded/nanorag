"""Reference solution for L01. Read it after you pass, not before."""
from __future__ import annotations

import hashlib
import re


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_id(doc_id: str, ordinal: int, text: str) -> str:
    digest = hashlib.sha256(normalise(text).encode("utf-8")).hexdigest()[:8]
    return f"{doc_id}:{ordinal}:{digest}"
