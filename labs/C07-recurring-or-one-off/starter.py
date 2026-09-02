"""C07 · Classify each cost.  Replace each ____ with "recurring" or "one-off".

Run:  python scripts/lab.py run C07
"""
GENERATION_TOKENS = ____      # every query
INITIAL_BACKFILL = ____       # embedding the corpus the first time
REEMBED_ON_DRIFT = ____       # re-embedding what changed this month
VECTOR_CLUSTER = ____         # the index serving infrastructure
RERANKER_INFERENCE = ____     # scoring candidates on every query
ENCODER_UPGRADE = ____        # moving to a new embedding model


def classify() -> dict[str, str]:
    return {
        "generation_tokens": GENERATION_TOKENS,
        "initial_backfill": INITIAL_BACKFILL,
        "reembed_on_drift": REEMBED_ON_DRIFT,
        "vector_cluster": VECTOR_CLUSTER,
        "reranker_inference": RERANKER_INFERENCE,
        "encoder_upgrade": ENCODER_UPGRADE,
    }
