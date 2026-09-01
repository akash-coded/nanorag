#!/usr/bin/env python3
"""Push wiki/ to the repository's wiki, once.

GitHub creates a wiki's git repository only after the first page is created in the
web UI. Until then `nanorag.wiki.git` returns "Repository not found", and there is
no API for wiki content -- GraphQL exposes `hasWikiEnabled` and nothing writable.
So this cannot be fully automated, and the error below says so rather than failing
with git's unhelpful message.

This is a SEED, not a mirror. After the first push the wiki is authoritative,
because the point of a wiki is that somebody can fix a wrong error string without
opening a pull request. Running it again needs --force.

    python scripts/sync_wiki.py
    python scripts/sync_wiki.py --force     # overwrite an already-seeded wiki
    python scripts/sync_wiki.py --dry-run
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEED = ROOT / "wiki"
REMOTE = "https://github.com/akash-coded/nanorag.wiki.git"

NOT_INITIALISED = """
The wiki git repository does not exist yet.

Turning the Wiki feature on is not enough: GitHub creates nanorag.wiki.git only
after the first page is created through the web UI, and there is no API for it.

  1. Open  https://github.com/akash-coded/nanorag/wiki
  2. Create any page. The title and body do not matter -- this script overwrites them.
  3. Run this again.
"""


def run(cmd: list[str], cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="overwrite a wiki that already has pages")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pages = sorted(p for p in SEED.glob("*.md") if p.name != "README.md")
    if not pages:
        sys.exit(f"no pages in {SEED}")
    print(f"{len(pages)} pages to seed: " + ", ".join(p.stem for p in pages))
    if args.dry_run:
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        clone = pathlib.Path(tmp) / "wiki"
        got = run(["git", "clone", "--quiet", REMOTE, str(clone)])
        if got.returncode:
            if "not found" in got.stderr.lower():
                print(NOT_INITIALISED.strip(), file=sys.stderr)
                return 2
            print(got.stderr.strip(), file=sys.stderr)
            return 1

        existing = [p for p in clone.glob("*.md")]
        substantive = [p for p in existing if p.read_text(encoding="utf-8").strip()]
        if len(substantive) > 1 and not args.force:
            print(f"the wiki already has {len(substantive)} pages. This is a seed, not a mirror --"
                  "\nrerun with --force only if you mean to overwrite what is there.",
                  file=sys.stderr)
            return 3

        for page in pages:
            shutil.copy2(page, clone / page.name)

        run(["git", "add", "-A"], cwd=clone)
        status = run(["git", "status", "--porcelain"], cwd=clone)
        if not status.stdout.strip():
            print("wiki is already identical to the seed")
            return 0
        commit = run(["git", "-c", "user.name=nanorag", "-c",
                      "user.email=noreply@github.com", "commit", "-q", "-m",
                      "Seed the wiki from wiki/ in the main repository"], cwd=clone)
        if commit.returncode:
            print(commit.stderr.strip(), file=sys.stderr)
            return 1
        push = run(["git", "push", "--quiet", "origin", "HEAD"], cwd=clone)
        if push.returncode:
            print(push.stderr.strip(), file=sys.stderr)
            return 1

    print(f"pushed {len(pages)} pages -> https://github.com/akash-coded/nanorag/wiki")
    print("The wiki is authoritative from here. Edit it there, not in wiki/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
