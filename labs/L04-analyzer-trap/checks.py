from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

CHUNKS = [
    "ERR_CONN_RESET occurred during the post-mortem.",
    "See docs/adr for the decision; version v2.1.4 shipped.",
    "The acl_group_id was wrong at 12:04:31.",
    "Plain prose with nothing special in it.",
]


def census_counts_chunks(m):
    got = m.separator_census(CHUNKS)
    expect(got.get("_") == 2, f"'_' appears in 2 chunks, got {got.get('_')}")
    expect(got.get(".") == 4, f"every chunk here ends with a period, so 4; got {got.get('.')}")
    expect(" " not in got, "whitespace should not be counted as a separator")
    return Measured("census: " + ", ".join(f"{k}×{v}" for k, v in sorted(got.items())))


def keeps_identifiers_whole(m):
    got = m.analyzer_tokenize("ERR_CONN_RESET timed out.")
    expect("err_conn_reset" in got,
           f"expected 'err_conn_reset' as one token, got {got}. Splitting on '_' gives three "
           "terms that appear in every incident report — IDF near zero, matches everything")
    expect(got == ["err_conn_reset", "timed", "out"], f"expected 3 tokens, got {got}")


def still_splits_on_period(m):
    got = m.analyzer_tokenize("version v2.1.4 shipped")
    expect("v2.1.4" not in got,
           "'.' must NOT be a token char. Keeping it gains 208 chunks of version strings and "
           "loses sentence boundaries across ~2,400 — a measured regression of −0.125 recall")
    expect("shipped" in got, f"'shipped' should survive, got {got}")


def hyphen_and_slash_survive(m):
    got = m.analyzer_tokenize("the post-mortem is in docs/adr")
    expect("post-mortem" in got, f"'post-mortem' should be one token, got {got}")
    expect("docs/adr" in got, f"'docs/adr' should be one token, got {got}")


def strips_trailing_token_chars(m):
    """Hidden: prose punctuation must not leak into terms."""
    got = m.analyzer_tokenize("wait - then go, and stop -")
    expect(all(t.strip("_-/") == t for t in got),
           f"tokens must not begin or end with a token char, got {got}")
    expect("-" not in got, f"a bare separator became a token: {got}")


def empty_and_symbol_only(m):
    """Hidden: degenerate input."""
    for text in ["", "   ", "___", "---", "!!!"]:
        got = m.analyzer_tokenize(text)
        expect(isinstance(got, list), f"tokenize({text!r}) returned {type(got).__name__}")
        expect(all(t for t in got), f"tokenize({text!r}) produced an empty token: {got}")


def token_chars_are_configurable(m):
    """Hidden: the decision must be a parameter, not baked in."""
    got = m.analyzer_tokenize("v2.1.4", token_chars="_-/.")
    expect("v2.1.4" in got,
           f"with '.' added to token_chars, 'v2.1.4' should survive whole, got {got}. "
           "The separator set has to be a decision someone can change and measure")


def idf_consequence(m):
    """Hidden: connect the tokenizer to the scoring, which is the whole point."""
    corpus = [f"incident {i}: connection err reset timeout" for i in range(50)]
    corpus.append("ERR_CONN_RESET root cause identified")
    df = {}
    for doc in corpus:
        for term in set(m.analyzer_tokenize(doc)):
            df[term] = df.get(term, 0) + 1
    expect(df.get("err_conn_reset") == 1,
           f"'err_conn_reset' should have df 1 in this corpus, got {df.get('err_conn_reset')}")
    expect(df.get("err", 0) >= 50,
           f"the shredded token 'err' should appear in 50+ documents, got {df.get('err')}")
    return Measured("df: err_conn_reset=1 (specific) vs err=50 (useless) — same 51 documents")


CHECKS = [
    Check("census counts chunks, not occurrences", "Blast radius", census_counts_chunks),
    Check("identifiers survive as one token", "The bug from #1", keeps_identifiers_whole),
    Check("'.' still splits", "The trade you chose not to make", still_splits_on_period),
    Check("'-' and '/' survive", "The two that pay", hyphen_and_slash_survive),
    Check("tokens do not keep trailing separators", "Prose punctuation leaks", strips_trailing_token_chars, public=False),
    Check("degenerate input yields no empty tokens", "Symbols only", empty_and_symbol_only, public=False),
    Check("the separator set is configurable", "A decision, not a constant", token_chars_are_configurable, public=False),
    Check("tokenization changes df, and so IDF", "L03 meets L04", idf_consequence, public=False),
]
