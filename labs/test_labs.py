"""Every lab's reference solution must pass every one of its own checks.

This is the test that keeps the labs honest. A lab whose reference solution
fails its own hidden checks is a lab that cannot be completed, and a learner who
hits one loses an hour deciding whether they or the lab is wrong.

It also asserts the inverse: the starter must NOT pass. A starter that already
passes is a lab with nothing in it.
"""
from __future__ import annotations

import pathlib

import pytest

from labs import _harness, _registry

LABS = _registry.load()


def _load(path: pathlib.Path, name: str):
    return _harness.load_solution(path, name)


def test_pathway_is_a_valid_dag():
    problems = _registry.validate(LABS)
    assert not problems, "\n".join(problems)


def test_at_least_one_lab_exists():
    assert LABS, "no labs found — labs/L*/meta.json is empty"


@pytest.mark.parametrize("lab_id", sorted(LABS))
def test_lab_has_the_expected_files(lab_id):
    lab = LABS[lab_id]
    for name in ("brief.md", "starter.py", "reference.py", "checks.py", "meta.json"):
        assert (lab.path / name).exists(), f"{lab_id} is missing {name}"


@pytest.mark.parametrize("lab_id", sorted(LABS))
def test_reference_passes_all_checks(lab_id):
    lab = LABS[lab_id]
    checks = _load(lab.path / "checks.py", f"c_{lab_id}").CHECKS
    reference = _load(lab.path / "reference.py", f"r_{lab_id}")
    results = _harness.run_checks(reference, checks, include_hidden=True)
    failed = [f"{r.name}: {r.detail}" for r in results if not r.passed]
    assert not failed, (f"{lab_id} reference solution fails its own checks:\n  "
                        + "\n  ".join(failed))


@pytest.mark.parametrize("lab_id", sorted(LABS))
def test_starter_does_not_already_pass(lab_id):
    lab = LABS[lab_id]
    checks = _load(lab.path / "checks.py", f"cs_{lab_id}").CHECKS
    try:
        starter = _harness.try_load(lab.path / "starter.py", f"s_{lab_id}")
    except _harness.ImportFailed:
        return  # a starter that cannot import certainly does not pass
    results = _harness.run_checks(starter, checks, include_hidden=True)
    assert not all(r.passed for r in results), (
        f"{lab_id} starter passes every check — there is nothing to do in this lab")


@pytest.mark.parametrize("lab_id", sorted(i for i, x in LABS.items() if x.format == "fill"))
def test_fill_starter_imports_with_blanks_unfilled(lab_id):
    """A ____ inside a module-level expression -- re.escape(____), "a" + ____ --
    runs at import and no check ever gets to explain it. Blanks belong in bare
    assignments or inside function bodies, where a check can name the blank."""
    lab = LABS[lab_id]
    try:
        _harness.try_load(lab.path / "starter.py", f"fill_{lab_id}")
    except _harness.ImportFailed as exc:
        pytest.fail(f"{lab_id} is fill-format but its blanks are used at import time: {exc}. "
                    "Move the expression that uses the blank inside a function.")


@pytest.mark.parametrize("lab_id", sorted(LABS))
def test_lab_has_public_and_hidden_checks(lab_id):
    lab = LABS[lab_id]
    checks = _load(lab.path / "checks.py", f"ch_{lab_id}").CHECKS
    assert any(c.public for c in checks), f"{lab_id} has no public checks"
    assert any(not c.public for c in checks), (
        f"{lab_id} has no hidden checks — the gap between public and hidden is the lesson")
