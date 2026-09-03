#!/usr/bin/env python3
"""L.A.B. simulator — the command line a learner actually uses.

    python scripts/lab.py list                 every lab, grouped by track
    python scripts/lab.py next                 what you can start right now
    python scripts/lab.py status               how far through you are
    python scripts/lab.py run L03              public checks for one lab
    python scripts/lab.py run L03 --hidden     everything, including hidden checks
    python scripts/lab.py verify               the pathway is a valid DAG

Progress is derived, never stored. `status` runs the checks and reports what
passes, so there is no progress file to drift out of sync with the code and no
way to mark something complete that does not actually work.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from labs import _harness, _registry  # noqa: E402

GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def _load_module(path: pathlib.Path, name: str):
    return _harness.load_solution(path, name)


def _checks_for(lab: _registry.Lab) -> list[_harness.Check]:
    return _load_module(lab.path / "checks.py", f"checks_{lab.id}").CHECKS


def _run_one(lab: _registry.Lab, hidden: bool) -> list[_harness.Result]:
    checks = _checks_for(lab)
    try:
        solution = _harness.try_load(lab.path / "starter.py", f"starter_{lab.id}")
    except _harness.ImportFailed as exc:
        return _harness.import_failure(checks, exc, include_hidden=hidden)
    return _harness.run_checks(solution, checks, include_hidden=hidden)


def _resolve(labs: dict, token: str) -> _registry.Lab | None:
    """Accept L01, l01, the directory name, or any path inside a lab.

    The editor tasks pass ${fileDirname}, which is a full path, and a learner
    types L01. Both should work rather than one being the "real" way.
    """
    token = token.strip().rstrip("/")
    direct = labs.get(token.upper())
    if direct:
        return direct
    tail = pathlib.Path(token).name or token
    for lab in labs.values():
        if lab.dirname == tail or lab.id.lower() == tail.lower():
            return lab
    # a path deeper inside a lab, e.g. labs/L01-.../starter.py
    for part in reversed(pathlib.Path(token).parts):
        for lab in labs.values():
            if lab.dirname == part:
                return lab
    return None


def _passing(lab: _registry.Lab) -> bool:
    try:
        return all(r.passed for r in _run_one(lab, hidden=True))
    except Exception:
        return False


def cmd_list(args) -> int:
    labs = _registry.load()
    for track, name in _registry.TRACKS.items():
        in_track = [x for x in labs.values() if x.track == track]
        if not in_track:
            continue
        stage, artefact = _registry.PDLC[track]
        print(f"\n{BOLD}{track} · {name}{RESET}  {DIM}— {stage}: {artefact}{RESET}")
        for lab in sorted(in_track, key=lambda x: (x.kind != "challenge", x.id)):
            gate = f"{DIM}needs {','.join(lab.prereqs)}{RESET}" if lab.prereqs else ""
            tag = f"{DIM}[{lab.format}]{RESET} " if lab.kind == "challenge" else ""
            print(f"  {lab.badge} {lab.id}  {tag}{lab.title:<50} {lab.minutes:>3}m  {gate}")
    print(f"\n{len(labs)} labs")
    return 0


def cmd_next(args) -> int:
    labs = _registry.load()
    done = {i for i, lab in labs.items() if _passing(lab)}
    # Challenges first: they are the on-ramp, 5-15 minutes, and unlock a lab.
    ready = sorted(_registry.unlocked(labs, done),
                   key=lambda x: (x.kind != "challenge", x.track, x.id))
    if not ready:
        print("Everything unlocked is done. Nice.")
        return 0
    print(f"{BOLD}Ready to start{RESET}  {DIM}(prerequisites satisfied){RESET}\n")
    for lab in ready[:8]:
        tag = f"{DIM}[{lab.format}]{RESET} " if lab.kind == "challenge" else ""
        print(f"  {lab.badge} {lab.id}  {tag}{lab.title:<50} {lab.minutes:>3}m")
        print(f"     {DIM}{lab.concept}{RESET}")
    return 0


def cmd_status(args) -> int:
    labs = _registry.load()
    done = {i for i, lab in labs.items() if _passing(lab)}
    for track, name in _registry.TRACKS.items():
        in_track = [x for x in labs.values() if x.track == track]
        if not in_track:
            continue
        got = sum(1 for x in in_track if x.id in done)
        bar = "█" * got + "·" * (len(in_track) - got)
        print(f"  {track}  {bar:<12} {got}/{len(in_track)}  {name}")
    print(f"\n  {BOLD}{len(done)}/{len(labs)}{RESET} labs passing")
    return 0


def cmd_run(args) -> int:
    labs = _registry.load()
    lab = _resolve(labs, args.lab_id)
    if lab is None:
        print(f"No lab {args.lab_id!r}. Try: python scripts/lab.py list")
        return 2
    missing = [p for p in lab.prereqs if not _passing(labs[p])]
    if missing and not args.force:
        print(f"{lab.id} expects {', '.join(missing)} first. Use --force to run anyway.")
        return 2

    results = _run_one(lab, hidden=args.hidden)
    print(f"\n{BOLD}{lab.id} · {lab.title}{RESET}\n")
    for r in results:
        mark = f"{GREEN}pass{RESET}" if r.passed else f"{RED}FAIL{RESET}"
        print(f"  {mark}  {r.name}")
        if r.measure:
            print(f"        {DIM}{r.measure}{RESET}")
        if not r.passed and r.detail:
            print(f"        {r.detail}")
    ok = sum(1 for r in results if r.passed)
    scope = "all checks" if args.hidden else "public checks"
    print(f"\n  {ok}/{len(results)} {scope}")
    if ok == len(results) and not args.hidden:
        print(f"  {DIM}Now run with --hidden. The public checks are the ones you"
              f" were told about.{RESET}")
    return 0 if ok == len(results) else 1


def cmd_index(args) -> int:
    """Regenerate labs/README.md from the registry, so it cannot drift."""
    labs = _registry.load()
    out = [
        "# L.A.B. simulator",
        "",
        "**L**ook · **A**ttribute · **B**uild — one loop, eight tracks.",
        "",
        "Two sizes. **Challenges** (`C`) are 5–15 minutes and one mechanism each, in four",
        "shapes — `implement`, `fill` (blanks), `fix` (a planted bug), `predict` (submit the",
        "number). Finishing one points you at the **lab** (`L`) it unlocks: 15–50 minutes,",
        "a real decision, and public plus hidden checks.",
        "",
        "Read [the method](../docs/80-lab/README.md) first. Then:",
        "",
        "```bash",
        "python scripts/lab.py next        # what you can start now",
        "python scripts/lab.py run L01     # public checks",
        "python scripts/lab.py run L01 --hidden",
        "python scripts/lab.py status      # how far through you are",
        "```",
        "",
        "Difficulty: 🟢 easy · 🟡 medium · 🔴 hard · ⚫ boss (a track capstone)",
        "",
    ]
    for track, name in _registry.TRACKS.items():
        in_track = sorted([x for x in labs.values() if x.track == track], key=lambda x: x.id)
        if not in_track:
            continue
        stage, artefact = _registry.PDLC[track]
        out += [f"## {track} · {name}", "",
                f"**{stage}** — hands on {artefact}.", "",
                "| | Item | Format | | Time | After |", "|---|---|---|---|---:|---|"]
        for lab in sorted(in_track, key=lambda x: (x.kind != "challenge", x.id)):
            after = ", ".join(f"`{p}`" for p in lab.prereqs) or "—"
            fmt = lab.format if lab.kind == "challenge" else "lab"
            out.append(f"| {lab.badge} | [`{lab.id}`]({lab.dirname}/brief.md) | {fmt} "
                       f"| {lab.title} | {lab.minutes}m | {after} |")
        out.append("")
    minutes = sum(x.minutes for x in labs.values())
    footer = (f"{len(labs)} labs · {minutes} minutes of work · "
              "every reference solution is tested against its own checks in CI.")
    out += ["---", "", footer, ""]
    (_registry.LABS_DIR / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote labs/README.md ({len(labs)} labs)")
    return 0


def cmd_welcome(args) -> int:
    """The greeting a Codespace shows on attach.

    Deliberately short. A wall of text on first attach is scrolled past, and the
    only thing a learner needs at that moment is the next command.
    """
    labs = _registry.load()
    done = {i for i, lab in labs.items() if _passing(lab)}
    ready = sorted(_registry.unlocked(labs, done), key=lambda x: (x.track, x.id))

    print(f"\n  {BOLD}nanorag · L.A.B. simulator{RESET}   "
          f"{DIM}Look · Attribute · Build{RESET}\n")
    if done:
        print(f"  {GREEN}{len(done)}/{len(labs)}{RESET} labs passing.\n")
    else:
        print(f"  {len(labs)} labs, {len(_registry.TRACKS)} tracks. "
              f"{DIM}Nothing passing yet -- that is the starting state.{RESET}\n")

    for lab in ready[:3]:
        print(f"    {lab.badge} {BOLD}{lab.id}{RESET}  {lab.title}")
        print(f"       {DIM}{lab.concept}{RESET}")
    if not ready:
        print("    Everything unlocked is done.")

    nxt = ready[0].id if ready else "L01"
    print(f"""
  {BOLD}open it{RESET}          python scripts/lab.py open {nxt}
  {BOLD}check your work{RESET}  python scripts/lab.py run {nxt}
  {BOLD}then{RESET}             python scripts/lab.py run {nxt} --hidden
  {DIM}everything else  python scripts/lab.py list | status | next{RESET}

  {DIM}In the editor: Ctrl/Cmd+Shift+B runs the lab you are looking at.{RESET}
""")
    return 0


def cmd_open(args) -> int:
    """Open a lab's brief and starter side by side.

    Recreates the two-pane shape of a problem site: the brief rendered on the
    left, the file you edit on the right. Falls back to printing the paths when
    the `code` CLI is not on PATH, which is the case outside an editor.
    """
    labs = _registry.load()
    lab = _resolve(labs, args.lab_id)
    if lab is None:
        print(f"No lab {args.lab_id!r}. Try: python scripts/lab.py list")
        return 2

    brief, starter = lab.path / "brief.md", lab.path / "starter.py"
    if shutil.which("code"):
        subprocess.run(["code", "--reuse-window", str(starter)], check=False)
        subprocess.run(["code", "--reuse-window", "--command",
                        "markdown.showPreviewToSide", str(brief)], check=False)
        # the --command form is not supported by every build; open it either way
        subprocess.run(["code", "--reuse-window", str(brief)], check=False)
        print(f"opened {lab.id} -- brief and starter")
    else:
        print(f"\n  {BOLD}{lab.id} · {lab.title}{RESET}\n")
        print(f"  brief    {brief}")
        print(f"  edit     {starter}")
        print(f"  check    python scripts/lab.py run {lab.id}\n")
    return 0


def cmd_verify(args) -> int:
    labs = _registry.load()
    problems = _registry.validate(labs)
    if problems:
        print("Pathway problems:", *problems, sep="\n  ")
        return 1
    print(f"pathway is a valid DAG — {len(labs)} labs, no cycles, no dangling prerequisites")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="L.A.B. simulator")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("next").set_defaults(fn=cmd_next)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    sub.add_parser("welcome").set_defaults(fn=cmd_welcome)
    op = sub.add_parser("open")
    op.add_argument("lab_id")
    op.set_defaults(fn=cmd_open)
    run = sub.add_parser("run")
    run.add_argument("lab_id")
    run.add_argument("--hidden", action="store_true", help="include hidden checks")
    run.add_argument("--force", action="store_true", help="run despite unmet prerequisites")
    run.set_defaults(fn=cmd_run)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
