from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402


def mk(n, size=200):
    return [{"chunk_id": f"c{i}", "text": f"Chunk {i}. " + "x" * size} for i in range(1, n + 1)]


def token_estimate(m):
    expect(m.estimate_tokens("abcd") == 1, f"'abcd' is 4 chars -> 1 token, got {m.estimate_tokens('abcd')}")
    expect(m.estimate_tokens("abcde") == 2,
           f"5 chars must round UP to 2, got {m.estimate_tokens('abcde')} — rounding down "
           "lets a packer exceed its budget by a token per chunk")
    expect(m.estimate_tokens("") == 0, "empty text is 0 tokens")


def respects_the_budget(m):
    chunks = mk(8)
    budget = 150
    got = m.pack_context(chunks, budget)
    expect(got["tokens"] <= budget,
           f"packed {got['tokens']} tokens into a {budget} budget — the budget is hard")
    expect(len(got["included"]) < 8, "with this budget not everything should fit")
    return Measured(f"{len(got['included'])}/8 chunks, {got['tokens']}/{budget} tokens "
                    f"({budget - got['tokens']} slack)")


def never_truncates(m):
    chunks = mk(8)
    got = m.pack_context(chunks, 150)
    for chunk in chunks:
        if chunk["chunk_id"] in got["included"]:
            expect(chunk["text"] in got["text"],
                   f"{chunk['chunk_id']} is listed as included but its text is not intact in the "
                   "block. A truncated chunk still gets a citation marker, and that citation "
                   "points at something that does not say what it claims")


def labels_by_position(m):
    got = m.pack_context(mk(3, size=10), 500)
    markers = re.findall(r"\[(\d+)\]", got["text"])
    expect(markers == ["1", "2", "3"],
           f"expected positional markers [1] [2] [3], got {markers}. Citation numbers are "
           "positions in THIS prompt, not chunk identity")


def preserves_rank_order(m):
    chunks = mk(6)
    got = m.pack_context(chunks, 200)
    order = [c["chunk_id"] for c in chunks if c["chunk_id"] in got["included"]]
    expect(got["included"] == order,
           f"included chunks must stay in rank order; got {got['included']}")


def stops_at_first_miss(m):
    """Hidden: no greedy backfill — a later small chunk must NOT jump the queue."""
    chunks = [
        {"chunk_id": "big", "text": "y" * 4000},
        {"chunk_id": "small", "text": "tiny"},
    ]
    got = m.pack_context(chunks, 100)
    expect("small" not in got["included"],
           "'small' was backfilled after 'big' did not fit. Greedy backfill makes inclusion "
           "depend on the sizes of the chunks above it, so a metric change can no longer be "
           "attributed to the ranker")
    expect(got["included"] == [], f"nothing should fit; got {got['included']}")


def budget_zero_and_empty(m):
    """Hidden: degenerate budgets."""
    got = m.pack_context(mk(3), 0)
    expect(got["included"] == [] and got["text"] == "", f"a zero budget packs nothing; got {got}")
    expect(got["dropped"] == 3, f"dropped should be 3, got {got['dropped']}")
    empty = m.pack_context([], 500)
    expect(empty["included"] == [] and empty["dropped"] == 0, f"no chunks in, none out; got {empty}")


def counts_the_separator(m):
    """Hidden: the blank line between entries costs tokens too."""
    one = m.pack_context(mk(1, size=40), 10_000)["tokens"]
    two = m.pack_context(mk(2, size=40), 10_000)["tokens"]
    expect(two > 2 * one - 2,
           f"two chunks cost {two} and one costs {one}; the separator between entries has to be "
           "counted or the budget silently overruns as k grows")


def dropped_is_accurate(m):
    """Hidden: the caller needs to know what it lost."""
    got = m.pack_context(mk(8), 150)
    expect(got["dropped"] == 8 - len(got["included"]),
           f"dropped={got['dropped']} does not match 8 - {len(got['included'])} included. "
           "This number is how a caller detects k_collapse")
    return Measured(f"dropped {got['dropped']} of 8 — this is the k_collapse signal")


CHECKS = [
    Check("token estimate rounds up", "Rounding down overruns", token_estimate),
    Check("packs under a hard budget", "The constraint", respects_the_budget),
    Check("never truncates a chunk", "Citations must be honest", never_truncates),
    Check("labels by position in the packed set", "[n] is a position", labels_by_position),
    Check("keeps rank order", "The ranker decides", preserves_rank_order),
    Check("stops at the first chunk that does not fit", "No greedy backfill", stops_at_first_miss, public=False),
    Check("zero budget and empty input", "Degenerate cases", budget_zero_and_empty, public=False),
    Check("counts the separator between entries", "Silent overrun as k grows", counts_the_separator, public=False),
    Check("reports how many were dropped", "The k_collapse signal", dropped_is_accurate, public=False),
]
