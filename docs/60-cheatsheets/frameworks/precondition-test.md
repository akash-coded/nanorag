# 🔬 The Precondition Test

> **The question:** should I adopt this technique at all?

Every retrieval technique fixes **one specific failure**. It is worth what it costs only if you
have that failure. Almost nobody checks first.

## The test

Three questions, in order. If any answer is "I don't know", stop and go and find out — that is
cheaper than the implementation.

1. **What failure does this technique fix?** Name the mechanism, not the benefit. "Improves
   retrieval" is not a mechanism. "Closes a vocabulary gap between queries and documents" is.
2. **Do I have that failure?** Name the diagnostic and the number that would confirm it.
3. **What does the fix cost when it works?** Latency, tokens, storage, an extra model to version,
   or a coupling that did not exist before.

## The table, filled in

| Technique | Fixes | Diagnostic — 10 minutes | Cost when it works |
|---|---|---|---|
| **HyDE** | Vocabulary mismatch between queries and documents | Sample 30 queries. Do their terms appear in the documents at all? | A model call per query, ~4× latency |
| **Contextual chunking** | Chunks unretrievable in isolation | Read 20 chunks cold. Can you tell what they are about? | 2.4× storage, and **chunks stop being independent** — a parent edit invalidates all its children |
| **Query decomposition** | Second hop absent from the candidate pool | Is `full_chain_recall_at_N` far below per-passage recall? | N× retrieval calls |
| **Reranking** | First stage orders badly *using signals it did not have* | Do your reranker's features overlap the retriever's? | Linear in N, nothing precomputable |
| **Larger `k`** | Evidence retrieved and dropped | Count found-then-dropped questions | Tokens, and `context_precision` collapses |
| **Semantic cache** | Repeated near-duplicate queries | What share of queries are within ε of a previous one? | False hits — a wrong answer with a discount |
| **Fine-tuned encoder** | Domain vocabulary the general model has never seen | Do domain terms cluster sensibly in the base encoder? | Training data, a retraining cadence, a re-embed bill |

## The failure mode this prevents

Adopting a technique because it worked in someone's paper. **It worked on their corpus, which had
the failure it fixes.** The paper is usually right and usually irrelevant.

This repository has two measured examples: contextual chunking cost 2.4× storage and did not
clear the band, because these chunks already carry their heading path. HyDE cost a model call per
query and did not clear the band, because the eval questions share a fact graph with the
documents. **Both techniques are real. Neither had anything to do here.**

## When this does not apply

**When the diagnostic costs more than the experiment.** If a technique is a two-line change and
you already have the harness, just measure it. The Precondition Test earns its keep when the
implementation is a week and the diagnostic is an afternoon.

## The sentence to use in a review

> *"What failure does this fix, and have we confirmed we have it?"*

It is not a rhetorical question and it should not be asked as one. Half the time the answer is
yes and you have just watched someone justify their work in one sentence.

---

**Seen in:** [#37 — contextual chunking rejected](https://github.com/akash-coded/nanorag/discussions/37) ·
[negative result — HyDE](https://github.com/akash-coded/nanorag/discussions/categories/show-and-tell)
