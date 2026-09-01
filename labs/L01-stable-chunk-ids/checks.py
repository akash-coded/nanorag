from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

DOC = "incident-4471"
PARAS = [f"Paragraph {i} of the incident report." for i in range(40)]
EDITED = list(PARAS)
EDITED[19] = "Paragraph 19 of the incident summary."   # one word changed


def _ids(m, paras):
    return [m.chunk_id(DOC, i, p) for i, p in enumerate(paras)]


def shape(m):
    got = m.chunk_id("doc-1", 7, "hello world")
    expect(isinstance(got, str), f"chunk_id must return a str, got {type(got).__name__}")
    parts = got.split(":")
    expect(len(parts) == 3,
           f"expected 'doc_id:ordinal:hash8', got {got!r} ({len(parts)} colon-separated parts)")
    expect(parts[0] == "doc-1", f"first part should be the doc_id, got {parts[0]!r}")
    expect(parts[1] == "7", f"second part should be the ordinal, got {parts[1]!r}")
    expect(re.fullmatch(r"[0-9a-f]{8}", parts[2]) is not None,
           f"third part should be 8 lowercase hex chars, got {parts[2]!r}")
    return Measured(f"example id: {got}")


def deterministic(m):
    a = m.chunk_id(DOC, 3, "the same text")
    b = m.chunk_id(DOC, 3, "the same text")
    expect(a == b, "same inputs produced different ids — the hash must not be salted or random")


def edit_changes_exactly_one(m):
    before, after = _ids(m, PARAS), _ids(m, EDITED)
    changed = sum(1 for x, y in zip(before, after) if x != y)
    expect(changed != 0,
           "a one-word edit changed no ids — the chunk text is not part of the id, so the "
           "index would keep a stale vector under a live id and never notice")
    expect(changed == 1,
           f"a one-word edit changed {changed} ids; it should change exactly 1. "
           "More than one means the id depends on something outside the chunk")
    return Measured("1 of 40 ids changed on a one-word edit — 39 chunks skip re-embedding")


def whitespace_is_not_an_edit(m):
    plain = m.chunk_id(DOC, 5, "the quick brown fox")
    respaced = m.chunk_id(DOC, 5, "  the quick\n\tbrown   fox  ")
    expect(plain == respaced,
           "re-extracting the same words with different whitespace produced a different id. "
           "A new PDF extractor would look like a full-document edit")


def position_disambiguates(m):
    """Hidden: identical text at two positions must not collide."""
    a = m.chunk_id(DOC, 4, "This agreement is governed by the laws of England.")
    b = m.chunk_id(DOC, 31, "This agreement is governed by the laws of England.")
    expect(a != b,
           "identical boilerplate at two positions produced the same id. In a contract with "
           "repeated clauses those chunks collide and one is silently lost")


def document_scoped(m):
    """Hidden: the same text in two documents must not collide."""
    a = m.chunk_id("doc-a", 0, "Revenue rose 4% year on year.")
    b = m.chunk_id("doc-b", 0, "Revenue rose 4% year on year.")
    expect(a != b, "the same sentence in two different documents produced the same id")


def empty_and_unicode(m):
    """Hidden: degenerate input must not raise."""
    for text in ["", "   ", "\n\n", "café ☕ naïve", "ERR_CONN_RESET"]:
        got = m.chunk_id("doc-x", 0, text)
        expect(isinstance(got, str) and got.count(":") == 2,
               f"chunk_id({text!r}) returned {got!r}")


def insertion_shifts_ordinals(m):
    """Hidden: this SHOULD change many ids. The lab is about knowing that."""
    inserted = ["A new opening paragraph."] + PARAS
    before, after = _ids(m, PARAS), _ids(m, inserted)[1:]
    changed = sum(1 for x, y in zip(before, after) if x != y)
    expect(changed == len(PARAS),
           "inserting a paragraph at the top should shift every ordinal below it and change "
           f"every id, but only {changed} of {len(PARAS)} changed. If your id ignores the "
           "ordinal it is not position-aware, and identical chunks will collide")
    return Measured("insertion changes all 40 ids — scheme C is stable against edits, not insertions")


CHECKS = [
    Check("id has the shape doc_id:ordinal:hash8", "The format the store expects", shape),
    Check("same input gives the same id", "No salt, no randomness", deterministic),
    Check("a one-word edit changes exactly one id", "The whole point", edit_changes_exactly_one),
    Check("whitespace-only change is not an edit", "Re-extraction must be free", whitespace_is_not_an_edit),
    Check("identical text at two positions differs", "Boilerplate must not collide", position_disambiguates, public=False),
    Check("identical text in two documents differs", "Ids are document-scoped", document_scoped, public=False),
    Check("empty and unicode input do not raise", "Degenerate input is still input", empty_and_unicode, public=False),
    Check("an insertion shifts every ordinal below it", "The known limitation, made visible", insertion_shifts_ordinals, public=False),
]
