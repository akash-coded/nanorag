"""L12 · The release gate.

A metric result looks like:
    {"name": "evidence_recall", "delta": 0.0281, "ci": (0.0164, 0.0402)}
A slice result adds "n".

Run:  python scripts/lab.py run L12
"""
from __future__ import annotations

MIN_SLICE_N = 30


def slice_verdict(result: dict, min_n: int = MIN_SLICE_N) -> str:
    """"skipped" if result["n"] < min_n -- too small to gate on, report it instead.
    Otherwise "real" / "regression" / "band" by the same interval rule as L08.
    """
    # TODO
    raise NotImplementedError


def evaluate_gate(primary: str, metrics: list[dict], slices: list[dict],
                  pre_registered: str | None, cost_delta_pct: float,
                  cost_budget_pct: float = 25.0, min_n: int = MIN_SLICE_N) -> dict:
    """Run the gate. Stop at the FIRST blocker.

    In order:
      1. `pre_registered` must equal `primary`, else block with reason
         "primary metric was not pre-registered"
      2. the primary metric must have verdict "real", else
         "primary metric did not clear the noise band"
      3. any OTHER metric with verdict "regression" ->
         "secondary regression: <name>"
      4. any slice with verdict "regression" -> "slice regression: <name>"
      5. cost_delta_pct > cost_budget_pct -> "cost regression: +N% exceeds budget"
      6. otherwise ship

    Return {"ship": bool, "reason": str, "skipped_slices": [names]}.
    `skipped_slices` always lists slices below min_n, shipping or not -- a gate
    that silently ignores a slice reads as if it covered it.
    """
    # TODO
    raise NotImplementedError


def decision_record(gate: dict, primary: str, metrics: list[dict]) -> str:
    """Render a markdown decision record.

    Must contain:
      - a heading line starting "# Release decision:" then SHIP or BLOCKED
      - the reason
      - a table row per metric with its delta and interval
      - a "Skipped slices" line naming them, or "none"

    Return the markdown string.
    """
    # TODO
    raise NotImplementedError
