# Common errors

**Search this page for your literal error string.** Every entry below is something that actually
happened in this repository, with the message as it appears, not paraphrased.

If you solve something not listed here, add it. The value of this page is entirely its coverage.

---

## `Input required and not supplied: issue_message`

**Where:** the `Welcome` workflow, on every newly opened issue or PR.

**Cause:** `actions/first-interaction` v3 renamed its inputs from kebab-case to snake_case —
`issue-message` → `issue_message`, `pr-message` → `pr_message`, `repo-token` → `repo_token`.
GitHub Actions does **not** normalise the hyphen, so `getInput('issue_message')` found nothing.

**Fix:** rename the inputs in the workflow.

**Why it hid:** it fails *open* for the repository — the greet job goes red and nothing else
breaks — and *closed* for the person it exists to serve, who silently gets no welcome. Caught by
CI going red on an unrelated PR, not by review of the bump.

---

## `Parse error on line N: ... Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE' ...`

**Where:** a Mermaid diagram, or `node tools/validate-mermaid.mjs`.

**Cause:** an unquoted `(` or `)` inside a `[]` node label. `PI[pipeline.py<br/>evaluate()]` fails;
`PI["pipeline.py<br/>evaluate()"]` parses.

**Fix:** quote the label. Every label in this repo is quoted for exactly this reason.

**Why it hid:** on GitHub a diagram that fails to parse renders as **nothing** — no error, no
placeholder, just absence. It shipped once and was only found by parsing every block against the
real parser.

```bash
node tools/validate-mermaid.mjs
```

---

## `Not Found` from `actions/deploy-pages`

**Where:** the `Pages` workflow, at the deploy step, with the build step green.

**Cause:** GitHub Pages had never been **enabled** for the repository. The workflow is fine; there
is nothing to deploy into.

**Fix:** Settings → Pages → Source → **GitHub Actions**. Or:

```bash
gh api -X POST repos/OWNER/REPO/pages -f build_type=workflow
```

**Why it hid:** the repository's homepage field advertised the Pages URL, so it looked configured.

---

## `E402 Module level import not at top of file` in a script that must import late

**Where:** `ruff check`, on any file that calls `sys.path.insert` or `matplotlib.use()` before
importing.

**Cause:** the ordering is deliberate — `matplotlib.use("Agg")` must run before `pyplot` is
imported, and `sys.path.insert` must run before a local package import.

**Fix:** `# noqa: E402` **with the reason written next to it.** Reordering to satisfy the linter
breaks the backend selection or the import.

---

## `findfont: Failed to find font weight medium, now using 400`

**Where:** any matplotlib figure using `fontweight="medium"`.

**Cause:** DejaVu Sans, matplotlib's default, has no medium weight.

**Fix:** use `"normal"` or `"bold"`, or install a font that has one. Harmless warning; the figure
renders.

---

## `Pull Request has merge conflicts (mergePullRequest)`

**Where:** merging several Dependabot PRs in a row.

**Cause:** they all edit `pyproject.toml`. Merging one invalidates the others.

**Fix:** comment `@dependabot rebase` on each remaining PR and merge them one at a time.

---

## `no such file or directory: nanorag` after a successful `cd nanorag`

**Where:** any shell where the working directory persists between commands.

**Cause:** you are already inside `nanorag/`, and there is a Python package directory *also* called
`nanorag/`. The second `cd nanorag` puts you in the package.

**Fix:** use absolute paths, or `git -C /path/to/repo`. This has cost real time.

---

## `ModuleNotFoundError: No module named 'nanorag'` after `pip install -e .`

**Cause:** almost always a different interpreter than the one that ran `pip`.

**Fix:**

```bash
python -c "import sys; print(sys.executable)"
python -m pip install -e ".[dev]"      # -m pins the interpreter
```

---

## `sqlite3.OperationalError: no such module: fts5`

**Cause:** a Python built against a SQLite without FTS5. Common on some Linux distribution
packages and older conda builds.

**Fix:**

```python
import sqlite3
print(sqlite3.sqlite_version)
con = sqlite3.connect(":memory:")
print([r for r in con.execute("PRAGMA compile_options") if "FTS5" in r[0]])
```

If FTS5 is absent, install Python from python.org, use the system Python on macOS, or a
`python:3.12` container. There is no pure-Python fallback — the lexical leg **is** FTS5.

---

## A query returns results and they are the wrong results, with no error

**Cause:** several, and none of them raise. This is the class of bug this repository is mostly
about — see [Troubleshooting](Troubleshooting).

The three most common: a tokenizer that split your identifiers, a mixed-encoder index, and a
post-filter that collapsed `k`.
