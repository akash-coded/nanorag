"""Reference solution for L07."""
from __future__ import annotations


def evidence_recall(gold: list[str], packed: list[str]) -> float:
    if not gold:
        return 0.0
    return sum(1 for g in gold if g in set(packed)) / len(gold)


def full_chain_recall(gold: list[str], packed: list[str]) -> float:
    if not gold:
        return 0.0
    return 1.0 if set(gold) <= set(packed) else 0.0


def full_chain_recall_at_n(gold: list[str], pool: list[str]) -> float:
    if not gold:
        return 0.0
    return 1.0 if set(gold) <= set(pool) else 0.0


def found_then_dropped(rows: list[dict]) -> list[str]:
    return [
        r["qid"] for r in rows
        if full_chain_recall_at_n(r["gold"], r["pool"]) == 1.0
        and full_chain_recall(r["gold"], r["packed"]) == 0.0
    ]
