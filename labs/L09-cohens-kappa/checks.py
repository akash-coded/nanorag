from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402


def _pair(tt, tf, ft, ff):
    human = [True] * (tt + tf) + [False] * (ft + ff)
    judge = [True] * tt + [False] * tf + [True] * ft + [False] * ff
    return human, judge


def counts_the_cells(m):
    h, j = _pair(176, 3, 9, 12)
    got = m.confusion(h, j)
    expect(got == {"tt": 176, "tf": 3, "ft": 9, "ff": 12}, f"got {got}")


def the_worked_example(m):
    h, j = _pair(176, 3, 9, 12)
    k = m.cohens_kappa(h, j)
    expect(0.55 < k < 0.65,
           f"94% raw agreement on this 90/10 split should give kappa ≈ 0.60, got {k:.4f}")
    return Measured(f"raw 94.0%  →  kappa {k:.3f}. Most of that 94% was chance")


def imbalance_moves_kappa(m):
    """Same raw agreement, different balance, different verdict."""
    balanced = m.cohens_kappa(*_pair(47, 3, 3, 47))     # 94% raw, 50/50
    skewed = m.cohens_kappa(*_pair(92, 3, 3, 2))         # 94% raw, 95/5
    expect(balanced > skewed + 0.2,
           f"the same 94% raw agreement should give a much higher kappa on a balanced set; "
           f"got balanced {balanced:.3f} vs skewed {skewed:.3f}")
    return Measured(f"94% raw: kappa {balanced:.3f} at 50/50, {skewed:.3f} at 95/5 — same judge")


def report_carries_the_base_rate(m):
    got = m.agreement_report(*_pair(176, 3, 9, 12))
    expect(set(got) == {"n", "raw", "kappa", "base_rate"}, f"unexpected keys: {sorted(got)}")
    expect(abs(got["base_rate"] - 0.895) < 0.01,
           f"human positive rate should be ≈0.895, got {got['base_rate']:.4f}")
    expect(got["n"] == 200, f"n should be 200, got {got['n']}")


def a_useless_judge_scores_zero(m):
    """Hidden: always-yes must not be rewarded."""
    human = [True] * 90 + [False] * 10
    judge = [True] * 100
    k = m.cohens_kappa(human, judge)
    expect(abs(k) < 1e-9,
           f"a judge that says True to everything has earned nothing beyond chance; "
           f"kappa should be 0.0, got {k:.6f}")


def kappa_can_go_negative(m):
    """Hidden: worse than chance is a real outcome."""
    k = m.cohens_kappa(*_pair(80, 15, 15, 0))
    expect(k < 0,
           f"agreement below chance must give a negative kappa, got {k:.4f}. If you clamped at "
           "zero you lose the signal that a label mapping is inverted")


def perfect_agreement_is_one(m):
    """Hidden: the top of the scale."""
    k = m.cohens_kappa(*_pair(50, 0, 0, 50))
    expect(abs(k - 1.0) < 1e-9, f"perfect agreement should be kappa 1.0, got {k}")


def degenerate_inputs(m):
    """Hidden: no labels, and one-class-only."""
    expect(m.cohens_kappa([], []) == 0.0, "no labels should give 0.0, not a crash")
    k = m.cohens_kappa([True] * 20, [True] * 20)
    expect(k == 0.0,
           f"if both raters used one class for everything, p_e is 1.0 and there is no agreement "
           f"left to earn — return 0.0, not NaN or a division error. Got {k}")


def unpaired_labels_raise(m):
    """Hidden: silently zipping to the shorter list loses data."""
    try:
        m.confusion([True, False, True], [True, False])
    except ValueError:
        return
    raise AssertionError(
        "mismatched label lengths should raise ValueError — zip() would silently drop the "
        "extra label and report a kappa computed on data you did not notice was truncated")


CHECKS = [
    Check("counts the four confusion cells", "The contingency table", counts_the_cells),
    Check("the worked example gives kappa ≈ 0.60", "94% raw is not 94% good", the_worked_example),
    Check("class balance moves kappa", "Same raw, different verdict", imbalance_moves_kappa),
    Check("the report carries the base rate", "Never quote kappa alone", report_carries_the_base_rate),
    Check("an always-yes judge scores zero", "Chance earns nothing", a_useless_judge_scores_zero, public=False),
    Check("kappa can go negative", "Worse than chance is real", kappa_can_go_negative, public=False),
    Check("perfect agreement is 1.0", "Top of the scale", perfect_agreement_is_one, public=False),
    Check("degenerate inputs do not divide by zero", "p_e = 1.0", degenerate_inputs, public=False),
    Check("unpaired label lists raise", "zip() would hide it", unpaired_labels_raise, public=False),
]
