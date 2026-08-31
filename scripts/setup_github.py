#!/usr/bin/env python3
"""One-time GitHub provisioning for this repository.

Creates everything that cannot live in the git tree: repository settings, labels, milestones,
seeded issues (open and closed), Discussions with their categories and seeded threads, and a
Projects v2 board with custom fields and items.

    export GITHUB_TOKEN=github_pat_...
    python scripts/setup_github.py --owner fde-academy-learning --repo adv-rag-hands-on

Idempotent: safe to re-run. Anything that already exists is skipped rather than duplicated.

    --dry-run     print what would happen, change nothing
    --only        labels,milestones,settings,issues,discussions,project   (comma separated)
    --skip        same vocabulary, inverted

Token permissions needed (fine-grained PAT):
    Repository → Administration: read/write   (settings, labels, enabling Discussions)
                 Contents:       read/write
                 Issues:         read/write
                 Discussions:    read/write
                 Pull requests:  read/write
    Account    → Projects:       read/write   (only for the board)

If the Projects permission is unavailable, everything else still runs and the board step is
reported as skipped with the manual instructions.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import seed_content as content  # noqa: E402
from gh import GitHubError, fail, graphql, ok, request, skip, warn  # noqa: E402

STEPS = ("settings", "labels", "milestones", "issues", "discussions", "project")


# ────────────────────────────────────────────────────────────────── settings ──
def configure_repository(owner, repo, dry):
    """Description, topics, features, merge policy, branch protection."""
    payload = {
        "description": ("Runnable retrieval / RAG / evaluation curriculum — 10 notebooks and a "
                        "toolkit that run entirely in memory, with an eval gate in CI"),
        "homepage": f"https://{owner}.github.io/{repo}/",
        "has_issues": True,
        "has_projects": True,
        "has_discussions": True,
        "has_wiki": False,
        "allow_squash_merge": True,
        "allow_merge_commit": False,
        "allow_rebase_merge": True,
        "delete_branch_on_merge": True,
        "allow_auto_merge": True,
        "squash_merge_commit_title": "PR_TITLE",
        "squash_merge_commit_message": "PR_BODY",
    }
    if dry:
        skip("settings", "would set description, topics, enable Discussions")
        return
    try:
        request("PATCH", f"/repos/{owner}/{repo}", payload)
        ok("repository settings", "Discussions + Projects enabled, squash-merge only")
    except GitHubError as exc:
        fail("repository settings", exc.message[:120])

    topics = ["rag", "retrieval-augmented-generation", "information-retrieval", "bm25",
              "reranking", "vector-search", "llm-evaluation", "evaluation", "bedrock",
              "jupyter-notebooks", "teaching-materials", "python", "sqlite", "fts5",
              "hybrid-search", "llm-as-a-judge"]
    try:
        request("PUT", f"/repos/{owner}/{repo}/topics", {"names": topics})
        ok("topics", f"{len(topics)} set")
    except GitHubError as exc:
        warn("topics", exc.message[:100])

    # Branch protection: require CI + the eval gate, and a review. Best-effort — this needs
    # Administration:write and is unavailable on some plans for private repos.
    protection = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["Lint", "Tests (py3.11)",
                         "One-click promise (fresh machine, no pip install)"],
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": True,
        },
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "required_conversation_resolution": True,
    }
    try:
        request("PUT", f"/repos/{owner}/{repo}/branches/main/protection", protection)
        ok("branch protection", "main requires CI + 1 review")
    except GitHubError as exc:
        warn("branch protection", f"skipped — {exc.message[:90]}")


# ──────────────────────────────────────────────────────────────────── labels ──
def create_labels(owner, repo, dry):
    existing = {l["name"] for l in request("GET", f"/repos/{owner}/{repo}/labels?per_page=100")}
    created = updated = 0
    for name, color, description in content.LABELS:
        if dry:
            skip(f"label {name}")
            continue
        payload = {"name": name, "color": color, "description": description}
        try:
            if name in existing:
                request("PATCH", f"/repos/{owner}/{repo}/labels/{name.replace(' ', '%20')}",
                        payload)
                updated += 1
            else:
                request("POST", f"/repos/{owner}/{repo}/labels", payload)
                created += 1
        except GitHubError as exc:
            warn(f"label {name}", exc.message[:80])
    # Remove GitHub's defaults we do not use, so the label list stays legible.
    for junk in ("bug", "enhancement", "question", "invalid", "wontfix", "duplicate"):
        if junk in existing and not dry:
            try:
                request("DELETE", f"/repos/{owner}/{repo}/labels/{junk}")
            except GitHubError:
                pass
    ok("labels", f"{created} created, {updated} updated")


# ──────────────────────────────────────────────────────────────── milestones ──
def create_milestones(owner, repo, dry):
    existing = {m["title"]: m for m in
                request("GET", f"/repos/{owner}/{repo}/milestones?state=all&per_page=100")}
    mapping = {}
    for title, description, state in content.MILESTONES:
        if title in existing:
            mapping[title] = existing[title]["number"]
            continue
        if dry:
            skip(f"milestone {title}")
            continue
        try:
            m = request("POST", f"/repos/{owner}/{repo}/milestones",
                        {"title": title, "description": description, "state": state})
            mapping[title] = m["number"]
        except GitHubError as exc:
            warn(f"milestone {title}", exc.message[:80])
    ok("milestones", f"{len(mapping)} present")
    return mapping


# ──────────────────────────────────────────────────────────────────── issues ──
def create_issues(owner, repo, milestones, dry):
    existing = {i["title"] for i in
                request("GET", f"/repos/{owner}/{repo}/issues?state=all&per_page=100")}
    created = []
    for spec in content.ISSUES:
        if spec["title"] in existing:
            skip(f"issue “{spec['title'][:52]}…”", "exists")
            continue
        if dry:
            skip(f"issue “{spec['title'][:52]}…”", spec["state"])
            continue
        payload = {"title": spec["title"], "body": spec["body"], "labels": spec["labels"]}
        if spec.get("milestone") in milestones:
            payload["milestone"] = milestones[spec["milestone"]]
        try:
            issue = request("POST", f"/repos/{owner}/{repo}/issues", payload)
            if spec["state"] == "closed":
                request("PATCH", f"/repos/{owner}/{repo}/issues/{issue['number']}",
                        {"state": "closed", "state_reason": "completed"})
            created.append((issue["number"], spec["title"], spec["state"]))
            ok(f"issue #{issue['number']}", f"{spec['state']:<6} {spec['title'][:56]}")
            time.sleep(0.6)                      # stay under the secondary rate limit
        except GitHubError as exc:
            fail(f"issue “{spec['title'][:40]}…”", exc.message[:90])
    return created


# ─────────────────────────────────────────────────────────────── discussions ──
REPO_Q = """
query($owner:String!,$name:String!){
  repository(owner:$owner,name:$name){
    id hasDiscussionsEnabled
    discussionCategories(first:50){ nodes { id name slug } }
    discussions(first:100){ nodes { title } }
  }
}"""

CREATE_DISCUSSION_M = """
mutation($repoId:ID!,$catId:ID!,$title:String!,$body:String!){
  createDiscussion(input:{repositoryId:$repoId,categoryId:$catId,title:$title,body:$body}){
    discussion { number url }
  }
}"""

ADD_COMMENT_M = """
mutation($discussionId:ID!,$body:String!){
  addDiscussionComment(input:{discussionId:$discussionId,body:$body}){
    comment { id }
  }
}"""

DISCUSSION_ID_Q = """
query($owner:String!,$name:String!,$number:Int!){
  repository(owner:$owner,name:$name){ discussion(number:$number){ id } }
}"""


def create_discussions(owner, repo, dry):
    data = graphql(REPO_Q, {"owner": owner, "name": repo})["repository"]
    if not data["hasDiscussionsEnabled"]:
        fail("discussions", "not enabled — run the `settings` step first")
        return []

    categories = {c["name"]: c["id"] for c in data["discussionCategories"]["nodes"]}
    existing = {d["title"] for d in data["discussions"]["nodes"]}

    missing = {name for name, *_ in content.CATEGORIES} - set(categories)
    if missing:
        warn("discussion categories",
             f"create manually in Settings → Discussions: {', '.join(sorted(missing))}")
        print("      (the GitHub API cannot create discussion categories; "
              "threads for missing categories fall back to General)")

    created = []
    for spec in content.DISCUSSIONS:
        title = spec["title"]
        if title in existing:
            skip(f"discussion “{title[:52]}…”", "exists")
            continue
        cat_id = categories.get(spec["category"]) or categories.get("General")
        if not cat_id:
            fail(f"discussion “{title[:40]}…”", "no usable category")
            continue
        if dry:
            skip(f"discussion “{title[:52]}…”", spec["category"])
            continue

        body = spec["body"]
        if "[worked example]" in title or spec["category"] in ("Q&A", "Design Reviews",
                                                              "Show and tell", "Reading Club",
                                                              "Interview Prep"):
            body += content.SEED_FOOTER
        try:
            out = graphql(CREATE_DISCUSSION_M, {
                "repoId": data["id"], "catId": cat_id, "title": title, "body": body})
            disc = out["createDiscussion"]["discussion"]
            created.append((disc["number"], title))
            ok(f"discussion #{disc['number']}", f"{spec['category']:<16} {title[:48]}")

            if spec.get("answer"):
                ids = graphql(DISCUSSION_ID_Q,
                              {"owner": owner, "name": repo, "number": disc["number"]})
                graphql(ADD_COMMENT_M, {
                    "discussionId": ids["repository"]["discussion"]["id"],
                    "body": spec["answer"] + content.SEED_FOOTER})
                ok("  ↳ answer posted")
            time.sleep(0.8)
        except GitHubError as exc:
            fail(f"discussion “{title[:40]}…”", exc.message[:90])
    return created


# ─────────────────────────────────────────────────────────────────── project ──
OWNER_ID_Q = """
query($login:String!){ user(login:$login){ id } organization(login:$login){ id } }"""

CREATE_PROJECT_M = """
mutation($ownerId:ID!,$title:String!){
  createProjectV2(input:{ownerId:$ownerId,title:$title}){ projectV2 { id number url } }
}"""

CREATE_FIELD_M = """
mutation($projectId:ID!,$name:String!,$options:[ProjectV2SingleSelectFieldOptionInput!]!){
  createProjectV2Field(input:{projectId:$projectId,dataType:SINGLE_SELECT,
                              name:$name,singleSelectOptions:$options}){
    projectV2Field { ... on ProjectV2SingleSelectField { id name } }
  }
}"""

CREATE_TEXT_FIELD_M = """
mutation($projectId:ID!,$name:String!){
  createProjectV2Field(input:{projectId:$projectId,dataType:TEXT,name:$name}){
    projectV2Field { ... on ProjectV2Field { id name } }
  }
}"""

ADD_ITEM_M = """
mutation($projectId:ID!,$contentId:ID!){
  addProjectV2ItemById(input:{projectId:$projectId,contentId:$contentId}){ item { id } }
}"""

ISSUE_NODE_Q = """
query($owner:String!,$name:String!,$number:Int!){
  repository(owner:$owner,name:$name){ issue(number:$number){ id } }
}"""

FIELDS = [
    ("Phase", ["P0 Harness", "P1 Baseline", "P2 Retrieval", "P3 Context", "P4 Evaluation",
               "P5 Cost", "P6 Agentic", "P7 Hardening"]),
    ("Effort", ["S <1d", "M 2-3d", "L ~1w", "XL cohort"]),
    ("Cohort", ["C1", "C2", "faculty", "open"]),
    ("Risk", ["low", "medium", "high"]),
]


def create_project(owner, repo, issues, dry):
    if dry:
        skip("project board", "would create 'Advanced RAG — Delivery' with 5 custom fields")
        return
    try:
        ids = graphql(OWNER_ID_Q, {"login": owner})
    except GitHubError as exc:
        warn("project board", f"cannot resolve owner — {exc.message[:80]}")
        return
    owner_id = (ids.get("organization") or ids.get("user") or {}).get("id")
    if not owner_id:
        warn("project board", "owner id not resolvable")
        return

    try:
        out = graphql(CREATE_PROJECT_M,
                      {"ownerId": owner_id, "title": "Advanced RAG — Delivery"})
        project = out["createProjectV2"]["projectV2"]
        ok("project board", project["url"])
    except GitHubError as exc:
        warn("project board", f"skipped — {exc.message[:110]}")
        print("      A classic PAT with the `project` scope, or a fine-grained token with")
        print("      account permission Projects: read/write, is required to create boards.")
        print("      Everything else in this script has still run. Create the board manually")
        print("      following docs/PROJECT-BOARD.md — it takes about five minutes.")
        return

    for name, options in FIELDS:
        try:
            graphql(CREATE_FIELD_M, {
                "projectId": project["id"], "name": name,
                "options": [{"name": o, "description": "", "color": "GRAY"} for o in options]})
            ok(f"  field {name}", f"{len(options)} options")
        except GitHubError as exc:
            warn(f"  field {name}", exc.message[:80])
    try:
        graphql(CREATE_TEXT_FIELD_M, {"projectId": project["id"], "name": "Metric moved"})
        ok("  field Metric moved", "text — the field that makes the board worth keeping")
    except GitHubError as exc:
        warn("  field Metric moved", exc.message[:80])

    added = 0
    for number, _title, _state in issues:
        try:
            node = graphql(ISSUE_NODE_Q, {"owner": owner, "name": repo, "number": number})
            graphql(ADD_ITEM_M, {"projectId": project["id"],
                                 "contentId": node["repository"]["issue"]["id"]})
            added += 1
            time.sleep(0.4)
        except GitHubError as exc:
            warn(f"  add #{number}", exc.message[:70])
    ok("  items", f"{added} issues added to the board")


# ────────────────────────────────────────────────────────────────────── main ──
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="", help=f"comma separated: {','.join(STEPS)}")
    ap.add_argument("--skip", default="", help="comma separated")
    args = ap.parse_args()

    wanted = set(args.only.split(",")) if args.only else set(STEPS)
    wanted -= set(args.skip.split(",")) if args.skip else set()

    print(f"\n\033[1mProvisioning {args.owner}/{args.repo}\033[0m"
          + ("  \033[33m(dry run)\033[0m" if args.dry_run else ""))

    try:
        repo_info = request("GET", f"/repos/{args.owner}/{args.repo}")
        print(f"  repository found · {repo_info['visibility']} · "
              f"default branch {repo_info['default_branch']}\n")
    except GitHubError as exc:
        print(f"\n\033[31mCannot reach {args.owner}/{args.repo}: {exc.message}\033[0m")
        print("\nCreate it first:")
        print(f"  gh repo create {args.owner}/{args.repo} --public "
              f"--description 'Runnable retrieval/RAG/evaluation curriculum'")
        print("  …or at https://github.com/new")
        return 1

    milestones, issues = {}, []
    if "settings" in wanted:
        print("\033[1mRepository settings\033[0m")
        configure_repository(args.owner, args.repo, args.dry_run)
    if "labels" in wanted:
        print("\n\033[1mLabels\033[0m")
        create_labels(args.owner, args.repo, args.dry_run)
    if "milestones" in wanted:
        print("\n\033[1mMilestones\033[0m")
        milestones = create_milestones(args.owner, args.repo, args.dry_run)
    if "issues" in wanted:
        print("\n\033[1mIssues\033[0m")
        if not milestones:
            milestones = {m["title"]: m["number"] for m in request(
                "GET", f"/repos/{args.owner}/{args.repo}/milestones?state=all&per_page=100")}
        issues = create_issues(args.owner, args.repo, milestones, args.dry_run)
    if "discussions" in wanted:
        print("\n\033[1mDiscussions\033[0m")
        create_discussions(args.owner, args.repo, args.dry_run)
    if "project" in wanted:
        print("\n\033[1mProject board\033[0m")
        if not issues and not args.dry_run:
            issues = [(i["number"], i["title"], i["state"]) for i in request(
                "GET", f"/repos/{args.owner}/{args.repo}/issues?state=all&per_page=100")
                if "pull_request" not in i]
        create_project(args.owner, args.repo, issues, args.dry_run)

    print(f"\n\033[1mDone.\033[0m  https://github.com/{args.owner}/{args.repo}")
    print("\nManual steps the API cannot do:")
    print("  1. Settings → Discussions → create the custom categories listed above")
    print("     (Design Reviews, Reading Club, Interview Prep) and set Q&A to answerable")
    print("  2. Settings → Pages → source: GitHub Actions   (enables the notebook site)")
    print("  3. Pin 2–3 discussions and 3–4 issues")
    print("  4. Add a repository social preview image (Settings → General)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
