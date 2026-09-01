#!/usr/bin/env python3
"""Create discussions from JSON specs, with labels, replies and a marked answer.

This repository has nine discussion categories and GitHub provides no API to add
more — there is no category mutation in the GraphQL schema, confirmed by
introspection. Rather than leave the structure unbuilt, threads carry a **title
prefix** and a **label** that together do what a tenth category would have done:
they make a set of threads findable, filterable and visually distinct.

    [clinic · EX-04]   ...   label: clinic          -> Q&A
    [maths]            ...   label: maths           -> Q&A
    [errata]           ...   label: errata          -> Q&A
    [solution · EX-04] ...   label: solution        -> Show and Tell
    [negative result]  ...   label: negative-result -> Show and Tell
    [round · <shape>]  ...   label: interview-round -> Interview Prep
    [office hours · <date>]  label: office-hours    -> Announcements

Spec files are JSON:

    {
      "category": "q-a",
      "title": "[clinic · EX-04] ...",
      "labels": ["clinic", "type: exercise"],
      "body": "...",
      "answer": 2,                # 1-based index into comments; Q&A-format only
      "comments": [ {"body": "...", "replies": [{"body": "..."}]} ]
    }

Usage:
    python scripts/create_thread.py threads/clinic/*.json [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

OWNER, REPO = "akash-coded", "nanorag"
DELAY_COMMENT = 2.5
DELAY_THREAD = 12.0

Q_META = """
query($o:String!,$r:String!){
  repository(owner:$o,name:$r){
    id
    discussionCategories(first:30){ nodes{ id slug isAnswerable } }
    labels(first:100){ nodes{ id name } } } }
"""
M_CREATE = """
mutation($repo:ID!,$cat:ID!,$t:String!,$b:String!){
  createDiscussion(input:{repositoryId:$repo, categoryId:$cat, title:$t, body:$b}){
    discussion{ id number url } } }
"""
M_COMMENT = """
mutation($d:ID!,$b:String!,$p:ID){
  addDiscussionComment(input:{discussionId:$d, body:$b, replyToId:$p}){
    comment{ id url } } }
"""
M_ANSWER = """
mutation($id:ID!){ markDiscussionCommentAsAnswer(input:{id:$id}){ clientMutationId } }
"""
M_LABEL = """
mutation($l:[ID!]!,$t:ID!){
  addLabelsToLabelable(input:{labelIds:$l, labelableId:$t}){ clientMutationId } }
"""


def graphql(query: str, **variables) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            continue
        if isinstance(value, list):
            for item in value:
                cmd += ["-f", f"{key}[]={item}"]
        else:
            cmd += (["-F", f"{key}={value}"] if isinstance(value, int)
                    else ["-f", f"{key}={value}"])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"graphql failed: {proc.stderr.strip()}")
    payload = json.loads(proc.stdout)
    if "errors" in payload:
        raise RuntimeError(f"graphql errors: {payload['errors']}")
    return payload["data"]


def load_meta() -> tuple[str, dict, dict, dict]:
    repo = graphql(Q_META, o=OWNER, r=REPO)["repository"]
    cats = {c["slug"]: c for c in repo["discussionCategories"]["nodes"]}
    labels = {l["name"]: l["id"] for l in repo["labels"]["nodes"]}
    return repo["id"], cats, labels, {}


def create(spec_path: pathlib.Path, repo_id, cats, labels, dry: bool) -> int:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    slug = spec["category"]
    if slug not in cats:
        raise RuntimeError(f"unknown category {slug!r}; have {sorted(cats)}")
    category = cats[slug]

    if spec.get("answer") and not category["isAnswerable"]:
        raise RuntimeError(
            f"{spec_path.name}: category {slug!r} is not answerable, so 'answer' cannot be set")

    print(f"  {spec['title'][:72]}")
    if dry:
        n = 1 + sum(1 + len(c.get('replies', [])) for c in spec.get("comments", []))
        print(f"     [{slug}] {len(spec.get('labels', []))} labels, {n} posts")
        return 0

    d = graphql(M_CREATE, repo=repo_id, cat=category["id"],
                t=spec["title"], b=spec["body"])["createDiscussion"]["discussion"]
    print(f"     {d['url']}")
    time.sleep(DELAY_COMMENT)

    wanted = [labels[name] for name in spec.get("labels", []) if name in labels]
    missing = [n for n in spec.get("labels", []) if n not in labels]
    if missing:
        print(f"     ! unknown labels skipped: {missing}", file=sys.stderr)
    if wanted:
        graphql(M_LABEL, l=wanted, t=d["id"])
        time.sleep(1.0)

    posted, tops = 1, []
    for comment in spec.get("comments", []):
        top = graphql(M_COMMENT, d=d["id"], b=comment["body"])["addDiscussionComment"]["comment"]
        tops.append(top)
        posted += 1
        time.sleep(DELAY_COMMENT)
        for reply in comment.get("replies", []):
            graphql(M_COMMENT, d=d["id"], b=reply["body"], p=top["id"])
            posted += 1
            time.sleep(DELAY_COMMENT)

    if spec.get("answer"):
        graphql(M_ANSWER, id=tops[spec["answer"] - 1]["id"])
        print("     * answer marked")
    return posted


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    repo_id, cats, labels, _ = load_meta()
    total = 0
    for i, path in enumerate(sorted(args.files)):
        try:
            total += create(path, repo_id, cats, labels, args.dry_run)
        except Exception as exc:
            print(f"  ! {path.name}: {exc}", file=sys.stderr)
        if i < len(args.files) - 1 and not args.dry_run:
            time.sleep(DELAY_THREAD)
    print(f"\n{total} posts created")
    return 0


if __name__ == "__main__":
    sys.exit(main())
