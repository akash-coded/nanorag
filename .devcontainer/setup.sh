#!/usr/bin/env bash
# One-time environment build for a Codespace or a local dev container.
#
# Runs at onCreate rather than postCreate so a prebuild can bake the result:
# with prebuilds configured, a Codespace opens with this already done and the
# learner waits for nothing.
set -euo pipefail

echo "──> installing nanorag and the dev extras"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -e ".[dev]"

echo "──> installing the documentation validators (node)"
npm --prefix tools install --silent --no-audit --no-fund || \
  echo "    (skipped -- the labs and notebooks do not need these)"

# The lexical retrieval leg IS FTS5. A Python built without it produces no error
# at import time and fails several notebooks in, so assert it here where the
# message can say what to do.
echo "──> checking SQLite has FTS5"
python - <<'PY'
import sqlite3, sys
con = sqlite3.connect(":memory:")
has = any("FTS5" in row[0] for row in con.execute("PRAGMA compile_options"))
if not has:
    sys.exit(
        "\n  This Python's SQLite was built without FTS5, and the lexical retrieval\n"
        "  leg is FTS5 -- there is no fallback. Rebuild the container from the\n"
        "  image in .devcontainer/devcontainer.json, which has it.\n")
print(f"    ok -- sqlite {sqlite3.sqlite_version} with FTS5")
PY

echo "──> verifying the lab pathway"
python scripts/lab.py verify

echo
echo "ready. run:  python scripts/lab.py next"
