from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

CFG = {"k": 8, "alpha": 0.2, "encoder": "lsa-256", "rerank": "cross"}
CANDS = [{"chunk_id": f"c{i}", "score": 1.0 - i / 10, "method": "hybrid"} for i in range(6)]


def _trace(m, packed, gold):
    return m.build_trace("flood excess?", CFG, CANDS, packed, gold, "The excess is £500.",
                         {"retrieve": 120.0, "rerank": 300.0, "pack": 8.0, "generate": 512.0})


def fingerprint_ignores_key_order(m):
    a = m.config_fingerprint({"k": 8, "alpha": 0.2})
    b = m.config_fingerprint({"alpha": 0.2, "k": 8})
    expect(a == b,
           f"the same config in a different key order fingerprinted differently ({a} vs {b}) — "
           "every dict rebuild would look like a config change")
    expect(len(a) == 8, f"fingerprint should be 8 chars, got {len(a)}")
    return Measured(f"config {a}")


def fingerprint_detects_change(m):
    a = m.config_fingerprint({"k": 8, "alpha": 0.2})
    b = m.config_fingerprint({"k": 8, "alpha": 0.5})
    expect(a != b, "changing alpha must change the fingerprint, or it cannot answer "
                   "'was this the same system?'")


def trace_stores_references(m):
    got = _trace(m, ["c0", "c1"], ["c0"])
    expect(got["candidate_ids"] == [f"c{i}" for i in range(6)],
           f"candidate_ids should be ids in rank order, got {got['candidate_ids']}")
    blob = str(got)
    expect("score" not in blob or "chunk_id" not in blob or len(blob) < 2000,
           "the trace looks like it stores whole candidate dicts — store references, the chunk "
           "text and scores can be re-derived and the trace store should not rival the index")
    expect(got["config_fp"] == m.config_fingerprint(CFG), "config_fp must be the fingerprint")


def k_collapse_is_recorded(m):
    got = _trace(m, ["c0", "c1"], ["c0"])
    expect(got["k_collapse"] == 4,
           f"6 candidates, 2 packed, so k_collapse is 4; got {got['k_collapse']}. This is the "
           "only field that shows a post-retrieval filter eating the result set")
    expect(abs(got["total_ms"] - 940.0) < 1e-6, f"total_ms should be 940.0, got {got['total_ms']}")
    return Measured(f"k_collapse {got['k_collapse']}, total {got['total_ms']:.0f}ms "
                    f"(rerank {got['stage_ms']['rerank']:.0f}ms is the budget)")


def attributes_the_four_verdicts(m):
    miss = _trace(m, ["c0"], ["zzz"])
    expect(m.attribute(miss, False) == "retrieval miss", "gold absent from the pool is a miss")
    loss = _trace(m, ["c0"], ["c0", "c3"])
    expect(m.attribute(loss, False) == "packing loss", "gold in pool, not packed, is packing loss")
    gen = _trace(m, ["c0", "c3"], ["c0", "c3"])
    expect(m.attribute(gen, False) == "generation failure", "gold packed, answer wrong")
    accident = _trace(m, ["c1"], ["c0"])
    expect(m.attribute(accident, True) == "right by accident",
           "a correct answer with the gold never packed is the dangerous verdict — the model "
           "answered from memory and retrieval contributed nothing")


def right_by_accident_beats_the_others(m):
    """Hidden: order of checks matters."""
    t = _trace(m, ["c5"], ["zzz"])
    expect(m.attribute(t, True) == "right by accident",
           "a correct answer whose gold was never even retrieved is still 'right by accident', "
           "not 'retrieval miss' — check the accident case first")


def everything_present_is_ok(m):
    """Hidden: the success path."""
    t = _trace(m, ["c0", "c1"], ["c0"])
    expect(m.attribute(t, True) == "ok", "correct answer with gold packed should be 'ok'")


def fingerprint_handles_nested_and_nonjson(m):
    """Hidden: real configs contain tuples and objects."""
    got = m.config_fingerprint({"filters": {"acl": ("a", "b")}, "k": 8})
    expect(isinstance(got, str) and len(got) == 8,
           f"a nested config with a tuple should still fingerprint, got {got!r}")


def empty_packed_is_total_collapse(m):
    """Hidden: everything filtered out."""
    got = _trace(m, [], ["c0"])
    expect(got["k_collapse"] == 6, f"nothing packed means k_collapse is 6, got {got['k_collapse']}")
    expect(m.attribute(got, False) == "packing loss",
           "gold in the pool and nothing packed is packing loss, not a retrieval miss")


CHECKS = [
    Check("fingerprint ignores key order", "Same system, same hash", fingerprint_ignores_key_order),
    Check("fingerprint detects a changed value", "Different system, different hash", fingerprint_detects_change),
    Check("trace stores references, not copies", "Do not rival the index", trace_stores_references),
    Check("k_collapse and total_ms are recorded", "The field that pays for itself", k_collapse_is_recorded),
    Check("attributes all four verdicts", "A verdict, not a guess", attributes_the_four_verdicts),
    Check("'right by accident' is checked first", "Order matters", right_by_accident_beats_the_others, public=False),
    Check("the success path returns ok", "Not every trace is a failure", everything_present_is_ok, public=False),
    Check("nested and non-JSON config values", "Real configs are messy", fingerprint_handles_nested_and_nonjson, public=False),
    Check("nothing packed is total collapse", "Filter ate everything", empty_packed_is_total_collapse, public=False),
]
