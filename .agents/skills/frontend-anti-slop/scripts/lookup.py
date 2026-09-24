#!/usr/bin/env python3
"""Keyword lookup over the bundled UI/UX data tables.

Usage
    python3 scripts/lookup.py typography luxury editorial
    python3 scripts/lookup.py colors fintech dark
    python3 scripts/lookup.py motion hover card
    python3 scripts/lookup.py ux form validation --platform Web
    python3 scripts/lookup.py ux --category Accessibility --top 30
    python3 scripts/lookup.py typography --list-categories
    python3 scripts/lookup.py colors "AI/Chatbot" --full

Tables live in ../data/ next to this script. Scoring is a plain keyword
count over every column, with the row's name column weighted three times.
No dependencies beyond the standard library.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

TABLES = {
    "typography": {
        "file": "typography.csv",
        "name": "Font Pairing Name",
        "category": "Category",
        "brief": ["Font Pairing Name", "Category", "Heading Font", "Body Font",
                  "Mood/Style Keywords", "Best For"],
        "full_extra": ["Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"],
    },
    "colors": {
        "file": "colors.csv",
        "name": "Product Type",
        "category": "Product Type",
        "brief": ["Product Type", "Primary", "Secondary", "Accent",
                  "Background", "Foreground", "Notes"],
        "full_extra": ["On Primary", "On Secondary", "On Accent", "Card",
                       "Card Foreground", "Muted", "Muted Foreground", "Border",
                       "Destructive", "On Destructive", "Ring"],
    },
    "motion": {
        "file": "motion.csv",
        "name": "Category",
        "category": "Category",
        "brief": ["Category", "Intensity Tier", "Trigger", "Duration", "Easing",
                  "Do", "Don't"],
        "full_extra": ["Keywords", "GSAP Snippet", "Framework Notes",
                       "Performance Notes"],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "name": "Issue",
        "category": "Category",
        "brief": ["Category", "Issue", "Platform", "Severity", "Do", "Don't"],
        "full_extra": ["Description", "Code Example Good", "Code Example Bad"],
    },
}


def tokens(text):
    return [t for t in re.split(r"[^a-z0-9+#]+", text.lower()) if len(t) > 1]


def load(table):
    path = DATA_DIR / TABLES[table]["file"]
    if not path.exists():
        sys.exit(f"Data file not found: {path}")
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hits(term, toks):
    """Exact token match counts 2, prefix match (form -> forms) counts 1."""
    return sum(2 if t == term else (1 if t.startswith(term) else 0) for t in toks)


def score(row, terms, name_col):
    if not terms:
        return 1
    name_toks = tokens(row.get(name_col, ""))
    all_toks = tokens(" ".join(row.values()))
    return sum(3 * hits(term, name_toks) + hits(term, all_toks) for term in terms)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", choices=sorted(TABLES))
    ap.add_argument("keywords", nargs="*", help="keywords to match, any order")
    ap.add_argument("--top", type=int, default=8, help="rows to show (default 8)")
    ap.add_argument("--category", help="exact or partial match on the category column")
    ap.add_argument("--platform", help="ux table only: Web, Mobile, Desktop, All")
    ap.add_argument("--full", action="store_true", help="print every column")
    ap.add_argument("--list-categories", action="store_true",
                    help="print the distinct category values and exit")
    args = ap.parse_args()

    spec = TABLES[args.table]
    rows = load(args.table)

    if args.list_categories:
        seen = {}
        for r in rows:
            seen[r[spec["category"]]] = seen.get(r[spec["category"]], 0) + 1
        for k, v in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{v:3d}  {k}")
        return

    if args.category:
        needle = args.category.lower()
        rows = [r for r in rows if needle in r[spec["category"]].lower()]
    if args.platform and args.table == "ux":
        needle = args.platform.lower()
        rows = [r for r in rows if needle in r.get("Platform", "").lower()
                or r.get("Platform", "").lower() == "all"]

    terms = tokens(" ".join(args.keywords))
    scored = [(score(r, terms, spec["name"]), r) for r in rows]
    scored = [(s, r) for s, r in scored if s > 0]
    scored.sort(key=lambda sr: -sr[0])

    if not scored:
        print("No rows matched. Try fewer or broader keywords, or --list-categories.")
        return

    cols = spec["brief"] + (spec["full_extra"] if args.full else [])
    print(f"{args.table}: {len(scored)} match(es), showing {min(args.top, len(scored))}\n")
    for s, r in scored[: args.top]:
        head = f"[{r.get('No', '?')}] {r.get(spec['name'], '')}"
        print(head)
        for c in cols:
            if c == spec["name"] or not r.get(c):
                continue
            val = r[c].replace("\n", " ").strip()
            if not args.full and len(val) > 160:
                val = val[:157] + "..."
            print(f"  {c}: {val}")
        print()


if __name__ == "__main__":
    main()
