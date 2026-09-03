#!/usr/bin/env python3
"""Seed the Lifecycle Reference board with nanorag's own artefacts, gates and signals.

The board answers "how should a project like this move from idea to operation",
and it answers with THIS repository's real outputs rather than generic advice --
every row points at a file, a workflow, a board or a thread that exists. Each
row is also placed in AiDD, BMAD and AI-DLC vocabulary, so a team that uses any
of those can read the same board in its own terms.

Idempotent: upserts by title. Run once; rerun after adding rows.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import boards  # noqa: E402

R = "https://github.com/akash-coded/nanorag/blob/main"
A, G, P, S = "Artefact", "Gate", "Practice", "Signal"

# (phase, kind, title, aidd, bmad, aidlc, in-this-repo)
ROWS = [
 # ── 0 Frame
 ("0 Frame", P, "Write the constraint that makes it hard before writing anything else",
  "1 Intent before implementation", "Analysis", "Inception",
  f"Every design review and lab brief opens with a Look section -- evidence first. {R}/docs/80-lab/README.md"),
 ("0 Frame", A, "A one-page problem statement with the falsifier attached",
  "1 Intent before implementation", "Analysis", "Inception",
  f"ADR template: 'What would change this' is a required section. {R}/docs/20-decisions/template.md"),
 ("0 Frame", G, "Can a user know a document exists but not read it? Answered before design",
  "1 Intent before implementation", "Analysis", "Inception",
  f"The single question that decides the retrieval architecture. {R}/docs/60-cheatsheets/frameworks/inference-channel-audit.md"),
 # ── 1 Discover
 ("1 Discover", P, "Read fifty documents and fifty real queries before touching retrieval",
  "2 Context as an asset", "Analysis", "Inception",
  f"Week 1 of the engagement playbook. {R}/docs/60-cheatsheets/playbooks/first-30-days.md"),
 ("1 Discover", A, "A corpus spec: what is in scope, and what the retrievable unit is",
  "2 Context as an asset", "Analysis", "Inception",
  f"Track T1's capstone artefact. Produced by L01-L02 and the C01 challenge. {R}/labs/README.md"),
 ("1 Discover", S, "Twenty chunks read cold: can you tell what each is about?",
  "2 Context as an asset", "Analysis", "Inception",
  f"The ten-minute precondition test that decides whether contextual chunking has anything to fix. {R}/docs/60-cheatsheets/frameworks/precondition-test.md"),
 # ── 2 Specify
 ("2 Specify", A, "An eval set with gold EVIDENCE, not just gold answers, and nulls at the real base rate",
  "3 Right-sized process", "Planning", "Inception",
  f"Notebook 02 builds it; EX-04 practises it; without evidence labels the four verdicts are unreachable. {R}/notebooks/02_multihop_rag_use_case.ipynb"),
 ("2 Specify", A, "The primary metric, named before any number exists",
  "3 Right-sized process", "Planning", "Inception",
  f"Pre-registration in the PR template and eval-baseline.json. {R}/.github/PULL_REQUEST_TEMPLATE/measurement.md"),
 ("2 Specify", G, "A noise band measured on the UNCHANGED system",
  "3 Right-sized process", "Planning", "Inception",
  f"paired_bootstrap on the baseline. A delta is only interpretable against it. {R}/docs/30-learning/interview-prep/01-mathematical-foundations/paired-bootstrap-and-power.md"),
 ("2 Specify", S, "The ungrounded floor: what the model scores with no retrieval at all",
  "3 Right-sized process", "Planning", "Inception",
  f"Every answer_correct is read against it; it is how 'right by accident' is detected. {R}/docs/60-cheatsheets/frameworks/four-verdicts.md"),
 # ── 3 Design
 ("3 Design", A, "An ADR per non-obvious decision, with the alternative that lost and a falsifier",
  "1 Intent before implementation", "Solutioning", "Inception",
  f"Eight so far, all with 'What would change this'. {R}/docs/20-decisions/README.md"),
 ("3 Design", G, "Design review: constraints in, critique out, synthesis marked as the answer",
  "5 The review seam", "Solutioning", "Inception",
  f"Design Reviews category; the checklist reviewers run. {R}/docs/60-cheatsheets/playbooks/design-review-checklist.md"),
 ("3 Design", P, "Rule out configuration before suspecting design",
  "6 Reading the failure", "Solutioning", "Inception",
  "The grid search in #4 that lost is what promoted the diagnosis from weights to features. https://github.com/akash-coded/nanorag/issues/4"),
 ("3 Design", A, "A cost model whose inputs are named: corpus size, change rate, volume, dimension",
  "3 Right-sized process", "Solutioning", "Inception",
  f"Track T6 capstone. Generation tokens are ~31% of the bill. {R}/docs/60-cheatsheets/frameworks/cost-iceberg.md"),
 # ── 4 Build
 ("4 Build", P, "Slice work so each PR moves one number and ships with its interval",
  "4 Slicing the work", "Implementation", "Construction",
  f"The measurement PR template requires every metric, cleared or not. {R}/.github/PULL_REQUEST_TEMPLATE/measurement.md"),
 ("4 Build", A, "An implementation with a measurement attached",
  "4 Slicing the work", "Implementation", "Construction",
  f"Track T3's capstone artefact. {R}/labs/README.md"),
 ("4 Build", G, "The reference solution passes its own hidden checks; the starter does not",
  "5 The review seam", "Implementation", "Construction",
  f"labs/test_labs.py, in CI on every change. A lab that cannot be completed is worse than no lab. {R}/labs/test_labs.py"),
 ("4 Build", P, "Blanks and bugs as teaching shapes, not only 'implement this'",
  "4 Slicing the work", "Implementation", "Construction",
  f"fill / fix / predict challenges: reading and reasoning, not just typing. {R}/docs/80-lab/README.md"),
 # ── 5 Validate
 ("5 Validate", G, "Primary metric clears the band; every slice clears ITS OWN band",
  "5 The review seam", "Implementation", "Construction",
  f"An aggregate cannot detect a failure confined to a minority class -- #1 nearly shipped that way. {R}/docs/60-cheatsheets/playbooks/release-gate-playbook.md"),
 ("5 Validate", G, "Judge calibrated: kappa WITH its base rate, self-consistency measured first",
  "5 The review seam", "Implementation", "Construction",
  f"Track T5 capstone; L09 and C06. 94% agreement is kappa 0.6 at 90/10 and 0.37 at 95/5. {R}/docs/60-cheatsheets/frameworks/calibration-triangle.md"),
 ("5 Validate", S, "Frozen slice agrees with dev slice",
  "6 Reading the failure", "Implementation", "Construction",
  "A gain that appears on dev and vanishes on frozen is overfitting, and it survives every other check."),
 ("5 Validate", P, "Report the negative result with the mechanism, not the technique",
  "6 Reading the failure", "Implementation", "Construction",
  f"ADR-0007, and the [negative result] threads in Show and Tell. {R}/docs/20-decisions/0007-report-negative-results.md"),
 # ── 6 Release
 ("6 Release", A, "A decision record: ship, do not ship, or not yet measurable",
  "5 The review seam", "Implementation", "Operations",
  f"Track T8's capstone; L12 produces one. {R}/labs/L12-release-gate/brief.md"),
 ("6 Release", G, "Branch protection on the checks that run on EVERY PR, and only those",
  "3 Right-sized process", "Implementation", "Operations",
  "Requiring a path-filtered check blocks PRs that do not touch the path -- which is how protection gets disabled a week later."),
 ("6 Release", G, "Untrusted input never reaches a shell, and code from a comment runs with no credentials",
  "5 The review seam", "Implementation", "Operations",
  f"discussion-lab.yml: triage {{}} / execute {{}} in docker --network=none / post discussions:write. {R}/.github/workflows/discussion-lab.yml"),
 ("6 Release", S, "Gate override rate under one in ten",
  "6 Reading the failure", "Implementation", "Operations",
  f"Above that the threshold is wrong and the fix is to grow the eval set, not loosen the gate. ADR-0008. {R}/docs/20-decisions/0008-eval-gate-in-ci.md"),
 # ── 7 Operate
 ("7 Operate", A, "A trace that records the decisions -- candidates, packed set, config fingerprint, k_collapse",
  "2 Context as an asset", "Implementation", "Operations",
  f"Track T7's capstone; L11 builds it. A trace that records the answer is a log. {R}/labs/L11-replayable-trace/brief.md"),
 ("7 Operate", P, "Postmortems name the DETECTION GAP: why a person found it before a test did",
  "6 Reading the failure", "Implementation", "Operations",
  f"The required field on the incident template. {R}/.github/ISSUE_TEMPLATE/incident_postmortem.yml"),
 ("7 Operate", S, "Unanswered Q&A older than 48h, hot threads, content churn -- on one board",
  "2 Context as an asset", "Implementation", "Operations",
  "The Repo Pulse board, refreshed every six hours. https://github.com/users/akash-coded/projects/12"),
 ("7 Operate", S, "Who has attempted what, how many tries, who is stuck past the due date",
  "6 Reading the failure", "Implementation", "Operations",
  "The Hands-on Tracker: one row per learner per item, moved by the workflows. https://github.com/users/akash-coded/projects/11"),
 ("7 Operate", P, "Answered threads harvested into the FAQ; the thread stays the source of truth",
  "2 Context as an asset", "Implementation", "Operations",
  f"faq.yml weekly; the FAQ links rather than copies. {R}/docs/90-reference/faq.md"),
]


def main() -> int:
    boards.require_budget(400, 'the lifecycle seed')
    board = boards.Board(boards.LIFECYCLE)
    for phase, kind, title, aidd, bmad, aidlc, note in ROWS:
        _, created = board.upsert(title, **{"Phase": phase, "Kind": kind, "AiDD unit": aidd,
                                            "BMAD phase": bmad, "AI-DLC phase": aidlc,
                                            "In this repo": note})
        print(f"  {'+' if created else '~'} [{phase}] {kind:<9} {title[:60]}")
    print(f"{len(ROWS)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
