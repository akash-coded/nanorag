# Everything a student or a CI runner needs, in one place.
.DEFAULT_GOAL := help
PY ?= python3

help:            ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup:           ## Install runtime + dev dependencies
	$(PY) -m pip install -U pip
	$(PY) -m pip install -e ".[dev]"

lab:             ## Launch JupyterLab on the notebooks
	$(PY) -m jupyterlab notebooks

test:            ## Fast unit tests (no notebook execution)
	$(PY) -m pytest -m "not notebooks"

test-all:        ## Everything, including notebook execution
	$(PY) -m pytest

lint:            ## Ruff check
	$(PY) -m ruff check nanorag tests scripts

fmt:             ## Ruff autofix
	$(PY) -m ruff check --fix nanorag tests scripts

notebooks:       ## Execute every notebook headlessly and report timings
	$(PY) scripts/verify_notebooks.py

strip:           ## Strip notebook outputs before committing
	$(PY) scripts/strip_outputs.py

eval:            ## Run the release-gate evaluation and print the scorecard
	$(PY) scripts/run_eval.py

board:           ## One-time GitHub setup: labels, discussions, issues, project board
	$(PY) scripts/setup_github.py --owner $${OWNER:?set OWNER=your-github-handle} --repo $${REPO:-nanorag}

.PHONY: help setup lab test test-all lint fmt notebooks strip eval board wiki-pull

.PHONY: check wiki-pull
## Every check CI runs, locally, with exit codes that mean something. Run before every push.
check:
	bash scripts/check.sh

wiki-pull: ## Refresh wiki/ from the live wiki (the wiki is canonical; wiki/ is a mirror)
	@tmp=$$(mktemp -d) && git clone -q --depth 1 https://github.com/akash-coded/nanorag.wiki.git "$$tmp" \
	  && rsync -a --delete --exclude .git --exclude README.md "$$tmp/" wiki/ && rm -rf "$$tmp" \
	  && git status --short wiki/ && echo "wiki/ refreshed from the live wiki; commit the result"
