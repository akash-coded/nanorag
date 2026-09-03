#!/usr/bin/env bash
# Every check CI runs, locally, with exit codes that mean something.
#
# `ruff ... | tail -1 && pytest ... | tail -1` never fails: a pipe's status is
# tail's. That chain pushed a commit with three failing tests and read as green.
# So: pipefail, and no pipes on the gating commands at all.
set -euo pipefail

# Prefer the project venv when one exists and none is active, so `bash scripts/check.sh`
# behaves the same whether or not the contributor remembered to activate it.
if [ -z "${VIRTUAL_ENV:-}" ]; then
  for venv in .venv venv; do
    if [ -x "$venv/bin/python" ]; then PATH="$PWD/$venv/bin:$PATH"; export PATH; break; fi
  done
fi
cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"
say() { printf '\n\033[1m── %s\033[0m\n' "$1"; }

# Say what to run, not a traceback, when the tools are missing for this interpreter.
if ! "$PY" -c "import ruff, pytest" 2>/dev/null; then
  printf '%s has no ruff/pytest. Create the project venv and retry:\n  uv sync --extra dev\n  # or: python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"\n' "$PY" >&2
  exit 2
fi

say "ruff";        "$PY" -m ruff check nanorag tests scripts labs
# Mirrors the required CI job: notebooks are excluded here as they are there. They run in
# notebooks.yml and via `make test-all`; with nbformat installed they take many minutes.
say "pytest";      "$PY" -m pytest -q --no-header -p no:cacheprovider -m "not notebooks" 2>&1 | tail -3; test "${PIPESTATUS[0]}" -eq 0
say "lab DAG";     "$PY" scripts/lab.py verify
say "links";       "$PY" tools/check_links.py
say "mermaid";     node tools/validate-mermaid.mjs
say "markdown";    npx --yes markdownlint-cli2 "**/*.md" "#tools/node_modules" "#_site_docs"
say "workflows";   for f in .github/workflows/*.yml; do "$PY" -c "import yaml,sys;yaml.safe_load(open('$f'))" || { echo "invalid: $f"; exit 1; }; done; echo "all parse"
printf '\n\033[32mall checks passed\033[0m\n'
