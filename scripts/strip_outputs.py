#!/usr/bin/env python3
"""Strip outputs and execution counts from every committed notebook.

Notebook diffs are unreadable once base64 PNGs are in them, and a reviewer who
cannot read a diff does not review it. Run before committing, or let the
pre-commit hook in CONTRIBUTING.md do it for you.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

changed = 0
for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
    nb = json.load(open(path))
    dirty = False
    for cell in nb["cells"]:
        if cell.get("outputs"):
            cell["outputs"] = []
            dirty = True
        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            dirty = True
        cell.get("metadata", {}).pop("execution", None)
    if dirty:
        json.dump(nb, open(path, "w"), indent=1)
        open(path, "a").write("\n")
        changed += 1
        print(f"stripped {path.name}")
print(f"{changed} notebook(s) changed" if changed else "already clean")
