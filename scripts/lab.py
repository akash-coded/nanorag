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
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from labs import _harness, _registry  # noqa: E402

GREEN, RED, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


def _load_module(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _checks_for(lab: _registry.Lab) -> list[_harness.Check]:
    return _load_module(lab.path / "checks.py", f"checks_{lab.id}").CHECKS


def _run_one(lab: _registry.Lab, hidden: bool) -> list[_harness.Result]:
    solution = _load_module(lab.path / "starter.py", f"starter_{lab.id}")
    return _harness.run_checks(solution, _checks_for(lab), include_hidden=hidden)


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
        for lab in sorted(in_track, key=lambda x: x.id):
            gate = f"{DIM}needs {','.join(lab.prereqs)}{RESET}" if lab.prereqs else ""
            print(f"  {lab.badge} {lab.id}  {lab.title:<52} {lab.minutes:>3}m  {gate}")
    print(f"\n{len(labs)} labs")
    return 0


def cmd_next(args) -> int:
    labs = _registry.load()
    done = {i for i, lab in labs.items() if _passing(lab)}
    ready = sorted(_registry.unlocked(labs, done), key=lambda x: (x.track, x.id))
    if not ready:
        print("Everything unlocked is done. Nice.")
        return 0
    print(f"{BOLD}Ready to start{RESET}  {DIM}(prerequisites satisfied){RESET}\n")
    for lab in ready[:8]:
        print(f"  {lab.badge} {lab.id}  {lab.title:<52} {lab.minutes:>3}m")
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
    lab = labs.get(args.lab_id.upper())
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
        "**L**ook · **A**ttribute · **B**uild — one loop, twelve labs, eight tracks.",
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
                "| | Lab | | Time | After |", "|---|---|---|---:|---|"]
        for lab in in_track:
            after = ", ".join(f"`{p}`" for p in lab.prereqs) or "—"
            out.append(f"| {lab.badge} | [`{lab.id}`]({lab.dirname}/brief.md) | {lab.title} "
                       f"| {lab.minutes}m | {after} |")
        out.append("")
    out += ["---", "",
            f"{len(labs)} labs · "
            f"{sum(x.minutes for x in labs.values())} minutes of work · "
            "every reference solution is tested against its own checks in CI.", ""]
    (_registry.LABS_DIR / "README.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote labs/README.md ({len(labs)} labs)")
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
    run = sub.add_parser("run")
    run.add_argument("lab_id")
    run.add_argument("--hidden", action="store_true", help="include hidden checks")
    run.add_argument("--force", action="store_true", help="run despite unmet prerequisites")
    run.set_defaults(fn=cmd_run)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
