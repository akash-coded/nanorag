"""Reference solution for L09."""
from __future__ import annotations


def confusion(human: list[bool], judge: list[bool]) -> dict[str, int]:
    if len(human) != len(judge):
        raise ValueError(f"unpaired labels: {len(human)} human, {len(judge)} judge")
    counts = {"tt": 0, "tf": 0, "ft": 0, "ff": 0}
    for h, j in zip(human, judge):
        counts[("t" if h else "f") + ("t" if j else "f")] += 1
    return counts


def cohens_kappa(human: list[bool], judge: list[bool]) -> float:
    n = len(human)
    if n == 0:
        return 0.0
    c = confusion(human, judge)
    p_o = (c["tt"] + c["ff"]) / n
    h_true = (c["tt"] + c["tf"]) / n
    j_true = (c["tt"] + c["ft"]) / n
    p_e = h_true * j_true + (1 - h_true) * (1 - j_true)
    if p_e >= 1.0:
        return 0.0
    return (p_o - p_e) / (1 - p_e)


def agreement_report(human: list[bool], judge: list[bool]) -> dict:
    n = len(human)
    c = confusion(human, judge)
    return {
        "n": n,
        "raw": (c["tt"] + c["ff"]) / n if n else 0.0,
        "kappa": cohens_kappa(human, judge),
        "base_rate": (c["tt"] + c["tf"]) / n if n else 0.0,
    }
