"""Reference solution for L11."""
from __future__ import annotations

import hashlib
import json


def config_fingerprint(config: dict) -> str:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:8]


def build_trace(query: str, config: dict, candidates: list[dict],
                packed: list[str], gold: list[str], answer: str,
                stage_ms: dict[str, float]) -> dict:
    candidate_ids = [c["chunk_id"] for c in candidates]
    return {
        "query": query,
        "config_fp": config_fingerprint(config),
        "candidate_ids": candidate_ids,
        "packed_ids": list(packed),
        "gold": list(gold),
        "answer": answer,
        "stage_ms": dict(stage_ms),
        "total_ms": sum(stage_ms.values()),
        "k_collapse": len(candidate_ids) - len(packed),
    }


def attribute(trace: dict, answer_correct: bool) -> str:
    gold = set(trace["gold"])
    in_pool = gold <= set(trace["candidate_ids"])
    in_packed = gold <= set(trace["packed_ids"])
    if answer_correct and not in_packed:
        return "right by accident"
    if answer_correct:
        return "ok"
    if not in_pool:
        return "retrieval miss"
    if not in_packed:
        return "packing loss"
    return "generation failure"
