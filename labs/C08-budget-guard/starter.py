"""C08 · The loop overspends.  Fix the guard.

Run:  python scripts/lab.py run C08
"""
from __future__ import annotations


def run_loop(steps: list[int], budget: int, est_step: int) -> dict:
    """`steps` are the token costs the agent WOULD spend, in order.
    Take steps while there is budget for the next one; stop otherwise.

    Return {"spent": int, "taken": int, "reason": "budget" | "done"}.
    """
    spent, taken = 0, 0
    for cost in steps:
        spent += cost
        taken += 1
        if spent > budget:
            return {"spent": spent, "taken": taken, "reason": "budget"}
    return {"spent": spent, "taken": taken, "reason": "done"}
