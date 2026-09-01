"""L06 · Pack a prompt to a hard token budget.

Run:  python scripts/lab.py run L06
"""
from __future__ import annotations


def estimate_tokens(text: str) -> int:
    """Cheap, deterministic token estimate: ceil(len(text) / 4).

    Deliberately not a real tokenizer. A packer that needs a model loaded to
    decide what fits cannot run in a unit test, and the estimate only has to be
    consistent to make the budget decision reproducible.
    """
    # TODO
    raise NotImplementedError


def pack_context(chunks: list[dict], budget: int) -> dict:
    """Pack ranked chunks into a context block under a hard token budget.

    `chunks` are already in rank order, each {"chunk_id": str, "text": str}.

    Rules:
      - Take chunks in order. Include a chunk only if it fits WHOLE in the
        remaining budget. Stop at the first one that does not fit.
      - Never truncate. Leftover budget is the correct outcome.
      - Label each included chunk [1], [2], ... by POSITION in the packed set.
      - The rendered block joins entries as "[n] <text>" with a blank line
        between them.

    Return:
      {"text": str, "included": [chunk_id, ...], "tokens": int, "dropped": int}

    `tokens` is the estimate for the rendered block. `dropped` is how many of
    the input chunks did not make it.
    """
    # TODO
    raise NotImplementedError
