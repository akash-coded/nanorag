from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402


def never_exceeds_budget(m):
    got = m.run_loop([120, 110, 130], budget=300, est_step=120)
    expect(got["spent"] <= 300,
           f"spent {got['spent']} on a 300 budget. The guard checks after spending; it has to "
           "check whether the NEXT step fits, before taking it")
    return Measured(f"spent {got['spent']}/300 in {got['taken']} steps, reason={got['reason']!r}")


def reason_is_budget(m):
    got = m.run_loop([120, 110, 130], budget=300, est_step=120)
    expect(got["reason"] == "budget", f"it stopped because of the budget; reason should say so, got {got['reason']!r}")


def finishes_when_it_can(m):
    got = m.run_loop([50, 50, 50], budget=1000, est_step=50)
    expect(got == {"spent": 150, "taken": 3, "reason": "done"}, f"with plenty of budget, take every step: {got}")


def uses_the_estimate(m):
    """Hidden: the guard must reason about the NEXT step, which it can only estimate."""
    got = m.run_loop([100, 100], budget=150, est_step=100)
    expect(got["taken"] == 1, f"after 100 spent, a 100-token step does not fit in 150; got {got}")


def exact_fit(m):
    """Hidden: a step that lands exactly on the budget is affordable."""
    got = m.run_loop([100, 100], budget=200, est_step=100)
    expect(got["taken"] == 2 and got["reason"] == "done", f"200 spent on a 200 budget is not over: {got}")


def no_steps(m):
    """Hidden."""
    expect(m.run_loop([], budget=100, est_step=10) == {"spent": 0, "taken": 0, "reason": "done"}, "no steps: done at zero")


CHECKS = [
    Check("never spends past the budget", "The symptom", never_exceeds_budget),
    Check("the reason still says budget", "Trace must be honest", reason_is_budget),
    Check("takes every step when it can", "Do not stop early", finishes_when_it_can),
    Check("guards on the estimated next step", "Before, not after", uses_the_estimate, public=False),
    Check("exact fit is affordable", ">= vs >", exact_fit, public=False),
    Check("no steps", "Degenerate", no_steps, public=False),
]
