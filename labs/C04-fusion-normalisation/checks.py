from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402


def minimum_maps_to_zero(m):
    got = m._normalise({"a": 8.8, "b": 18.4, "c": 12.0})
    expect(abs(got["a"]) < 1e-9,
           f"the leg's minimum (8.8) should normalise to 0.0, got {got['a']:.3f}. "
           "Whatever you divide by, the minimum must land on zero")
    expect(abs(got["b"] - 1.0) < 1e-9, f"the maximum should be 1.0, got {got['b']:.3f}")
    return Measured("min→0.0, max→1.0: the leg spans the full unit interval")


def offset_leg_is_not_compressed(m):
    a = m._normalise({"x": 100.0, "y": 110.0})
    b = m._normalise({"x": 0.0, "y": 10.0})
    expect(abs(a["x"] - b["x"]) < 1e-9 and abs(a["y"] - b["y"]) < 1e-9,
           f"two legs with the same spread but different offsets must normalise identically; "
           f"got {a} vs {b}. Dividing by the max alone is offset-sensitive")


def fusion_is_now_fair(m):
    dense = {"A": 0.81, "B": 0.74}
    lex = {"A": 18.4, "B": 8.8}
    got = dict(m.weighted_fusion(dense, lex, alpha=0.5))
    expect(abs(got["B"]) < 1e-9,
           f"B is the minimum of BOTH legs, so its fused score must be 0.0, got {got['B']:.3f}")


def flat_leg_unchanged(m):
    """Hidden: the fix must not break the flat-leg guard."""
    got = m._normalise({"a": 3.0, "b": 3.0})
    expect(all(v == 0.0 for v in got.values()), f"a flat leg should still map to all zeros: {got}")


def negative_scores(m):
    """Hidden: cosine can be negative."""
    got = m._normalise({"a": -0.2, "b": 0.6})
    expect(abs(got["a"]) < 1e-9 and abs(got["b"] - 1.0) < 1e-9, f"negative minimum must still map to 0: {got}")


def single_candidate(m):
    """Hidden."""
    got = m._normalise({"only": 5.0})
    expect(got == {"only": 0.0}, f"one candidate has no spread; expected 0.0, got {got}")


CHECKS = [
    Check("the minimum maps to 0.0", "The symptom", minimum_maps_to_zero),
    Check("offset does not compress a leg", "Scale-free means offset-free", offset_leg_is_not_compressed),
    Check("fusion no longer favours the offset leg", "End to end", fusion_is_now_fair),
    Check("flat leg still guarded", "Do not break the divide-by-zero guard", flat_leg_unchanged, public=False),
    Check("negative scores", "Cosine goes below zero", negative_scores, public=False),
    Check("single candidate", "No spread", single_candidate, public=False),
]
