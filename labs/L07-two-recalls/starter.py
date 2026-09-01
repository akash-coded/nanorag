"""L07 · The two recalls.

Each eval row looks like:
    {"qid": "q1", "gold": ["c1", "c2"], "pool": [...], "packed": [...]}

Run:  python scripts/lab.py run L07
"""
from __future__ import annotations


def evidence_recall(gold: list[str], packed: list[str]) -> float:
    """Share of gold items present in the packed context.

    Continuous: 2 of 3 gold items is 0.5? No -- it is 2/3. With no gold at all,
    return 0.0 rather than dividing by zero.
    """
    # TODO
    raise NotImplementedError


def full_chain_recall(gold: list[str], packed: list[str]) -> float:
    """1.0 only if EVERY gold item is packed, else 0.0.

    Binary. No partial credit. With no gold at all, return 0.0.
    """
    # TODO
    raise NotImplementedError


def full_chain_recall_at_n(gold: list[str], pool: list[str]) -> float:
    """The same conjunction, measured over the candidate pool instead."""
    # TODO
    raise NotImplementedError


def found_then_dropped(rows: list[dict]) -> list[str]:
    """The diagnostic: qids where the pool had everything and packing lost some.

    That is full_chain_recall_at_n == 1.0 and full_chain_recall == 0.0.
    Return the qids in input order.
    """
    # TODO
    raise NotImplementedError
