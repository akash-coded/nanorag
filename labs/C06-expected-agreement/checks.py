from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402


def worked_example(m):
    got = m.expected_agreement(0.905, 0.895)
    want = 0.905 * 0.895 + 0.095 * 0.105
    expect(abs(got - want) < 1e-9, f"expected {want:.4f}, got {got:.4f}")
    return Measured(f"p_e = {got:.3f} — of a 94% raw agreement, that much was free")


def balanced_is_half(m):
    got = m.expected_agreement(0.5, 0.5)
    expect(abs(got - 0.5) < 1e-9, f"two fair coins agree half the time; got {got}")


def symmetric(m):
    expect(abs(m.expected_agreement(0.9, 0.3) - m.expected_agreement(0.3, 0.9)) < 1e-9,
           "p_e must not depend on which rater is which")


def both_always_yes(m):
    """Hidden: p_e = 1, so nothing is left to earn."""
    expect(abs(m.expected_agreement(1.0, 1.0) - 1.0) < 1e-9, "two always-yes raters agree 100% by chance")


def skew_raises_it(m):
    """Hidden: the more lopsided the split, the more agreement is free."""
    expect(m.expected_agreement(0.95, 0.95) > m.expected_agreement(0.9, 0.9) > m.expected_agreement(0.5, 0.5),
           "p_e should rise as both raters skew toward one class")
    return Measured(f"p_e at 50/50={m.expected_agreement(.5,.5):.2f}, 90/10={m.expected_agreement(.9,.9):.2f}, 95/5={m.expected_agreement(.95,.95):.3f}")


CHECKS = [
    Check("the worked example", "0.905 and 0.895", worked_example),
    Check("balanced raters: 0.5", "Two fair coins", balanced_is_half),
    Check("symmetric in h and j", "Order of raters", symmetric),
    Check("always-yes pair: 1.0", "Nothing left to earn", both_always_yes, public=False),
    Check("skew raises chance agreement", "Why the base rate matters", skew_raises_it, public=False),
]
