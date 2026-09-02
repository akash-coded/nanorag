"""Reference for C07."""
GENERATION_TOKENS = "recurring"
INITIAL_BACKFILL = "one-off"
REEMBED_ON_DRIFT = "recurring"
VECTOR_CLUSTER = "recurring"
RERANKER_INFERENCE = "recurring"
ENCODER_UPGRADE = "one-off"


def classify() -> dict[str, str]:
    return {
        "generation_tokens": GENERATION_TOKENS,
        "initial_backfill": INITIAL_BACKFILL,
        "reembed_on_drift": REEMBED_ON_DRIFT,
        "vector_cluster": VECTOR_CLUSTER,
        "reranker_inference": RERANKER_INFERENCE,
        "encoder_upgrade": ENCODER_UPGRADE,
    }
