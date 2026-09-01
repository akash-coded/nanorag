# 🪞 The Reranker Mirror

> **The question:** will this second stage add anything?

The shortest useful rule in retrieval:

> **A reranker only helps if it can see something the first stage could not.**
> A reranker over the same signals as the retriever is an expensive identity function —
> and occasionally worse than one.

## The mirror test

Write the two feature sets side by side. If the right column is a subset of the left, stop.

| First stage already uses | Your reranker uses | Verdict |
|---|---|---|
| Term overlap, IDF, length | Term overlap, proximity, length | 🪞 **Mirror.** Nothing new. Will not help |
| BM25 + dense cosine | Coverage, phrase, title match | 🪞 **Mirror.** All lexical; the dense signal is *discarded* |
| BM25 + dense cosine | `maxsim`, `doc_cosine`, cross-attention | ✅ **New information.** Worth measuring |
| BM25 only | Dense cosine | ✅ New — though cheaper as a fusion leg |
| Anything | Recency, authority, click logs | ✅ New — **and orthogonal**, which is the best case |

## Why a mirror can be *worse* than nothing

This is the part that surprises people. Measured here:

```text
k=8   rerank=none    ER 0.849   FCR 0.614
k=8   rerank=cross   ER 0.752   FCR 0.523    <- worse
```

The scorer used lexical features only. Applied to a **hybrid** candidate list, it re-sorted by
lexical signal alone and **threw away the dense contribution** that fusion had just added. It was
a worse BM25 applied on top of a well-fused list.

A mirror does not merely fail to add information. **It destroys the information the stage before
it produced.**

## The diagnostic order that saved a week

From [#4](https://github.com/akash-coded/nanorag/issues/4), and it generalises far past reranking:

1. **Rule out configuration before suspecting design.** Grid-search the weights. Forty minutes.
2. **The search failing is the finding.** If no weight vector wins, the problem is not the
   weights — it is the features.
3. Only then change the design.

> **Rule out configuration before you suspect design.** Configuration is cheap to test and is
> usually the answer. When it is not the answer, the fact that it is not is itself strong
> evidence.

## Depth matters as much as features

A reranker at `depth=k` has nothing to reorder — it can only permute the chunks that were already
going to be packed. Rerank depth must **exceed** `k`, usually several times over, or the stage is
decorative regardless of its features.

## When this does not apply

**Latency-motivated reranking.** A cheap first stage retrieving 1,000 and an expensive second
stage scoring 50 can be the right *architecture* even with overlapping features, because the
point is spending compute where it matters. But be honest that you are buying speed, not quality
— and measure that quality did not drop.

---

**Practise:** [EX-14 — Beat the reranker](../../30-learning/exercises/ex-14-beat-the-reranker.md) ·
**Measured in:** [#4](https://github.com/akash-coded/nanorag/issues/4) · **Stated in:** [#27](https://github.com/akash-coded/nanorag/discussions/27)
