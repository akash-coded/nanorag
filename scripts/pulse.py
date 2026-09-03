#!/usr/bin/env python3
"""Refresh the Repo Pulse board: what needs attention, what is hot, what changed.

One row per thing worth a maintainer's glance this week. Rows are upserted by a
stable title, and rows that no longer qualify are archived, so the board is a
live view rather than a log. Runs every six hours from pulse.yml.

    Unanswered Q&A    a Q&A thread with no accepted answer, older than 48h
    Discussion        any thread with 3+ comments in the last 7 days
    Pull request      open, updated in the last 7 days
    Issue             open, updated in the last 7 days, not on the delivery board yet
    Content changed   an area of the repo with commits in the last 7 days
    Arena activity    a lab or challenge with attempts on the Tracker this week
    New learner       a Tracker learner whose first attempt was this week
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import boards  # noqa: E402

OWNER, REPO = "akash-coded", "nanorag"
NOW = dt.datetime.now(dt.timezone.utc)
WEEK = NOW - dt.timedelta(days=7)
TWO_DAYS = NOW - dt.timedelta(hours=48)

AREAS = {
    "notebooks/": "notebooks",
    "labs/": "labs",
    "docs/60-cheatsheets/": "cheatsheets",
    "docs/": "docs",
    "wiki/": "wiki",
    "threads/": "discussions",
    ".github/workflows/": "workflows",
    "nanorag/": "toolkit",
}

# comments(last:20) x replies(last:5): about 120 points a refresh. The first version
# asked for 50 x 20 and cost about 950 -- GraphQL prices what a query could return, not
# what it does. Heat needs five recent events, so the sample loses nothing that matters;
# the totals stay exact.
Q = """
query($o:String!,$r:String!){
  repository(owner:$o,name:$r){
    discussions(first:100, orderBy:{field:UPDATED_AT, direction:DESC}){
      nodes{
        number title url isAnswered createdAt updatedAt category{name}
        comments(last:20){
          totalCount
          nodes{ createdAt replies(last:5){ totalCount nodes{createdAt} } } } } }
    pullRequests(first:30, states:OPEN, orderBy:{field:UPDATED_AT, direction:DESC}){
      nodes{ number title url updatedAt comments{totalCount} } }
    issues(first:50, states:OPEN, orderBy:{field:UPDATED_AT, direction:DESC}){
      nodes{ number title url updatedAt comments{totalCount} } } } }
"""


def _gh(*args):
    p = subprocess.run(["gh", *args], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(f"gh failed: {p.stderr.strip()[:200]}")
    return p.stdout


def _iso(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def heat(n_recent: int) -> str:
    return "🔥 Hot" if n_recent >= 5 else "Warm" if n_recent >= 2 else "Quiet"


def area_of(path: str) -> str:
    for prefix, name in AREAS.items():
        if path.startswith(prefix):
            return name
    return "docs" if path.endswith(".md") else "toolkit"


def collect() -> list[dict]:
    data = json.loads(
        _gh("api", "graphql", "-f", f"query={Q}", "-f", f"o={OWNER}", "-f", f"r={REPO}")
    )
    repo = data["data"]["repository"]
    rows: list[dict] = []

    for d in repo["discussions"]["nodes"]:
        stamps = [_iso(c["createdAt"]) for c in d["comments"]["nodes"]]
        stamps += [
            _iso(r["createdAt"]) for c in d["comments"]["nodes"] for r in c["replies"]["nodes"]
        ]
        recent = sum(1 for s in stamps if s >= WEEK)
        total = d["comments"]["totalCount"] + sum(
            c["replies"]["totalCount"] for c in d["comments"]["nodes"]
        )
        cat = d["category"]["name"]
        if (
            cat == "Q&A"
            and not d["isAnswered"]
            and _iso(d["createdAt"]) < TWO_DAYS
            and not d["title"].startswith(("[clinic", "[lab ", "[arena", "[submit"))
        ):
            age = (NOW - _iso(d["createdAt"])).days
            rows.append(
                {
                    "title": f"❓ #{d['number']} {d['title'][:70]}",
                    "Kind": "Unanswered Q&A",
                    "Heat": "🔥 Hot" if age >= 7 else "Warm",
                    "Engagement": total,
                    "Last activity": _iso(d["updatedAt"]).date(),
                    "Area": "discussions",
                    "Link": d["url"],
                }
            )
        elif recent >= 3:
            rows.append(
                {
                    "title": f"💬 #{d['number']} {d['title'][:70]}",
                    "Kind": "Discussion",
                    "Heat": heat(recent),
                    "Engagement": total,
                    "Last activity": _iso(d["updatedAt"]).date(),
                    "Area": "discussions",
                    "Link": d["url"],
                }
            )

    for pr in repo["pullRequests"]["nodes"]:
        if _iso(pr["updatedAt"]) >= WEEK:
            rows.append(
                {
                    "title": f"🔀 PR #{pr['number']} {pr['title'][:66]}",
                    "Kind": "Pull request",
                    "Heat": heat(pr["comments"]["totalCount"]),
                    "Engagement": pr["comments"]["totalCount"],
                    "Last activity": _iso(pr["updatedAt"]).date(),
                    "Area": "workflows",
                    "Link": pr["url"],
                }
            )
    for iss in repo["issues"]["nodes"]:
        if _iso(iss["updatedAt"]) >= WEEK and iss["comments"]["totalCount"] >= 1:
            rows.append(
                {
                    "title": f"🐛 #{iss['number']} {iss['title'][:68]}",
                    "Kind": "Issue",
                    "Heat": heat(iss["comments"]["totalCount"]),
                    "Engagement": iss["comments"]["totalCount"],
                    "Last activity": _iso(iss["updatedAt"]).date(),
                    "Area": "toolkit",
                    "Link": iss["url"],
                }
            )

    # content churn by area, from git
    log = subprocess.run(
        ["git", "log", f"--since={WEEK.date()}", "--name-only", "--pretty=format:"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    ).stdout
    churn: dict[str, set] = {}
    for line in log.splitlines():
        if line.strip():
            churn.setdefault(area_of(line.strip()), set()).add(line.strip())
    for area, files in sorted(churn.items(), key=lambda kv: -len(kv[1])):
        rows.append(
            {
                "title": f"📝 {len(files)} files changed in {area}/",
                "Kind": "Content changed",
                "Heat": heat(len(files) // 5),
                "Engagement": len(files),
                "Last activity": NOW.date(),
                "Area": area,
                "Link": f"https://github.com/{OWNER}/{REPO}/commits/main",
            }
        )

    # arena activity and new learners, from the Tracker
    try:
        tracker = boards.Board(boards.TRACKER)
        per_item: dict[str, int] = {}
        learners: dict[str, dt.date] = {}
        for row in tracker._index().values():
            fa = boards.field_value(row, "First attempt")
            item = boards.field_value(row, "Item")
            who = boards.field_value(row, "Learner")
            if fa and dt.date.fromisoformat(str(fa)[:10]) >= WEEK.date():
                first = dt.date.fromisoformat(str(fa)[:10])
                if item:
                    per_item[item] = per_item.get(item, 0) + 1
                if who and (who not in learners or first < learners[who]):
                    learners[who] = first
        for item, n in sorted(per_item.items()):
            rows.append(
                {
                    "title": f"🧪 {item}: {n} learner{'s' if n != 1 else ''} this week",
                    "Kind": "Arena activity",
                    "Heat": heat(n),
                    "Engagement": n,
                    "Last activity": NOW.date(),
                    "Area": "labs",
                    "Link": f"https://github.com/users/{OWNER}/projects/{boards.TRACKER}",
                }
            )
        for who, first in sorted(learners.items()):
            rows.append(
                {
                    "title": f"👋 new learner: {who}",
                    "Kind": "New learner",
                    "Heat": "Warm",
                    "Engagement": per_item and sum(per_item.values()) or 1,
                    "Last activity": first,
                    "Area": "labs",
                    "Link": f"https://github.com/{who}",
                }
            )
    except Exception as exc:  # noqa: BLE001 -- the pulse must not fail because the tracker is empty
        print(f"tracker read skipped: {exc}", file=sys.stderr)
    return rows


def main() -> int:
    boards.require_budget(600, "a pulse refresh")
    rows = collect()
    board = boards.Board(boards.PULSE)
    keep = set()
    for r in rows:
        title = r.pop("title")
        keep.add(title)
        _, created = board.upsert(title, **r)
        print(f"  {'+' if created else '~'} {title}")
    archived = 0
    for title, it in list(board._index(refresh=True).items()):
        if title not in keep:
            board.archive(it["id"])
            archived += 1
    print(f"{len(rows)} rows current, {archived} archived")
    return 0


if __name__ == "__main__":
    sys.exit(main())
