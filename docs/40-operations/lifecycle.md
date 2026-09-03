# The lifecycle, with this repository as the worked example

**[The board →](https://github.com/users/akash-coded/projects/13)** · 31 rows · filter by Phase, Kind, or any of three vocabularies

Most lifecycle diagrams are generic enough to be true of anything and therefore useful for
nothing. This one is different in one way: **every row points at a file, a workflow, a board or a
thread that exists in this repository.** The stages are the same eight any retrieval or
evaluation project goes through. The rows are what *this* project produced at each one.

## The eight phases, and what each hands to the next

| Phase | What has to be true to leave it | The artefact this repo produced |
|---|---|---|
| **0 · Frame** | The constraint that makes it hard is written down, with a falsifier | An [ADR template](../20-decisions/template.md) where *What would change this* is a required section |
| **1 · Discover** | You have read the corpus, not a summary of it | A corpus spec: track T1's capstone — what is in scope, what the retrievable unit is |
| **2 · Specify** | An eval set exists with **gold evidence**, nulls at the real base rate, a pre-registered primary metric, and a noise band measured on the *unchanged* system | [Notebook 02](../../notebooks/02_multihop_rag_use_case.ipynb), [`eval-baseline.json`](../../.github/eval-baseline.json), the [measurement PR template](../../.github/PULL_REQUEST_TEMPLATE/measurement.md) |
| **3 · Design** | Every non-obvious choice has an ADR naming the alternative that lost, and a review has said which parts survive | [Eight ADRs](../20-decisions/README.md), the [Design Reviews](https://github.com/akash-coded/nanorag/discussions/categories/design-reviews) category, the [review checklist](../60-cheatsheets/playbooks/design-review-checklist.md) |
| **4 · Build** | Each change moves one number and ships with its interval; the reference solution passes its own hidden checks and the starter does not | [`labs/test_labs.py`](../../labs/test_labs.py) in CI; the four challenge shapes in the [L.A.B. simulator](../80-lab/README.md) |
| **5 · Validate** | The primary metric clears the band; every slice clears *its own*; the judge is calibrated with κ *and its base rate*; the frozen slice agrees with dev | The [release gate playbook](../60-cheatsheets/playbooks/release-gate-playbook.md); lab [L12](../../labs/L12-release-gate/brief.md), which is that gate as code |
| **6 · Release** | A written decision — ship, do not ship, or *not yet measurable* — that someone outside the room can audit; branch protection on exactly the checks that run on every PR; untrusted input never reaches a shell | [ADR-0008](../20-decisions/0008-eval-gate-in-ci.md); the three-job [`discussion-lab.yml`](../../.github/workflows/discussion-lab.yml) |
| **7 · Operate** | Failures are reproducible after the fact; postmortems name the *detection gap*; what needs attention is on one board | [L11](../../labs/L11-replayable-trace/brief.md)'s trace, the [postmortem template](../../.github/ISSUE_TEMPLATE/incident_postmortem.yml), the [Repo Pulse](https://github.com/users/akash-coded/projects/12) and [Hands-on Tracker](https://github.com/users/akash-coded/projects/11) boards |

The dependency is real, not decorative. **L12 cannot be completed without T4's noise band, T5's
calibrated judge, T6's cost model and T7's trace** — the lab DAG enforces the lifecycle because
that dependency *is* the lesson.

## Four kinds of row

| Kind | What it is | Example on the board |
|---|---|---|
| **Artefact** | A thing a phase produces and the next phase consumes | *An eval set with gold evidence, not just gold answers* |
| **Gate** | A condition that must hold before you may leave the phase | *Every slice clears ITS OWN band* |
| **Practice** | A habit worth naming because its absence is how projects fail | *Rule out configuration before suspecting design* |
| **Signal** | An observable that tells you a phase is actually done, or has quietly come undone | *Gate override rate under one in ten* |

Gates are what most lifecycle documents omit, and they are the only rows that stop you doing
something. A lifecycle with no gates is a reading list.

## The same board in three other vocabularies

Teams arrive with a method already in their heads. Rather than argue, every row is also tagged
with where it sits in three of the current ones, so the board reads in whichever you use.

**AiDD — AI-Driven Development, six units.** *Intent before implementation* is phase 0–2 here:
the constraint, the spec, the eval set — written before a model is asked for anything. *Context
as an asset* is the corpus you actually read, the trace, the FAQ that links rather than copies.
*Right-sized process* is the pre-registered metric and the noise band: enough rigour that a
number means something, and no ceremony past that. *Slicing the work* is one number per PR.
*The review seam* is every gate. *Reading the failure* is the four verdicts, the detection gap,
and the grid search in [#4](https://github.com/akash-coded/nanorag/issues/4) that lost — which
is what promoted the diagnosis from weights to features.

**BMAD — Analysis, Planning, Solutioning, Implementation.** Phases 0–1 are Analysis; 2 is
Planning; 3 is Solutioning; 4–7 are Implementation. BMAD's distinctive move is the agentic
hand-off between roles with a written artefact at each seam — which is exactly what the
Artefact rows are, and why they are named as things rather than as activities.

**AI-DLC — Inception, Construction, Operations.** Inception is 0–3, Construction 4–5, Operations
6–7. AI-DLC's emphasis is that Operations is not an afterthought: the trace, the pulse board and
the tracker are designed in phase 7's rows, not bolted on after release.

The mapping is deliberately loose at the edges. A gate like *the judge is calibrated* sits in
Validate here, in Implementation for BMAD, in Construction for AI-DLC — and it is the same row.
**The vocabularies differ on where to draw lines; they agree on what has to be true.**

## What this board is for

- **Starting a similar project:** read down the Artefact column. That is the deliverable list.
- **Reviewing one:** read the Gate rows. Ask which ones have been passed and how you would know.
- **Explaining why this repo is shaped the way it is:** every row's *In this repo* field is the
  reason that file or workflow exists.
- **Arguing with it:** open a thread in
  [Design Reviews](https://github.com/akash-coded/nanorag/discussions/categories/design-reviews).
  Several rows are opinions with evidence attached, and evidence is the only thing that moves them.
