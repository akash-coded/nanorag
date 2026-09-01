"""Reference solution for L10."""
from __future__ import annotations

PRICE = {"input_per_1k": 0.003, "output_per_1k": 0.015, "embed_per_1k": 0.00002}


def query_cost(prompt_tokens: int, output_tokens: int, price: dict = PRICE) -> float:
    return (prompt_tokens / 1000 * price["input_per_1k"]
            + output_tokens / 1000 * price["output_per_1k"])


def monthly_tco(chunks: int, avg_chunk_tokens: int, queries_per_month: int,
                prompt_tokens: int, output_tokens: int, change_rate: float,
                cluster_monthly: float, price: dict = PRICE) -> dict:
    generation = queries_per_month * query_cost(prompt_tokens, output_tokens, price)
    backfill = chunks * avg_chunk_tokens / 1000 * price["embed_per_1k"]
    reembed = backfill * change_rate
    total = generation + backfill + reembed + cluster_monthly
    return {"generation": generation, "backfill": backfill, "reembed": reembed,
            "cluster": cluster_monthly, "total": total,
            "generation_share": generation / total if total else 0.0}


def pick_threshold(pairs: list[tuple[float, bool]], min_precision: float = 0.99) -> dict:
    best = None
    for theta in sorted({sim for sim, _ in pairs}, reverse=True):
        served = [same for sim, same in pairs if sim >= theta]
        if not served:
            continue
        precision = sum(served) / len(served)
        if precision >= min_precision:
            best = {"theta": theta, "precision": precision,
                    "hit_rate": len(served) / len(pairs),
                    "false_hits": len(served) - sum(served)}
    if best is None:
        return {"theta": 1.1, "precision": 1.0, "hit_rate": 0.0, "false_hits": 0}
    return best
