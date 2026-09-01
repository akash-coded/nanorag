"""L02 · Carry the heading path into every chunk.

Run:  python scripts/lab.py run L02
"""
from __future__ import annotations

SEP = " › "


def heading_path(headings: list[tuple[int, str]], max_depth: int = 4) -> str:
    """Build a breadcrumb from the heading stack above a chunk.

    `headings` is the ordered stack of (level, text) pairs from the document
    root down to the chunk, e.g.
        [(1, "Household"), (2, "Section 4 — Water damage"), (3, "4.3 Flood")]

    - Join with SEP.
    - If the stack is deeper than `max_depth`, keep the DEEPEST `max_depth`
      entries. The nearest headings carry the most information.
    - An empty stack gives an empty string.
    """
    # TODO
    raise NotImplementedError


def chunk_with_path(text: str, headings: list[tuple[int, str]]) -> dict:
    """Return the chunk as the store expects it.

        {"text": "<path>\\n<text>", "heading_path": "<path>"}

    - `text` gets the path prepended, separated by a single newline.
    - `heading_path` holds the same path, for filtering and the UI.
    - With no headings, `text` is unchanged and `heading_path` is "".
      Do NOT emit a leading newline in that case.
    """
    # TODO
    raise NotImplementedError
