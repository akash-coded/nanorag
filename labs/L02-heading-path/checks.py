from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

STACK = [(1, "Household"), (2, "Section 4 — Water damage"), (3, "4.3 Flood")]
BODY = "The excess is £500 per incident."


def joins_the_stack(m):
    got = m.heading_path(STACK)
    expect(got == "Household › Section 4 — Water damage › 4.3 Flood",
           f"expected the three headings joined by ' › ', got {got!r}")
    return Measured(f"path is {len(got)} chars ≈ {len(got)//4} tokens per chunk")


def prepends_to_text(m):
    got = m.chunk_with_path(BODY, STACK)
    expect(isinstance(got, dict), f"expected a dict, got {type(got).__name__}")
    expect(set(got) == {"text", "heading_path"},
           f"expected keys text and heading_path, got {sorted(got)}")
    expect(got["text"].startswith("Household › "),
           "the path must be prepended to the text, not only stored in the column — "
           "a heading in a column is filterable, a heading in the text is retrievable")
    expect(got["text"].endswith(BODY), "the original text must survive intact")
    expect("\n" in got["text"], "path and text must be separated by a newline")


def keeps_the_deepest(m):
    deep = [(i, f"H{i}") for i in range(1, 7)]
    got = m.heading_path(deep, max_depth=4)
    expect(got == "H3 › H4 › H5 › H6",
           f"with max_depth=4 keep the DEEPEST four, expected 'H3 › H4 › H5 › H6', got {got!r}")


def empty_stack_is_clean(m):
    expect(m.heading_path([]) == "", "an empty stack should give an empty path")
    got = m.chunk_with_path(BODY, [])
    expect(got["text"] == BODY,
           f"with no headings the text must be unchanged, got {got['text']!r} — "
           "a leading newline here becomes a leading blank line in every prompt")
    expect(got["heading_path"] == "", "with no headings the path should be ''")


def disambiguates_identical_text(m):
    """Hidden: the same sentence under two headings must differ."""
    a = m.chunk_with_path(BODY, [(1, "Household"), (2, "4.3 Flood")])
    b = m.chunk_with_path(BODY, [(1, "Motor"), (2, "2.1 Accidental damage")])
    expect(a["text"] != b["text"],
           "the same sentence under two different headings produced identical text — "
           "retrieval returns both and nothing tells them apart")


def separator_is_not_a_token(m):
    """Hidden: the separator must not become a searchable term."""
    path = m.heading_path(STACK)
    for bad in ["-", "/", "|", ">"]:
        expect(f" {bad} " not in path,
               f"the separator {bad!r} is in the analyzer's token set, so it becomes a term "
               "in every chunk and dilutes IDF. Use a character the tokenizer drops")


def max_depth_zero(m):
    """Hidden: a degenerate depth must not raise or return the whole stack."""
    got = m.heading_path(STACK, max_depth=0)
    expect(got == "", f"max_depth=0 should give an empty path, got {got!r}")


def shallower_than_max(m):
    """Hidden: a stack shorter than max_depth must not be padded or truncated."""
    got = m.heading_path([(1, "Only")], max_depth=4)
    expect(got == "Only", f"expected 'Only', got {got!r}")


CHECKS = [
    Check("joins the heading stack", "Breadcrumb format", joins_the_stack),
    Check("prepends the path to the text", "Retrievable, not just filterable", prepends_to_text),
    Check("keeps the deepest headings when truncating", "Nearest carries most", keeps_the_deepest),
    Check("no headings leaves the text alone", "No leading blank line", empty_stack_is_clean),
    Check("identical text under different headings differs", "Disambiguation", disambiguates_identical_text, public=False),
    Check("the separator is not a searchable token", "IDF dilution", separator_is_not_a_token, public=False),
    Check("max_depth=0 gives an empty path", "Degenerate input", max_depth_zero, public=False),
    Check("a shallow stack is not padded", "Off-by-one in the slice", shallower_than_max, public=False),
]
