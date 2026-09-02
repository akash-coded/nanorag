"""No multi-line string literal inside a list literal, anywhere in scripts/ or labs/.

    out += [
        "one string that wraps "
        "onto the next line",      # one element, or two with a comma missing?
    ]

Those two forms are indistinguishable by eye, and the failure is silent: two
entries become one and a line vanishes from rendered output. CodeQL flags it
after the push and blocks the merge; this catches it before the push. It has
shipped twice from this repository already, which is why it is a test and not a
note in a style guide.
"""
from __future__ import annotations

import ast
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(list((ROOT / "scripts").glob("*.py")) + list((ROOT / "labs").glob("**/*.py")))


def _offenders(path: pathlib.Path) -> list[tuple[int, int]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [
        (el.lineno, el.end_lineno)
        for node in ast.walk(tree) if isinstance(node, ast.List)
        for el in node.elts
        if isinstance(el, (ast.Constant, ast.JoinedStr)) and el.end_lineno > el.lineno
    ]


@pytest.mark.parametrize("path", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_no_multiline_string_inside_list_literal(path):
    found = _offenders(path)
    assert not found, (
        f"{path.relative_to(ROOT)} has a string literal spanning lines "
        + ", ".join(f"{a}-{b}" for a, b in found)
        + " inside a list literal. Name it before the list so a missing comma cannot"
          " silently merge two entries.")
