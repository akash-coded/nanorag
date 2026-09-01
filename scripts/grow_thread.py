#!/usr/bin/env python3
"""Post a nested reply tree onto an existing discussion, and mark an answer.

The seeding script that created these discussions could only post top-level
comments, which is why every thread in the repository read as a monologue. The
piece that makes a thread a conversation is `replyToId`: a comment that replies
to another comment nests under it, and that nesting is what carries "someone was
wrong, and here is the correction".

Thread files are JSON:

    {
      "discussion": 29,
      "answer": 4,                  # 1-based index into "comments"; optional
      "comments": [
        {"body": "...", "replies": [{"body": "..."}, ...]},
        ...
      ]
    }

Usage:
    python scripts/grow_thread.py threads/29-*.json [--dry-run]

Authentication is whatever `gh` is logged in as; no token is read from the
environment and none is written to disk.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

OWNER, REPO = "akash-coded", "nanorag"

# GitHub applies a secondary rate limit to rapid content creation. These delays
# keep a full seeding run inside it; going faster earns a multi-minute block.
DELAY_COMMENT = 2.5
DELAY_THREAD = 20.0

Q_DISCUSSION = """
query($o:String!,$r:String!,$n:Int!){
  repository(owner:$o,name:$r){ discussion(number:$n){ id title url
    comments(first:50){ nodes{ id } } } } }
"""
M_COMMENT = """
mutation($d:ID!,$b:String!,$p:ID){
  addDiscussionComment(input:{discussionId:$d, body:$b, replyToId:$p}){
    comment{ id url } } }
"""
M_ANSWER = """
mutation($id:ID!){
  markDiscussionCommentAsAnswer(input:{id:$id}){ clientMutationId } }
"""


def graphql(query: str, **variables) -> dict:
    """Call the GraphQL API through `gh`, which already holds credentials."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            continue  # omitted, so replyToId defaults to a top-level comment
        # -F sends a typed value (ints stay ints); -f always sends a string, which
        # GraphQL rejects for Int! variables.
        cmd += (["-F", f"{key}={value}"] if isinstance(value, int)
                else ["-f", f"{key}={value}"])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"graphql failed: {proc.stderr.strip()}")
    payload = json.loads(proc.stdout)
    if "errors" in payload:
        raise RuntimeError(f"graphql errors: {payload['errors']}")
    return payload["data"]


def grow(path: pathlib.Path, dry_run: bool = False) -> int:
    spec = json.loads(path.read_text(encoding="utf-8"))
    number = spec["discussion"]
    discussion = graphql(Q_DISCUSSION, o=OWNER, r=REPO, n=number)["repository"]["discussion"]
    print(f"#{number} {discussion['title'][:64]}")

    # Comments already on the thread can be replied to as well, so a tree can be
    # grafted onto an existing answer instead of restarting the conversation.
    existing = [c["id"] for c in discussion["comments"]["nodes"]]

    posted = 0
    tops: list[dict] = []
    for comment in spec["comments"]:
        under = comment.get("under_existing")
        if under is not None:
            parent = existing[under]
            if dry_run:
                tops.append({"id": "dry-run"})
                print(f"   -> under existing[{under}] ({len(comment['body'])} chars)")
            else:
                made = graphql(M_COMMENT, d=discussion["id"], b=comment["body"], p=parent)
                tops.append(made["addDiscussionComment"]["comment"])
                posted += 1
                print(f"   -> under existing[{under}]")
                time.sleep(DELAY_COMMENT)
            for reply in comment.get("replies", []):
                if dry_run:
                    print(f"      -> reply ({len(reply['body'])} chars)")
                    continue
                graphql(M_COMMENT, d=discussion["id"], b=reply["body"], p=parent)
                posted += 1
                print("      -> reply")
                time.sleep(DELAY_COMMENT)
            continue
        if dry_run:
            tops.append({"id": "dry-run"})
            print(f"   + top-level ({len(comment['body'])} chars)")
        else:
            top = graphql(M_COMMENT, d=discussion["id"], b=comment["body"])
            top = top["addDiscussionComment"]["comment"]
            tops.append(top)
            posted += 1
            print(f"   + {top['url'].rsplit('#', 1)[-1]}")
            time.sleep(DELAY_COMMENT)
        for reply in comment.get("replies", []):
            if dry_run:
                print(f"      -> reply ({len(reply['body'])} chars)")
                continue
            graphql(M_COMMENT, d=discussion["id"], b=reply["body"], p=tops[-1]["id"])
            posted += 1
            print("      -> reply")
            time.sleep(DELAY_COMMENT)

    # "answer" is 1-based into spec["comments"]; "answer_existing" marks a comment
    # that was already on the thread, which is the common case here — the original
    # reply was good, it simply was never marked.
    if spec.get("answer_existing") is not None and not dry_run:
        graphql(M_ANSWER, id=existing[spec["answer_existing"]])
        print(f"   * marked existing comment {spec['answer_existing']} as the answer")

    index = spec.get("answer")
    if index and not dry_run:
        graphql(M_ANSWER, id=tops[index - 1]["id"])
        print(f"   * marked comment {index} as the answer")
    elif index:
        print(f"   * would mark comment {index} as the answer")
    return posted


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    for i, path in enumerate(args.files):
        try:
            total += grow(path, args.dry_run)
        except Exception as exc:  # keep going; one bad thread must not lose the rest
            print(f"   ! {path.name}: {exc}", file=sys.stderr)
        if i < len(args.files) - 1 and not args.dry_run:
            time.sleep(DELAY_THREAD)
    print(f"\n{total} comments posted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
