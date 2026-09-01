"""Reference solution for L06."""
from __future__ import annotations

import math


def estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / 4)


def pack_context(chunks: list[dict], budget: int) -> dict:
    included, blocks, used = [], [], 0
    for chunk in chunks:
        entry = f"[{len(included) + 1}] {chunk['text']}"
        cost = estimate_tokens(entry)
        separator = estimate_tokens("\n\n") if blocks else 0
        if used + separator + cost > budget:
            break
        blocks.append(entry)
        included.append(chunk["chunk_id"])
        used += separator + cost
    text = "\n\n".join(blocks)
    return {"text": text, "included": included,
            "tokens": estimate_tokens(text), "dropped": len(chunks) - len(included)}
