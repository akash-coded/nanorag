"""Reference solution for L12."""
from __future__ import annotations

MIN_SLICE_N = 30


def _verdict(ci) -> str:
    lo, hi = ci
    if lo > 0:
        return "real"
    if hi < 0:
        return "regression"
    return "band"


def slice_verdict(result: dict, min_n: int = MIN_SLICE_N) -> str:
    if result.get("n", 0) < min_n:
        return "skipped"
    return _verdict(result["ci"])


def evaluate_gate(primary: str, metrics: list[dict], slices: list[dict],
                  pre_registered: str | None, cost_delta_pct: float,
                  cost_budget_pct: float = 25.0, min_n: int = MIN_SLICE_N) -> dict:
    skipped = [s["name"] for s in slices if s.get("n", 0) < min_n]

    def out(ship, reason):
        return {"ship": ship, "reason": reason, "skipped_slices": skipped}

    if pre_registered != primary:
        return out(False, "primary metric was not pre-registered")

    by_name = {m["name"]: m for m in metrics}
    if primary not in by_name:
        return out(False, f"primary metric {primary} was not measured")
    if _verdict(by_name[primary]["ci"]) != "real":
        return out(False, "primary metric did not clear the noise band")

    for metric in metrics:
        if metric["name"] != primary and _verdict(metric["ci"]) == "regression":
            return out(False, f"secondary regression: {metric['name']}")

    for sl in slices:
        if slice_verdict(sl, min_n) == "regression":
            return out(False, f"slice regression: {sl['name']}")

    if cost_delta_pct > cost_budget_pct:
        return out(False, f"cost regression: +{cost_delta_pct:.0f}% exceeds "
                          f"{cost_budget_pct:.0f}% budget")
    return out(True, "all gates clear")


def decision_record(gate: dict, primary: str, metrics: list[dict]) -> str:
    status = "SHIP" if gate["ship"] else "BLOCKED"
    lines = [
        f"# Release decision: {status}",
        "",
        f"**Reason:** {gate['reason']}",
        f"**Primary metric:** `{primary}` (pre-registered)",
        "",
        "| Metric | Delta | 95% CI |",
        "|---|---:|---|",
    ]
    for m in metrics:
        lo, hi = m["ci"]
        mark = " ⭑" if m["name"] == primary else ""
        lines.append(f"| `{m['name']}`{mark} | {m['delta']:+.4f} | [{lo:+.4f}, {hi:+.4f}] |")
    skipped = ", ".join(gate["skipped_slices"]) or "none"
    lines += ["", f"**Skipped slices** (below the minimum size to gate on): {skipped}"]
    return "\n".join(lines)
