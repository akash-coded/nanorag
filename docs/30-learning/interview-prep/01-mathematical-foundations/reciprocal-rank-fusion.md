# Reciprocal rank fusion — why `1/(k + rank)`

> **As asked:** *"You fuse a BM25 list and a dense list with RRF. Why that formula? Why not
> `1/rank`, or the nDCG discount? And where does 60 come from?"*

## The constraint that rules out scoring

BM25 returns values in roughly `8–25`. Cosine returns values in `[-1, 1]`. There is no
principled way to add them, and normalising them requires knowing each retriever's score
distribution — which drifts with the corpus.

The deeper reason is that **any monotone transform of a retriever's scores leaves its ranking
unchanged.** The scores therefore carry retriever-specific information that is not comparable
across retrievers; the *ranking* is the only part that is. So fusion without labelled
calibration data must consume ranks.

The economics framing, which is worth having ready: this is the **interpersonal comparison of
utility** problem. Two retrievers' scores are two agents' utilities, and Arrow's setting tells
you that aggregating preferences without comparable utilities means using a **positional voting
rule**.

## The three properties, and the formula that satisfies them

**1 · Consumes ranks, not scores.** Above.

**2 · Steeply decreasing but bounded.** Rank 1 should beat rank 50 — but not so decisively that
one retriever's top hit wins outright. What you want is that a document ranked 3rd by *both*
retrievers beats one ranked 1st by one and 200th by the other.

**3 · Requires no training.** Nothing fitted to labels means nothing to overfit and nothing to
re-tune on corpus drift.

$$
\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}
$$

## What `k` does

`k` is a **damping constant**, and reading the two extremes is the fastest way to see it:

| `k` | Weights for ranks 1, 2, 3 | Behaviour |
|---|---|---|
| `0` | `1.000, 0.500, 0.333` | Rank 1 worth twice rank 2. One confident retriever dominates the merge |
| `60` | `0.0164, 0.0161, 0.0159` | Nearly equal. What matters is **how many** retrievers ranked it, not how highly |

So `k = 60` deliberately makes RRF a **voting scheme rather than a scoring scheme**. That is the
design intent, and it is why RRF is robust when one leg is unreliable.

`60` itself has no derivation. It is an empirical constant from Cormack, Clarke and Buettcher
(2009), fitted on TREC, and the result is insensitive across roughly `30–120`. Swept on this
corpus:

```text
 k     evidence_recall
  0          0.781
 10          0.796
 30          0.802
 60          0.804
120          0.803
300          0.799
```

**+0.023 across the entire sweep.** Fusion weight `α` moves the same metric by `+0.061`. If you
are going to tune one parameter, it is not this one.

## Why not the alternatives

| Candidate | Fails |
|---|---|
| `1/rank` | Property 2. Rank 1 is worth ten times rank 10; one confident retriever dominates. This is exactly what `k` exists to prevent |
| `1/log(r+1)` | Nothing, really — it is the nDCG discount and it is defensible. It decays more slowly in the tail. Empirically similar; RRF won on adoption, not on a proof |
| `n − rank` (Borda) | Nothing in principle, but it is linear, so it weights the tail as heavily as the head. RRF is Borda with a convex weighting that cares more about the top |
| Normalised score sum | Property 1 and 3. Needs calibration data, and the calibration drifts |

## What a strong answer adds

**RRF is a positional voting rule, closer to Borda count than to a scoring function.** Once you
say that, "why not just add the scores" answers itself.

**And know when it loses.** RRF gives every leg an equal vote. If one retriever is materially
weaker, an equal vote drags the merge toward it. On this corpus the dense leg is weak, RRF loses
to weighted fusion, and the notebook says "default to RRF" three sections earlier — an apparent
contradiction argued out in
[discussion #30](https://github.com/akash-coded/nanorag/discussions/30). The resolution is a
procedure rather than a preference: **default to RRF because it needs no labels; measure once you
have them.**

## Measure it here

`nanorag/retrieve.py` implements both `rrf()` and `weighted_fusion()`.
[Notebook 04](https://github.com/akash-coded/nanorag/blob/main/notebooks/04_retrieval_methods_and_reranking.ipynb)
§4.9 sweeps both. [EX-13](../../exercises/ex-13-route-by-query-class.md) asks you to route `α`
by query class, which is where the interesting failure lives.
