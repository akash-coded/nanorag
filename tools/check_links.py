"""Resolve every relative markdown link in the repository.

Runs in CI and locally. Absolute GitHub application routes (/discussions, /issues,
/projects) must be written as full URLs: a relative "../../discussions" resolves
correctly from README.md at the root but NOT from inside docs/, where GitHub turns
it into /nanorag/blob/discussions. That bug shipped once; this script is why it
cannot ship again.
"""
from __future__ import annotations
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# wiki/ is the seed for the GitHub wiki, where links are extensionless page names
# ([Common Errors](Common-Errors)) rather than file paths. Resolving them as files
# is wrong, so they are checked by GitHub's own wiki renderer instead.
SKIP = {".git", "node_modules", ".venv", "_site", ".ipynb_checkpoints", "wiki"}
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")

def main() -> int:
    broken: list[str] = []
    files = [m for m in sorted(ROOT.rglob("*.md")) if not SKIP & set(m.parts)]
    for md in files:
        for target in LINK.findall(md.read_text(encoding="utf-8", errors="ignore")):
            if target.startswith(("http://", "https://", "mailto:", "<", "?")):
                continue  # "?" is a GitHub query string, e.g. ?template=docs.md
            if not (md.parent / target).resolve().exists():
                broken.append(f"{md.relative_to(ROOT)} -> {target}")
    if broken:
        print("Broken relative links:", *broken, sep="\n  ")
        return 1
    print(f"all relative links resolve ({len(files)} files scanned)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
