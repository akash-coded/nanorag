from __future__ import annotations

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

# A clear, large improvement on every question.
BEFORE = {f"q{i}": 0.5 for i in range(200)}
AFTER = {f"q{i}": 0.8 for i in range(200)}
# A tiny improvement swamped by variance.

_rng = random.Random(0)
NOISY_B = {f"q{i}": _rng.choice([0.0, 1.0]) for i in range(60)}
NOISY_A = {k: (v if _rng.random() > 0.08 else 1.0 - v) for k, v in NOISY_B.items()}


def computes_the_delta(m):
    got = m.paired_bootstrap(BEFORE, AFTER, n_boot=500)
    expect(abs(got["delta"] - 0.3) < 1e-9, f"delta should be 0.3, got {got['delta']}")
    expect(got["n"] == 200, f"n should be 200, got {got['n']}")


def clear_effect_is_real(m):
    got = m.paired_bootstrap(BEFORE, AFTER, n_boot=500)
    lo, hi = got["ci"]
    expect(lo > 0, f"a +0.3 delta on every question must clear zero; CI was [{lo}, {hi}]")
    expect(m.verdict(got["ci"]) == "real", f"verdict should be 'real', got {m.verdict(got['ci'])!r}")
    return Measured(f"delta {got['delta']:+.4f}  CI [{lo:+.4f}, {hi:+.4f}]  n={got['n']}")


def deterministic_with_a_seed(m):
    a = m.paired_bootstrap(BEFORE, AFTER, n_boot=300, seed=7)
    b = m.paired_bootstrap(BEFORE, AFTER, n_boot=300, seed=7)
    expect(a["ci"] == b["ci"],
           f"same seed gave different intervals {a['ci']} vs {b['ci']} — a run you cannot "
           "reproduce is a number you cannot defend")


def n_boot_does_not_change_width(m):
    """The central lesson: resamples stabilise, they do not narrow."""
    widths = []
    for n_boot in (500, 2000, 8000):
        ci = m.paired_bootstrap(NOISY_B, NOISY_A, n_boot=n_boot)["ci"]
        widths.append(ci[1] - ci[0])
    spread = max(widths) - min(widths)
    expect(spread < 0.06,
           f"widths at n_boot 500/2000/8000 were {[round(w,4) for w in widths]} — a spread of "
           f"{spread:.4f}. n_boot controls how precisely the endpoints are ESTIMATED, not how "
           "wide the interval is. Width is set by n")
    return Measured("widths " + " / ".join(f"{w:.4f}" for w in widths) +
                    "  — 16x the resamples, same width")


def verdict_reads_the_interval(m):
    expect(m.verdict((0.01, 0.05)) == "real", "an interval above zero is 'real'")
    expect(m.verdict((-0.05, -0.01)) == "regression", "an interval below zero is a regression")
    expect(m.verdict((-0.01, 0.05)) == "inside the noise band",
           "an interval straddling zero is inside the band — NOT a regression")


def growing_n_narrows_it(m):
    """Hidden: the lever that actually works."""
    small = {f"q{i}": 0.5 for i in range(40)}
    small_a = {f"q{i}": 0.55 for i in range(40)}
    big = {f"q{i}": 0.5 for i in range(600)}
    big_a = {f"q{i}": 0.55 for i in range(600)}
    w_small = m.paired_bootstrap(small, small_a, n_boot=800)["ci"]
    w_big = m.paired_bootstrap(big, big_a, n_boot=800)["ci"]
    expect((w_big[1] - w_big[0]) <= (w_small[1] - w_small[0]) + 1e-9,
           f"a larger eval set should not give a wider interval; {w_small} vs {w_big}")


def only_pairs_common_questions(m):
    """Hidden: an unpaired question cannot contribute."""
    got = m.paired_bootstrap({"a": 0.0, "b": 0.0}, {"a": 1.0, "c": 1.0}, n_boot=200)
    expect(got["n"] == 1, f"only 'a' is in both arms, so n should be 1, got {got['n']}")


def empty_overlap(m):
    """Hidden: no shared questions is a valid state."""
    got = m.paired_bootstrap({"a": 1.0}, {"b": 1.0}, n_boot=100)
    expect(got["n"] == 0 and got["delta"] == 0.0,
           f"no common qids should give n=0 and delta 0.0, got {got}")


def binary_metric_is_wider(m):
    """Hidden: binary metrics need more data for the same effect."""
    n = 120
    cont_b = {f"q{i}": 0.5 for i in range(n)}
    cont_a = {f"q{i}": 0.6 for i in range(n)}
    bin_b = {f"q{i}": float(i % 2) for i in range(n)}
    bin_a = {f"q{i}": float((i + (1 if i < n // 10 else 0)) % 2) for i in range(n)}
    w_cont = m.paired_bootstrap(cont_b, cont_a, n_boot=800)["ci"]
    w_bin = m.paired_bootstrap(bin_b, bin_a, n_boot=800)["ci"]
    expect((w_bin[1] - w_bin[0]) > (w_cont[1] - w_cont[0]),
           "a binary metric should give a wider interval than a constant-shift continuous one "
           f"at the same n; got binary {w_bin} vs continuous {w_cont}")
    return Measured(f"same n={n}: binary width {w_bin[1]-w_bin[0]:.4f} vs "
                    f"continuous {w_cont[1]-w_cont[0]:.4f}")


CHECKS = [
    Check("computes the paired delta", "Per-question differences", computes_the_delta),
    Check("a clear effect clears zero", "The happy path", clear_effect_is_real),
    Check("the same seed gives the same interval", "Reproducible or indefensible", deterministic_with_a_seed),
    Check("n_boot does not change the width", "The central lesson", n_boot_does_not_change_width),
    Check("verdict reads the interval, not the point", "Band is not regression", verdict_reads_the_interval),
    Check("growing n narrows the interval", "The lever that works", growing_n_narrows_it, public=False),
    Check("only questions in both arms are paired", "Unpaired cannot contribute", only_pairs_common_questions, public=False),
    Check("no overlap is handled", "Degenerate input", empty_overlap, public=False),
    Check("a binary metric gives a wider interval", "Why the two verdicts differ", binary_metric_is_wider, public=False),
]
