#!/usr/bin/env python3
"""Review a lab solution posted in a discussion comment, without executing it.

WHY THIS DOES NOT RUN THE CODE
------------------------------
Anyone can comment on a public discussion. A workflow that executes code from a
comment is remote code execution on your CI runner: the job can mine, scan, or
use whatever credentials are in its environment. No amount of `permissions:`
tightening changes that the code ran.

So this reviews the submission **statically**, using Python's own AST, and then
routes the learner to the path where code genuinely is executed safely -- a pull
request, where `labs.yml` already runs the real checks against a branch that had
to be pushed by someone with an account.

What a static review can honestly tell you:

  * whether the required functions exist, with the right names and arity
  * whether the solution hardcodes the expected answer instead of computing it
  * whether it reaches for something the lab forbids
  * whether a write-up carries numbers and an interval, where the lab asks for one

That is most of the feedback a first submission needs, and it arrives in seconds.

    python scripts/lab_submission.py --lab L01 --comment-file body.md
"""
from __future__ import annotations

import argparse
import ast
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from labs import _registry  # noqa: E402

CODE_BLOCK = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)
INTERVAL = re.compile(r"(CI\s*\[|95%|±|\[\s*[-+]?\d*\.\d+\s*,\s*[-+]?\d*\.\d+\s*\])")
NUMBER = re.compile(r"\d+\.\d+")

# Names a lab solution has no business touching. Not a security boundary -- the
# code is never run -- but reaching for these usually means the submission is
# solving a different problem than the one asked.
SUSPICIOUS = {"eval", "exec", "compile", "__import__", "open", "input"}
SUSPICIOUS_MODULES = {"os", "sys", "subprocess", "socket", "requests", "urllib", "shutil"}


def extract_code(body: str) -> str | None:
    blocks = CODE_BLOCK.findall(body)
    if not blocks:
        return None
    # The largest block is the submission; smaller ones are usually output pasted
    # alongside it.
    return max(blocks, key=len)


def required_functions(lab: _registry.Lab) -> list[str]:
    """The function names the starter defines, which are what checks call."""
    tree = ast.parse((lab.path / "starter.py").read_text(encoding="utf-8"))
    return [n.name for n in tree.body
            if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]


def review(lab: _registry.Lab, body: str) -> tuple[list[str], list[str], list[str]]:
    """Returns (passed, problems, notes)."""
    passed: list[str] = []
    problems: list[str] = []
    notes: list[str] = []

    code = extract_code(body)
    if code is None:
        problems.append(
            "No code block found. Wrap your solution in a fenced ```python block so it can be "
            "reviewed.")
        return passed, problems, notes

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        problems.append(f"The code does not parse: `{exc.msg}` on line {exc.lineno}.")
        return passed, problems, notes
    passed.append("parses as valid Python")

    defined = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    wanted = required_functions(lab)
    missing = [f for f in wanted if f not in defined]
    if missing:
        problems.append("Missing " + ", ".join(f"`{m}`" for m in missing)
                        + f" — the checks for {lab.id} call " + ", ".join(f"`{w}`" for w in wanted)
                        + ".")
    else:
        passed.append(f"defines all {len(wanted)} required functions")

    if any(isinstance(n, ast.Raise) and getattr(getattr(n.exc, "func", n.exc), "id", "")
           == "NotImplementedError" for n in ast.walk(tree)):
        problems.append("Still raises `NotImplementedError` — this looks like the starter.")

    called = {n.func.id for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    imported = {a.name.split(".")[0] for n in ast.walk(tree)
                if isinstance(n, ast.Import) for a in n.names}
    imported |= {n.module.split(".")[0] for n in ast.walk(tree)
                 if isinstance(n, ast.ImportFrom) and n.module}

    for name in sorted(called & SUSPICIOUS):
        notes.append(f"Calls `{name}`. No lab needs it — worth checking you are solving the "
                     "problem asked.")
    for name in sorted(imported & SUSPICIOUS_MODULES):
        notes.append(f"Imports `{name}`. The labs are pure functions over their arguments.")

    # A solution that returns a literal matching an example in the brief is
    # answering the example rather than the problem.
    literals = [n.value for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 12]
    brief = (lab.path / "brief.md").read_text(encoding="utf-8")
    echoed = [lit for lit in literals if lit in brief]
    if echoed:
        problems.append("Returns a string literal that appears verbatim in the brief — that "
                        "answers the example, not the problem.")

    if not problems:
        passed.append("nothing obviously hardcoded")

    if "measurement" in lab.tags or lab.track in {"T4", "T5", "T6"}:
        if not NUMBER.search(body):
            notes.append("No numbers in the write-up. This lab is about measurement — say what "
                         "you got.")
        elif not INTERVAL.search(body):
            notes.append("Numbers but no interval. A point estimate is not a result.")
        else:
            passed.append("write-up carries numbers with an interval")

    return passed, problems, notes


def render(lab: _registry.Lab, passed, problems, notes) -> str:
    ok = not problems
    head = "✅ **Static review passed**" if ok else "🔎 **Static review — some things to fix**"
    out = [f"{head} · {lab.badge} **{lab.id}** · {lab.title}", ""]

    if passed:
        out += ["**What checks out**", ""]
        out += [f"- {p}" for p in passed] + [""]
    if problems:
        out += ["**What does not**", ""]
        out += [f"- {p}" for p in problems] + [""]
    if notes:
        out += ["**Worth a look**", ""]
        out += [f"- {n}" for n in notes] + [""]

    out += [
        "---",
        "",
        "**This review did not run your code**, and deliberately so — a workflow that executes "
        "code from a public comment is remote code execution on the runner. It read your "
        "submission with Python's AST instead.",
        "",
        "**To have the real checks run it**, including the hidden ones:",
        "",
        "```bash",
        "# in a Codespace or a clone",
        f"python scripts/lab.py run {lab.id} --hidden",
        "```",
        "",
        "or push it and open a pull request — "
        "[`labs.yml`](https://github.com/akash-coded/nanorag/blob/main/.github/workflows/labs.yml) "
        "evaluates the lab and comments with a full result table.",
        "",
        f"<sub>Posted by the lab submission workflow · "
        f"[brief](https://github.com/akash-coded/nanorag/blob/main/labs/{lab.dirname}/brief.md)"
        f"</sub>",
        "<!-- lab-submission-review -->",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", required=True)
    ap.add_argument("--comment-file", required=True, type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    labs = _registry.load()
    lab = labs.get(args.lab.upper())
    if lab is None:
        print(f"unknown lab {args.lab!r}", file=sys.stderr)
        return 2

    body = args.comment_file.read_text(encoding="utf-8")
    text = render(lab, *review(lab, body))
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
