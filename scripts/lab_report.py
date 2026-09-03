#!/usr/bin/env python3
"""Render a lab run as markdown, for CI to post on a pull request.

    python scripts/lab_report.py L01 L05        specific labs
    python scripts/lab_report.py --changed      labs touched by the diff vs main

Public checks run always. Hidden checks run too, because on a pull request the
attempt is already submitted -- the public/hidden split is a pacing device for
someone working locally, not a secret.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from labs import _harness, _registry  # noqa: E402


def _load(path: pathlib.Path, name: str):
    return _harness.load_solution(path, name)


def changed_labs(base: str = "origin/main") -> list[str]:
    diff = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"],
                          capture_output=True, text=True, cwd=ROOT)
    labs = _registry.load()
    touched = set()
    for line in diff.stdout.splitlines():
        for lab in labs.values():
            if line.startswith(f"labs/{lab.dirname}/") and line.endswith("starter.py"):
                touched.add(lab.id)
    return sorted(touched)


def report(lab_ids: list[str]) -> tuple[str, bool]:
    labs = _registry.load()
    if not lab_ids:
        return ("No lab `starter.py` was changed in this pull request, so there is nothing to "
                "evaluate.\n"), True

    lines = ["## L.A.B. simulator", ""]
    all_green = True
    for lab_id in lab_ids:
        lab = labs.get(lab_id)
        if lab is None:
            lines += [f"### {lab_id}", "", f"Unknown lab `{lab_id}`.", ""]
            all_green = False
            continue
        try:
            checks = _load(lab.path / "checks.py", f"c_{lab_id}").CHECKS
            try:
                solution = _harness.try_load(lab.path / "starter.py", f"s_{lab_id}")
                results = _harness.run_checks(solution, checks, include_hidden=True)
            except _harness.ImportFailed as exc:
                results = _harness.import_failure(checks, exc, include_hidden=True)
        except Exception as exc:  # noqa: BLE001
            lines += [f"### {lab.badge} {lab.id} · {lab.title}", "",
                      f"`starter.py` could not be imported: `{type(exc).__name__}: {exc}`", ""]
            all_green = False
            continue

        passed = sum(1 for r in results if r.passed)
        head = "✅" if passed == len(results) else "❌"
        meta = (f"**{passed}/{len(results)} checks** · {lab.minutes} min · "
                f"track {lab.track} · [brief](../blob/main/labs/{lab.dirname}/brief.md)")
        lines += [f"### {head} {lab.badge} {lab.id} · {lab.title}", "", meta, "",
                  "| | Check | Note |", "|---|---|---|"]
        for r in results:
            note = r.measure if r.passed else (r.detail or "")
            note = note.replace("|", "\\|").replace("\n", " ")
            if len(note) > 160:
                note = note[:157] + "..."
            lines.append(f"| {'✅' if r.passed else '❌'} | {r.name} | {note} |")
        lines.append("")
        if passed != len(results):
            all_green = False
            hidden_note = ("> Failing checks include hidden ones, which the brief does not "
                           "describe. The gap between the public and hidden sets is where the "
                           "brief's assumptions were doing work.")
            lines += [hidden_note, ""]

    if all_green:
        done_note = ("All checks pass. The reference solution is in `reference.py` — "
                     "worth reading now, not before.")
        lines += ["---", "", done_note, ""]
    return "\n".join(lines), all_green


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lab_ids", nargs="*")
    ap.add_argument("--changed", action="store_true")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--fail-on-red", action="store_true")
    args = ap.parse_args()

    ids = changed_labs(args.base) if args.changed else [i.upper() for i in args.lab_ids]
    text, green = report(ids)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 1 if (args.fail_on_red and not green) else 0


if __name__ == "__main__":
    sys.exit(main())
