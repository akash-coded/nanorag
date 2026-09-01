# Environment setup

The repository's promise is that it runs offline with no dataset, no API key and no service. That
holds on every platform below, but each has one thing worth knowing in advance.

```bash
git clone https://github.com/akash-coded/nanorag.git
cd nanorag
make setup      # or: python -m pip install -e ".[dev]"
make lab
```

**Use `python -m pip`, not `pip`.** The `-m` form pins the interpreter, and a mismatch between the
`pip` on your PATH and the `python` you run is the single most common setup failure.

---

## macOS

Works out of the box on the system Python 3.10+ and on python.org builds.

**Homebrew Python is fine**, but if you have several installed, be deliberate:

```bash
python3 -c "import sys; print(sys.executable)"
```

**Apple Silicon:** no special handling. There is no compiled dependency in the core path — numpy
and matplotlib ship arm64 wheels.

---

## Linux

**Check FTS5 before anything else.** Some distribution Python packages are built against a SQLite
without it, and the lexical leg *is* FTS5 — there is no fallback.

```python
import sqlite3
con = sqlite3.connect(":memory:")
print([r for r in con.execute("PRAGMA compile_options") if "FTS5" in r[0]])
```

Empty output means no FTS5. Use a `python:3.12` container or a python.org build.

---

## Windows

**Use WSL2.** Native Windows will mostly work, but:

- Terminal colour output in `scripts/lab.py` needs a terminal that understands ANSI
- Path separators in a few notebook cells assume POSIX
- The `Makefile` needs `make`, which is not present by default

Under WSL2 it behaves exactly like Linux, including the FTS5 check above.

---

## Google Colab

Runs, with one caveat: **Colab's runtime resets**, so the in-memory index disappears between
sessions. That is the design working as intended, not a problem — but it means "Run All" is the
only supported flow.

```python
!git clone https://github.com/akash-coded/nanorag.git
%cd nanorag
!python -m pip install -q -e ".[dev]"
```

Then open a notebook from the file browser. Expect a kernel restart prompt after the install.

---

## Dev container / Codespaces

No devcontainer is committed yet — [open an idea](https://github.com/akash-coded/nanorag/discussions/categories/ideas)
if you want one. A minimal working config:

```json
{
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "postCreateCommand": "python -m pip install -e '.[dev]'",
  "customizations": { "vscode": { "extensions": ["ms-toolsai.jupyter"] } }
}
```

---

## For the L.A.B. simulator

The labs are pure Python and need nothing beyond the dev extras.

```bash
python scripts/lab.py next
python scripts/lab.py run L01
```

**If `lab.py` prints escape codes instead of colour**, your terminal is not interpreting ANSI. The
output is still correct; pipe through `sed 's/\x1b\[[0-9;]*m//g'` if it bothers you.

---

## For the docs site

Only needed if you are editing docs and want to preview:

```bash
python -m pip install mkdocs-material
mkdocs serve
```

## For the diagram and link validators

```bash
npm --prefix tools install
node tools/validate-mermaid.mjs
python tools/check_links.py
```

Both run in CI, so this is only for catching things before you push — which is worth doing, because
a red check on your own PR is slower than a local run.

---

## What is deliberately not required

No vector database. No API key. No dataset download. No GPU. No network at run time.

If something you are doing needs one of those, you are on an optional path — Bedrock, a
sentence-transformer encoder, a model judge — and the core material still runs without it.
