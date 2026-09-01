# Extension project — Does it transfer?

> **The claim under test:** *"The methodology transfers; the constants do not."*
>
> This repository says that sentence in six places. It has never been tested, because
> everything here runs on a corpus this repository generated itself.

**[Board →](https://github.com/users/akash-coded/projects/5)** · 7 phases · milestones `E0`–`E6`

## Why this project exists

Every number in nanorag was measured on a synthetic corpus built from a fact graph. That choice
is deliberate and defended in [ADR-0002](../20-decisions/0002-synthetic-corpus.md): gold labels
are true by construction, so there is no annotation-error floor under any result.

It also means **every finding here has an untested precondition.** The three contradicting
results in the README, the reranker result, the abstention result — each one might be a property
of retrieval, or a property of *this corpus*. Nothing currently distinguishes those.

That is a real weakness, and the honest response is not to caveat it harder. It is to go and
find out.

## The deliverable

**A transfer report** stating, for each claim this repository makes, whether it survived contact
with real data. Three outcomes are all acceptable and one is the most interesting:

| Outcome | What it means |
|---|---|
| ✅ **Reproduced** | The finding is about retrieval, not about our corpus. It generalises |
| ❌ **Contradicted** | The finding was an artefact of the fact-graph construction. **The most valuable outcome** — it says exactly what the synthetic corpus cannot teach |
| ➖ **Inconclusive** | Neither corpus can distinguish it. Says something about the metric, not the technique |

A project that finds everything reproduces has probably not tried hard enough. A project that
finds nothing reproduces has found something important about synthetic corpora.

## The phases

| | Phase | Exit criterion |
|---|---|---|
| **E0** | [Portability](https://github.com/akash-coded/nanorag/milestone/9) | The record schema and metrics run against a corpus this repository did not generate |
| **E1** | [Real corpus](https://github.com/akash-coded/nanorag/milestone/10) | MultiHop-RAG ingested behind the same interfaces; a baseline with intervals |
| **E2** | [Replicate findings](https://github.com/akash-coded/nanorag/milestone/11) | Each of the four findings reproduced, contradicted, or shown inconclusive — **with the number** |
| **E3** | [Modern encoder](https://github.com/akash-coded/nanorag/milestone/12) | `α` re-tuned, per-class deltas published, [ADR-0003](../20-decisions/0003-lsa-default-encoder.md)'s falsifier actually tested |
| **E4** | [Real ANN](https://github.com/akash-coded/nanorag/milestone/13) | Filtered recall measured, not assumed |
| **E5** | [Real judge](https://github.com/akash-coded/nanorag/milestone/14) | κ with its base rate, two bias probes in CI |
| **E6** | [Publish](https://github.com/akash-coded/nanorag/milestone/15) | The transfer report |

## The rules

They are the same rules as the parent project, and one more.

1. **Every claim ships with an interval.** A point estimate is not a result.
2. **Pre-register the metric.** Name it before the number exists, or you cannot tell shipping
   from cherry-picking.
3. **Slice by class.** An aggregate cannot detect a failure confined to a minority class — that
   is how [#1](https://github.com/akash-coded/nanorag/issues/1) nearly shipped.
4. **New:** every finding is filed against the board's **`Transfers?`** field — `reproduced`,
   `contradicted`, or `inconclusive`. The distribution of that field *is* the transfer report.

## The honest risks

**MultiHop-RAG has an annotation-error floor.** Its labels are human-made, so a 2-point
difference may be annotator disagreement. That is the cost of realism and it must be stated
wherever a number from it appears — it is exactly the floor ADR-0002 removed by construction.

**A contradicted finding is ambiguous.** If a result does not reproduce, the cause could be the
corpus, the encoder, the chunking, or the labels. **Change one thing at a time**, which is why
the phases are ordered and why E3 comes after E2.

**This project can fail usefully.** If E1 shows the harness cannot ingest a real corpus without
substantial rewriting, that is a finding about the harness, and it belongs in the report as
loudly as any metric.

---

**Tracking:** [board](https://github.com/users/akash-coded/projects/5) ·
**Parent roadmap:** [`P0`–`P7`](https://github.com/akash-coded/nanorag/milestones) ·
**Discuss:** [Design Reviews](https://github.com/akash-coded/nanorag/discussions/categories/design-reviews)
