# Glossary

Every term used across the repository. **Edit freely** — a glossary that needs a pull request is a
glossary nobody fixes.

For mathematical notation specifically — symbols, what `α` and `k₁` mean, the `n` versus `n_boot`
distinction — see [`docs/90-reference/notation.md`](https://github.com/akash-coded/nanorag/blob/main/docs/90-reference/notation.md),
which is versioned because the code depends on it.

---

## A

**ACL pre-filter** — applying a permission predicate **inside** the retrieval query rather than
after it. Post-filtering collapses `k` unpredictably and leaks result counts.

**Abstention** — refusing to answer. Unsolved here by any retrieval-score threshold; best F1 0.38
at the real base rate.

**Analyzer** — the tokenizer plus normalisers that turn text into index terms. Silently decides
what is searchable. See [Common Errors](Common-Errors).

**Annotation-error floor** — the noise under every number when labels are human-made. A 2-point
delta may be annotator disagreement. This repo's synthetic corpus removes it by construction.

**ANN** — approximate nearest neighbour. Trades exact recall for speed.

## B

**BM25** — the standard lexical scoring function. Saturating term frequency, interpolated length
normalisation, log-odds IDF.

**Bootstrap, paired** — resampling questions with replacement, keeping both arms on the same
questions, to get a confidence interval on a delta.

## C

**Capex-shaped cost** — large, infrequent, plannable: backfill, index build, encoder upgrade. As
opposed to opex-shaped: generation, rerank, serving.

**Casebook thread** — a reconstructed discussion written for teaching, published by the maintainer
with illustrative roles and real numbers. Labelled `casebook`.

**Chunk** — the retrievable unit. A property of your documents, not a constant.

**Content hash** — the hash of a chunk's *normalised* text, used in its id so an edit changes
exactly one id.

**Context precision** — the share of packed chunks that are gold. Falls as `k` rises.

**Cross-encoder** — a reranker that attends over the query and document together. Accurate,
unscalable, so it runs last over ~100 candidates.

## D

**Dedup by document** — capping chunks per document for diversity. Systematically drops the second
hop of a same-document pair; a common cause of low multi-hop recall.

**Detection gap** — in a postmortem, *why a user found it before a test did*. The most valuable
line and the one people skip.

## E

**`embedder_tag`** — the encoder identity pinned to an index version. **One index version, one
tag.** A mixed index throws no exception.

**Evidence recall@k** — the share of a question's gold evidence in the packed context. Continuous.

**Eval set** — questions with gold evidence. The instrument. Building one is usually the first two
weeks of an engagement.

## F

**Frozen slice** — eval questions held back and never iterated against. A gain that appears on dev
and vanishes on frozen is overfitting.

**Full-chain recall** — 1 if **every** gold item for a question is packed, else 0. Binary, so
per-question variance is `p(1−p)` — maximal at the 0.5 accuracy where interesting systems sit.

**Full-chain recall@N** — the same conjunction measured over the candidate pool. The gap between
this and full-chain recall is **packing loss**.

**Fusion** — merging rankings from several retrievers. RRF consumes ranks; weighted fusion consumes
normalised scores and needs labels to fit.

## G

**Gold evidence** — the chunks that actually answer a question. Without it you cannot separate a
retrieval failure from a generation one.

## H

**HyDE** — generate a hypothetical answer, embed *that*, retrieve against it. Fixes vocabulary
mismatch between queries and documents. Measured here as inside the noise band, because this corpus
has no such mismatch.

## I

**IDF** — inverse document frequency, as a log-odds ratio. **Goes negative** above roughly half the
collection.

## K

**`k`** — chunks packed into the prompt. Usually the binding constraint on full-chain recall.

**`k_collapse`** — how many candidates were dropped between retrieval and packing. The only field
that reveals a post-retrieval filter eating the result set.

**κ (Cohen's kappa)** — agreement corrected for chance. Report it **with the base rate**; 90%
agreement on a 90/10 split is κ ≈ 0.44.

## N

**`n` vs `n_boot`** — `n` is how much uncertainty there is (set by the eval set). `n_boot` is how
carefully you measure it (set by your patience). Only `n` changes the interval width.

**Noise band** — the 95% interval of the paired bootstrap on the *unchanged* system. A delta inside
it is not a result.

**Null question** — a question the corpus cannot answer. Without them at their real base rate you
cannot measure abstention at all.

## P

**Packing loss** — evidence that reached the candidate pool and did not survive into the prompt.

**Pre-registration** — naming the primary metric **before** the number exists. The only thing
distinguishing shipping-on-the-primary-metric from picking-the-one-that-agreed-with-you.

## R

**Right by accident** — the answer was correct and the gold evidence was never retrieved. The model
answered from memory; retrieval contributed nothing. Detected against the **ungrounded baseline**.

**RRF** — reciprocal rank fusion, `Σ 1/(k + rank)`. A positional voting rule, closer to Borda count
than to a scoring function.

## S

**Slice** — a subset of the eval set by question type, query class or tenant. **An aggregate cannot
detect a failure confined to a minority class.**

**Stable chunk id** — `doc_id + ordinal + hash(normalised text)`. Stable against edits, not against
insertions.

## T

**Tombstone** — soft-deleting an orphaned chunk, compacted later. Requires stable ids to tell an
edited chunk from a moved one.

**Trace** — candidates, packed set, per-stage latency, config fingerprint. A trace that records the
answer is a log; one that records the decisions is evidence.

## U

**Ungrounded baseline** — the eval set scored with **no retrieved context at all**. Whatever it
scores is what the model already knew. Every `answer_correct` should be read against it, and almost
nobody computes it.

## W

**Winner's curse** — a delta that only just reached significance is more likely than not an
overestimate. Budget roughly double when sizing a follow-up. Measured here: `+0.0338` became
`+0.0116` when the eval set grew from 207 to 812.
