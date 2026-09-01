"""L01 · Give a chunk an id that survives an edit.

Implement `chunk_id` so that re-ingesting a document changes the id of exactly
the chunks whose text changed -- no more, no fewer.

Run:  python scripts/lab.py run L01
"""
from __future__ import annotations

import hashlib
import re


def normalise(text: str) -> str:
    """Collapse whitespace so a re-extraction does not look like an edit.

    A different PDF extractor, a trailing newline, or Windows line endings must
    not change the id. Only the words are the content.
    """
    # TODO: return the text with all runs of whitespace collapsed to a single
    #       space, and leading/trailing whitespace stripped.
    raise NotImplementedError


def chunk_id(doc_id: str, ordinal: int, text: str) -> str:
    """Return a stable id of the form  doc_id:ordinal:hash8

    - `doc_id` and `ordinal` locate the chunk inside its document
    - `hash8` is the first 8 hex characters of the sha256 of the NORMALISED text

    Example:  "incident-4471:19:9f2c1ab0"
    """
    # TODO: build the id. Hash the normalised text, not the raw text.
    raise NotImplementedError
