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
import json
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

    # Built as named strings rather than wrapped literals inside the list: implicit
    # concatenation in a list is the pattern where one missing comma silently merges
    # two entries, and CodeQL is right to flag it even when it is deliberate.
    why_not_run = (
        "**This review did not run your code**, and deliberately so — a workflow that executes"
        " code from a public comment is remote code execution on the runner. It read your"
        " submission with Python's AST instead."
    )
    labs_yml = "https://github.com/akash-coded/nanorag/blob/main/.github/workflows/labs.yml"
    pr_route = (
        f"or push it and open a pull request — [`labs.yml`]({labs_yml}) evaluates the lab and"
        " comments with a full result table."
    )
    brief_url = f"https://github.com/akash-coded/nanorag/blob/main/labs/{lab.dirname}/brief.md"
    footer = f"<sub>Posted by the lab submission workflow · [brief]({brief_url})</sub>"

    out += [
        "---",
        "",
        why_not_run,
        "",
        "**To have the real checks run it**, including the hidden ones:",
        "",
        "```bash",
        "# in a Codespace or a clone",
        f"python scripts/lab.py run {lab.id} --hidden",
        "```",
        "",
        pr_route,
        "",
        footer,
        "<!-- lab-submission-review -->",
    ]
    return "\n".join(out)


def _next_line(labs: dict, lab: _registry.Lab, passed_all: bool) -> str:
    """The one sentence a learner most needs after a result, and the reason."""
    done = {lab.id} if passed_all else set()
    nxt = _registry.next_after(labs, lab.id, done) if passed_all else None
    if not passed_all:
        return (f"**Next:** the checks above, then `python scripts/lab.py run {lab.id}"
                " --hidden`. Re-post here when it passes — every attempt is counted, not"
                " only the first.")
    if nxt is None:
        return ("**Next:** nothing left in this track. Pick another with"
                " `python scripts/lab.py next`.")
    fmt = f" · {nxt.format}" if nxt.kind == "challenge" else ""
    return (f"**Next:** {nxt.badge} **{nxt.id}** · {nxt.title} ({nxt.minutes} min{fmt}) — "
            f"{nxt.concept}")


def render_report(report: dict) -> str:
    """Turn a sandbox JSON report into the reply a learner reads.

    Nothing here is a template sentence. Every line comes from data that exists
    per lab -- the check's own failure message, the meta.json skill line, the
    deeper link, the DAG -- so two labs never produce the same paragraph.
    """
    labs = _registry.load()
    lab = labs.get(report.get("lab", "").upper())
    if "error" in report or lab is None:
        return (f"⚠️ The sandbox could not evaluate this: "
                f"`{report.get('error', 'unknown lab')}`.\n\n"
                "If it was a timeout, something in your solution never returns -- a check"
                " gets 25 seconds. <!-- lab-submission-review -->")

    passed, total = report["passed"], report["total"]
    ok = passed == total
    head = "✅" if ok else ("🟡" if passed >= total // 2 else "🔎")
    out = [f"### {head} {lab.badge} {lab.id} · {lab.title} — **{passed}/{total} checks**", ""]

    hits = [r for r in report["results"] if r["passed"]]
    misses = [r for r in report["results"] if not r["passed"]]
    if hits:
        out.append("**Passed:** " + " · ".join(r["name"] for r in hits))
        measures = [r["measure"] for r in hits if r["measure"]]
        if measures:
            out.append("")
            out += [f"> {m}" for m in measures[:3]]
    if misses:
        out += ["", "**Missed:**", ""]
        for r in misses:
            tag = "" if r["public"] else " *(hidden)*"
            detail = (r["detail"] or "").replace("\n", " ")
            out.append(f"- **{r['name']}**{tag} — {detail}")
        hidden_only = all(not r["public"] for r in misses)
        if hidden_only:
            gap = ("Every public check passed and a hidden one did not. That is the normal"
                   " experience: the hidden checks cover what the brief left unsaid, and the"
                   " gap is the lesson.")
            out += ["", gap]

    out += ["", f"**What this gave you:** {lab.skill}" if lab.skill else ""]
    if lab.deeper:
        path, _, why = lab.deeper.partition(" -- ")
        url = f"https://github.com/akash-coded/nanorag/blob/main/{path.strip()}"
        out.append(f"**Go deeper:** [{pathlib.Path(path.strip()).name}]({url})"
                   + (f" — {why.strip()}" if why else ""))
    brief = f"https://github.com/akash-coded/nanorag/blob/main/labs/{lab.dirname}/brief.md"
    stamp = (f"<sub>{lab.section} · sandboxed run, no network, no credentials · "
             f"[brief]({brief})</sub>")
    out += ["", _next_line(labs, lab, ok), "", stamp, "<!-- lab-submission-review -->"]
    return "\n".join(x for x in out if x is not None)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab")
    ap.add_argument("--comment-file", type=pathlib.Path)
    ap.add_argument("--report", type=pathlib.Path, help="render a sandbox JSON report instead")
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()

    if args.report:
        text = render_report(json.loads(args.report.read_text(encoding="utf-8")))
        if args.out:
            args.out.write_text(text, encoding="utf-8")
        print(text)
        return 0
    if not (args.lab and args.comment_file):
        ap.error("--lab and --comment-file are required unless --report is given")

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
