from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402


def identifier_survives(m):
    got = m.tokenize("ERR_CONN_RESET occurred")
    expect("err_conn_reset" in got,
           f"got {got}. The identifier was shredded into terms present in every report; "
           "find the line that turns '_' into a separator")
    return Measured("err_conn_reset is one term — df goes from 1,842 to 3")


def prose_still_splits(m):
    got = m.tokenize("The service restarted, twice.")
    expect(got == ["the", "service", "restarted", "twice"], f"prose should still split on punctuation: {got}")


def hyphen_kept(m):
    got = m.tokenize("post-mortem")
    expect(got == ["post-mortem"], f"'-' belongs inside an identifier here: {got}")


def lowercases(m):
    expect(m.tokenize("Reset") == ["reset"], "tokens must be lowercased")


def minimal_change(m):
    """Hidden: the fix is a deletion, not a rewrite."""
    src = pathlib.Path(m.__file__).read_text(encoding="utf-8")
    expect('_SPLIT = re.compile(r"[^a-z0-9_-]+")' in src,
           "the character class was correct; the bug was elsewhere. Put _SPLIT back")


def mixed_identifier_and_prose(m):
    """Hidden."""
    got = m.tokenize("Saw ERR_CONN_RESET at 12:04, then acl_group_id changed.")
    expect("err_conn_reset" in got and "acl_group_id" in got, f"both identifiers must survive: {got}")
    expect("12" in got and "04" in got, f"':' should still split a timestamp: {got}")


CHECKS = [
    Check("ERR_CONN_RESET survives as one term", "The symptom", identifier_survives),
    Check("prose still splits on punctuation", "Do not over-fix", prose_still_splits),
    Check("hyphenated words stay whole", "'-' is in the class on purpose", hyphen_kept),
    Check("lowercases", "Case is not signal here", lowercases),
    Check("the fix is minimal", "One line was wrong", minimal_change, public=False),
    Check("identifiers and prose together", "Real text", mixed_identifier_and_prose, public=False),
]
