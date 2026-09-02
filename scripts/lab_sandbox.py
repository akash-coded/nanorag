#!/usr/bin/env python3
"""Run a submission against a lab's checks and emit a JSON report. Stdlib only.

This is the ONLY code that executes a learner's submission, and it is designed to
run inside a container with no network, no writable filesystem beyond /tmp, no
capabilities, and no credentials in the environment. It imports nothing outside
the standard library so it can run in a bare python:3.12-slim image with no
install step -- which is also why every lab is a pure function over its
arguments.

Defence in depth, in order of what fails first:

  1. the container has --network=none; nothing can be exfiltrated
  2. the job that runs the container has `permissions: {}`; there is no token
  3. `docker run --timeout` / `timeout(1)` kills the process
  4. this script ALSO arms SIGALRM, so a busy loop inside one check cannot hang
     the report even if the outer timeout is misconfigured
  5. the report is JSON on stdout; a submission that prints garbage cannot forge
     a result, because the outer job parses the LAST line only, and it is
     prefixed with a sentinel

    python scripts/lab_sandbox.py --lab C03 --submission /tmp/sub.py
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import signal
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from labs import _harness  # noqa: E402

SENTINEL = "@@LAB-REPORT@@"
WALL_SECONDS = 25


def _load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _find_lab(lab_id: str) -> pathlib.Path | None:
    for d in (ROOT / "labs").glob(f"{lab_id.upper()}-*"):
        if (d / "checks.py").exists():
            return d
    return None


def _alarm(_signum, _frame):
    print(SENTINEL + json.dumps({"error": f"timed out after {WALL_SECONDS}s"}))
    sys.stdout.flush()
    sys.exit(3)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", required=True)
    ap.add_argument("--submission", required=True, type=pathlib.Path)
    args = ap.parse_args()

    lab_dir = _find_lab(args.lab)
    if lab_dir is None:
        print(SENTINEL + json.dumps({"error": f"unknown lab {args.lab}"}))
        return 2

    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(WALL_SECONDS)

    checks = _load(lab_dir / "checks.py", "sandbox_checks").CHECKS
    try:
        module = _harness.try_load(args.submission, "sandbox_submission")
        results = _harness.run_checks(module, checks, include_hidden=True)
    except _harness.ImportFailed as exc:
        results = _harness.import_failure(checks, exc, include_hidden=True)

    public = {c.name for c in checks if c.public}
    report = {
        "lab": lab_dir.name.split("-")[0],
        "passed": sum(1 for r in results if r.passed),
        "total": len(results),
        "results": [
            {"name": r.name, "passed": r.passed, "detail": r.detail,
             "measure": r.measure, "public": r.name in public}
            for r in results
        ],
    }
    # Last line, sentinel-prefixed: the outer job ignores everything else the
    # submission may have printed.
    print(SENTINEL + json.dumps(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
