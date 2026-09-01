"""Reference solution for L02."""
from __future__ import annotations

SEP = " › "


def heading_path(headings: list[tuple[int, str]], max_depth: int = 4) -> str:
    if not headings:
        return ""
    kept = headings[-max_depth:] if max_depth > 0 else []
    return SEP.join(text for _level, text in kept)


def chunk_with_path(text: str, headings: list[tuple[int, str]]) -> dict:
    path = heading_path(headings)
    return {"text": f"{path}\n{text}" if path else text, "heading_path": path}
