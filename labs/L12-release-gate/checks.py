from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

METRICS = [
    {"name": "evidence_recall",   "delta": 0.0281, "ci": (0.0164, 0.0402)},
    {"name": "full_chain_recall", "delta": 0.0116, "ci": (-0.0038, 0.0271)},
    {"name": "context_precision", "delta": -0.0410, "ci": (-0.0655, -0.0166)},
]
SLICES = [
    {"name": "inference",  "n": 88, "delta": 0.035, "ci": (0.012, 0.058)},
    {"name": "comparison", "n": 54, "delta": -0.070, "ci": (-0.118, -0.022)},
    {"name": "temporal",   "n": 41, "delta": 0.010, "ci": (-0.050, 0.070)},
    {"name": "null",       "n": 24, "delta": 0.000, "ci": (-0.090, 0.090)},
]
CLEAN = [METRICS[0], METRICS[1]]
CLEAN_SLICES = [SLICES[0], SLICES[2], SLICES[3]]


def small_slices_are_skipped(m):
    expect(m.slice_verdict(SLICES[3]) == "skipped",
           f"n=24 is below the minimum, so it is reported not gated; got "
           f"{m.slice_verdict(SLICES[3])!r}. Gating a tiny slice fails on noise, and a gate "
           "that false-positives gets disabled")
    expect(m.slice_verdict(SLICES[1]) == "regression",
           f"n=54 with CI [-0.118, -0.022] is a real regression; got {m.slice_verdict(SLICES[1])!r}")


def band_is_not_regression(m):
    expect(m.slice_verdict(SLICES[2]) == "band",
           f"an interval straddling zero is 'band', not a regression; got {m.slice_verdict(SLICES[2])!r}")


def unregistered_primary_blocks(m):
    got = m.evaluate_gate("evidence_recall", CLEAN, CLEAN_SLICES,
                          pre_registered=None, cost_delta_pct=0.0)
    expect(got["ship"] is False, "an unregistered primary metric must block")
    expect("pre-registered" in got["reason"], f"reason should name pre-registration, got {got['reason']!r}")


def the_worked_run_is_blocked(m):
    got = m.evaluate_gate("evidence_recall", METRICS, SLICES,
                          pre_registered="evidence_recall", cost_delta_pct=55.0)
    expect(got["ship"] is False, "this run must not ship")
    expect("context_precision" in got["reason"],
           f"the FIRST blocker in order is the secondary regression on context_precision; "
           f"got {got['reason']!r}")
    return Measured(f"blocked: {got['reason']}")


def clean_run_ships(m):
    got = m.evaluate_gate("evidence_recall", CLEAN, CLEAN_SLICES,
                          pre_registered="evidence_recall", cost_delta_pct=5.0)
    expect(got["ship"] is True, f"a clean run should ship; got {got['reason']!r}")
    expect(got["skipped_slices"] == ["null"],
           f"the n=24 slice must still be reported as skipped even on a shipping run; "
           f"got {got['skipped_slices']}")
    return Measured("ships, with 1 slice reported as too small to gate on")


def slice_regression_blocks(m):
    """Hidden: a slice alone blocks, even with every aggregate clean."""
    got = m.evaluate_gate("evidence_recall", CLEAN, SLICES,
                          pre_registered="evidence_recall", cost_delta_pct=0.0)
    expect(got["ship"] is False, "a slice regression alone must block")
    expect("comparison" in got["reason"],
           f"reason should name the failing slice; got {got['reason']!r}")


def cost_blocks_a_quality_win(m):
    """Hidden: a win you cannot afford is not a win."""
    got = m.evaluate_gate("evidence_recall", CLEAN, CLEAN_SLICES,
                          pre_registered="evidence_recall", cost_delta_pct=55.0)
    expect(got["ship"] is False, "+55% cost against a 25% budget must block")
    expect("cost" in got["reason"], f"reason should name cost; got {got['reason']!r}")


def band_on_primary_blocks(m):
    """Hidden: the primary metric has to actually clear."""
    got = m.evaluate_gate("full_chain_recall", METRICS[:2], CLEAN_SLICES,
                          pre_registered="full_chain_recall", cost_delta_pct=0.0)
    expect(got["ship"] is False, "a primary metric inside the band has not cleared")
    expect("noise band" in got["reason"], f"got {got['reason']!r}")


def missing_primary_blocks(m):
    """Hidden: you cannot ship on a metric you did not measure."""
    got = m.evaluate_gate("ndcg", CLEAN, CLEAN_SLICES,
                          pre_registered="ndcg", cost_delta_pct=0.0)
    expect(got["ship"] is False, "a primary metric that was never measured must block")


def record_is_auditable(m):
    """Hidden: the artefact, not just the verdict."""
    gate = m.evaluate_gate("evidence_recall", METRICS, SLICES,
                           pre_registered="evidence_recall", cost_delta_pct=55.0)
    doc = m.decision_record(gate, "evidence_recall", METRICS)
    expect(doc.startswith("# Release decision: BLOCKED"),
           f"the first line must state the decision; got {doc.splitlines()[0]!r}")
    for metric in METRICS:
        expect(metric["name"] in doc,
               f"every measured metric must appear, cleared or not — {metric['name']} is missing")
    expect("+0.0281" in doc or "0.0281" in doc, "deltas must appear in the record")
    expect("null" in doc, "the skipped slice must be named — a silently ignored slice reads as covered")
    return Measured(f"decision record is {len(doc.splitlines())} lines, all 3 metrics reported")


CHECKS = [
    Check("slices below the minimum are skipped", "Gating noise disables gates", small_slices_are_skipped),
    Check("'band' is not 'regression'", "Do not block correct changes", band_is_not_regression),
    Check("an unregistered primary blocks", "The whole defence", unregistered_primary_blocks),
    Check("the worked run is blocked", "Stops at the first blocker", the_worked_run_is_blocked),
    Check("a clean run ships and still reports skips", "Silence reads as coverage", clean_run_ships),
    Check("a slice regression alone blocks", "Aggregates hide minority failures", slice_regression_blocks, public=False),
    Check("cost blocks a quality win", "A win you cannot afford", cost_blocks_a_quality_win, public=False),
    Check("a primary inside the band blocks", "Clearing is required", band_on_primary_blocks, public=False),
    Check("an unmeasured primary blocks", "Cannot ship on what you did not measure", missing_primary_blocks, public=False),
    Check("the decision record is auditable", "The PDLC artefact", record_is_auditable, public=False),
]
