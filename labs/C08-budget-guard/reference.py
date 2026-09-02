"""Reference for C08."""
from __future__ import annotations


def run_loop(steps: list[int], budget: int, est_step: int) -> dict:
    spent, taken = 0, 0
    for cost in steps:
        if spent + est_step > budget:
            return {"spent": spent, "taken": taken, "reason": "budget"}
        spent += cost
        taken += 1
    return {"spent": spent, "taken": taken, "reason": "done"}
