#!/usr/bin/env python3
"""Turn answered discussions into docs/90-reference/faq.md.

Discussions are where the real questions get answered, and docs are where people
look first. Without something joining them, every answer is findable only by
someone who already knows to search Discussions — so the same question gets asked
again, and the thread that answered it the first time is wasted.

This reads every thread whose answer has been marked, and writes an index with a
short extract. It deliberately does NOT copy the whole answer: the thread is the
source of truth, including the argument that got there, and a copy would go stale.

Usage:
    python scripts/harvest_faq.py            # write the file
    python scripts/harvest_faq.py --check    # exit 1 if the file is out of date
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

OWNER, REPO = "akash-coded", "nanorag"
OUT = pathlib.Path(__file__).resolve().parent.parent / "docs/90-reference/faq.md"

QUERY = """
query($o:String!,$r:String!){
  repository(owner:$o,name:$r){
    discussions(first:100, orderBy:{field:CREATED_AT, direction:ASC}){
      nodes{
        number title url isAnswered
        category{ name }
        answer{ body }
      } } } }
"""


def fetch() -> list[dict]:
    proc = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"o={OWNER}", "-f", f"r={REPO}"],
        capture_output=True, text=True)
    if proc.returncode:
        sys.exit(f"gh failed: {proc.stderr.strip()}")
    nodes = json.loads(proc.stdout)["data"]["repository"]["discussions"]["nodes"]
    return [n for n in nodes if n.get("isAnswered") and n.get("answer")]


# Answers often open by explaining *why* they are the accepted answer. That is
# useful in the thread and useless in an index, so it is dropped.
META = re.compile(
    r"^(marking|accepting|i am marking|marked)\b[^.]*\.\s*",
    re.I)


def extract(body: str, limit: int = 240) -> str:
    """First substantive sentence of the answer, with markdown flattened."""
    text = body
    text = re.sub(r"```[\s\S]*?```", " ", text)          # code blocks
    text = re.sub(r"^>.*$", " ", text, flags=re.M)        # persona headers, quotes
    text = re.sub(r"^\|.*$", " ", text, flags=re.M)       # tables
    text = re.sub(r"^#+\s*", "", text, flags=re.M)        # headings
    text = re.sub(r"^\s*[-*_]{3,}\s*$", " ", text, flags=re.M)   # horizontal rules
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.M)        # list numbering
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    # Strip emphasis markers but NOT underscores: full_chain_recall is an
    # identifier, and collapsing it to fullchainrecall makes the extract wrong.
    text = re.sub(r"[*`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    for _ in range(2):                       # at most two leading meta sentences
        stripped = META.sub("", text, count=1)
        if stripped == text:
            break
        text = stripped
    if len(text) <= limit:
        return text
    cut = text[:limit]
    stop = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    return (cut[:stop + 1] if stop > 80 else cut.rstrip() + "…").strip()


def render(threads: list[dict]) -> str:
    by_category: dict[str, list[dict]] = {}
    for t in threads:
        by_category.setdefault(t["category"]["name"], []).append(t)

    out = [
        "# FAQ",
        "",
        "Every discussion whose answer has been marked, grouped by category.",
        "",
        "**Generated** by `scripts/harvest_faq.py` and refreshed weekly by the",
        "`FAQ` workflow — edit the thread, not this file. The extract is the opening of",
        "the accepted answer; the thread itself carries the argument that got there, which",
        "is usually the more useful half.",
        "",
        f"{len(threads)} answered {'thread' if len(threads) == 1 else 'threads'}.",
        "",
    ]
    for category in sorted(by_category):
        out += [f"## {category}", ""]
        for t in sorted(by_category[category], key=lambda x: x["number"]):
            out += [f"### [{t['title']}]({t['url']})", "",
                    extract(t["answer"]["body"]), "",
                    f"[Read the thread →]({t['url']})", ""]
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed file differs from what would be generated")
    args = ap.parse_args()

    content = render(fetch())
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != content:
            print("docs/90-reference/faq.md is out of date; run scripts/harvest_faq.py")
            return 1
        print("faq.md is up to date")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUT.relative_to(OUT.parent.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
