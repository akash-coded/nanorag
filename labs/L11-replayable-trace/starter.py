"""L11 · A replayable trace.

Run:  python scripts/lab.py run L11
"""
from __future__ import annotations

import hashlib
import json


def config_fingerprint(config: dict) -> str:
    """A stable 8-char hash of a config.

    - Key ORDER must not matter: {"a":1,"b":2} and {"b":2,"a":1} are the same
      system and must fingerprint identically.
    - A changed VALUE must change the fingerprint.
    - Return the first 8 hex chars of the sha256 of the canonical JSON.
    """
    # TODO
    raise NotImplementedError


def build_trace(query: str, config: dict, candidates: list[dict],
                packed: list[str], gold: list[str], answer: str,
                stage_ms: dict[str, float]) -> dict:
    """Assemble the trace.

    `candidates` are [{"chunk_id", "score", "method"}] in rank order.

    Return:
      {"query", "config_fp", "candidate_ids", "packed_ids", "gold",
       "answer", "stage_ms", "total_ms", "k_collapse"}

    - `candidate_ids` and `packed_ids` are id lists in order. Store references,
      not chunk text -- the text is already in the index.
    - `total_ms` is the sum of `stage_ms`.
    - `k_collapse` is how many candidates did NOT make it into packed.
    """
    # TODO
    raise NotImplementedError


def attribute(trace: dict, answer_correct: bool) -> str:
    """Return one of the four verdicts.

      "retrieval miss"     gold not in candidate_ids
      "packing loss"       gold in candidate_ids, not all in packed_ids
      "generation failure" all gold in packed_ids, answer wrong
      "right by accident"  answer right, but not all gold was packed

    Check "right by accident" FIRST -- a correct answer with missing evidence is
    that verdict regardless of where the evidence was lost.
    With correct answer and all gold packed, return "ok".
    """
    # TODO
    raise NotImplementedError
