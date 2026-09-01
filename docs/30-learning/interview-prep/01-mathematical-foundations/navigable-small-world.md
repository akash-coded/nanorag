# Navigable small-world graphs, and the failure that returns well-formed answers

> **As asked:** *"Greedy search on an HNSW graph is roughly logarithmic. Why? And what breaks
> the guarantee in production?"*

## Why greedy search works at all

A k-NN graph connects each node to its nearest neighbours. Greedy search — move to whichever
neighbour is closer to the query, stop when none is — walks downhill toward the query.

On a **pure** k-NN graph that walk gets stuck. Every edge is short, so the search descends into
the nearest local basin and cannot leave it, because leaving requires a step that temporarily
increases distance. Every edge in the graph is correct; **the graph as a whole is unusable.**

Kleinberg's result supplies the missing ingredient: add long-range links, sampled with
probability proportional to `d^{-r}` for the right exponent `r`, and greedy routing becomes
`O(log² n)`. The intuition is that at every scale there is an edge that roughly halves the
remaining distance — the search takes big steps while far away and small ones when close.

HNSW gets the same effect structurally instead of stochastically: a hierarchy of layers, sparse
and long-range at the top, dense and short-range at the bottom. Enter at the top, descend.

## What actually breaks it

**1 · No long-range links at all.** This repository shipped it. Issue
[#2](https://github.com/akash-coded/nanorag/issues/2): `_matrix()` built a pure 16-NN graph, and
after the corpus grew from 1,186 to 2,430 chunks recall collapsed:

```text
ef=8     recall@20 = 0.00
ef=64    recall@20 = 0.00     <- should be near 1.0
ef=512   recall@20 = 0.55
```

The diagnostic worth carrying: **recall that degrades gracefully with `ef` means the visit
budget is too small; recall pinned at zero regardless of `ef` means the graph is disconnected.**
Different problems, different fixes, and it is a one-line distinction that saves a day.

**2 · Metadata filtering.** The guarantee assumes you may traverse any edge. Add a filter —
ACLs, tenant, date — and post-filtering the results collapses `k` unpredictably, while
pre-filtering **deletes nodes from the graph** and can disconnect the very region containing the
answer. This is the single biggest gap between ANN benchmarks and production, because benchmarks
almost never filter. Real systems always do.

**3 · Distribution shift after the build.** The graph encodes the geometry of the data at
build time. Incrementally inserting a large, differently-distributed batch degrades navigability
without any error, and nothing tells you.

## The property that makes this dangerous

**Every one of these failures returns well-formed results.** No exception, no dimension
mismatch, no error. The search runs, returns `k` documents, and they are the wrong `k`. Recall
against exhaustive search is the *only* thing that detects it, which is why it belongs in CI and
not in someone's notebook.

## What a strong answer adds

**The uniform-sampling caveat.** This repository's fix adds four *uniformly* sampled long-range
links per node, not `d^{-r}`-sampled ones. Uniform links are enough to escape a local basin —
they connect distant clusters — but they do not give the graded shortcuts that make routing
efficient. At `n = 2,430` the difference does not bite; at `n = 10⁶` it would. Saying that
unprompted is the difference between having read about HNSW and having debugged one.

**And the honest scope.** The in-repo graph exists to make the failure visible, not to compete
with a real index. [#15](https://github.com/akash-coded/nanorag/issues/15) tracks putting a real
ANN backend behind the same `Hit` interface; the comparison against this graph is the
interesting half of that issue.

## Measure it here

`nanorag/store.py` — `ann_vector()` and the graph construction in `_matrix()`.
[Notebook 04](https://github.com/akash-coded/nanorag/blob/main/notebooks/04_retrieval_methods_and_reranking.ipynb)
§4.6 plots the recall-versus-`ef` curve you can watch collapse.
