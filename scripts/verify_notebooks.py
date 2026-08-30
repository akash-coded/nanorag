#!/usr/bin/env python3
"""Execute every notebook headlessly, report timings and figure counts.

Used by `make notebooks` and by the notebook-smoke CI job. Exits non-zero on the
first cell that raises, and prints the traceback where you can read it.
"""
from __future__ import annotations

import pathlib
import sys
import time

import nbformat
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"


def main(argv: list[str]) -> int:
    targets = [NB_DIR / a for a in argv[1:]] or sorted(NB_DIR.glob("*.ipynb"))
    failures = 0
    print(f"{'notebook':<50} {'status':<10} {'time':>8}  figures")
    print("-" * 82)
    for path in targets:
        nb = nbformat.read(path, as_version=4)
        t0 = time.perf_counter()
        NotebookClient(nb, timeout=900, kernel_name="python3",
                       resources={"metadata": {"path": str(NB_DIR)}},
                       allow_errors=True).execute()
        elapsed = time.perf_counter() - t0
        errs, figs = [], 0
        for cell in nb.cells:
            for out in cell.get("outputs", []):
                if out.get("output_type") == "error":
                    errs.append("".join(out["traceback"])[-2000:])
                if (out.get("data") or {}).get("image/png"):
                    figs += 1
        status = "OK" if not errs else f"{len(errs)} ERROR"
        print(f"{path.name:<50} {status:<10} {elapsed:7.1f}s  {figs}")
        for tb in errs:
            print(tb)
        failures += len(errs)
    print("-" * 82)
    print("all clean" if not failures else f"{failures} failing cell(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
