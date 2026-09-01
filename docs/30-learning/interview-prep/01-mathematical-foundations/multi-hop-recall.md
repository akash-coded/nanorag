# Multi-hop recall — the conjunction, and why independence is wrong

> **As asked:** *"Your per-passage Recall@10 is 0.86. A question needs three passages to be
> answerable. What is your end-to-end recall?"*

## The answer they are looking for first

If retrieving each passage were independent:

$$
P(\text{all three}) = 0.86^3 \approx 0.64
$$

**A 14-point drop from a metric that looked healthy.** Most candidates never compute this, quote
`0.86` as system quality, and are wrong by an amount that grows with every hop.

That is the entry price. The follow-up is where the answer is actually scored.

## Why independence is the wrong model

Passages that answer one question are **not** independently retrieved. They frequently sit in the
same document, or in documents sharing entities, so retrieving one raises the chance of
retrieving the next:

$$
P(A \wedge B) = P(A)\cdot P(B \mid A), \qquad P(B\mid A) > P(B)
$$

Positive correlation lifts the true conjunction **above** the independence estimate. So `0.64` is
a **lower bound**, not a prediction — and the gap between bound and measurement is itself
diagnostic:

| Observation | What it means |
|---|---|
| measured ≈ predicted | Hops are genuinely independent. Evidence is scattered; the packer has to work hard |
| measured ≫ predicted | Hops co-occur. Often a sign your chunker split one coherent passage in two |
| **measured ≪ predicted** | Something is actively suppressing the second hop |

That last row is the useful one. The usual culprit is **deduplication by document**: a diversity
constraint capping chunks per document will systematically drop the second hop of a same-document
pair. It looks like a retrieval quality problem and is a packing policy problem.

## The stage confusion that produces most wrong answers

Two different metrics get called "recall" and they have different denominators:

```
full_chain_recall_at_N   over the candidate pool (N=100)    0.871
full_chain_recall        over the packed context (k=8)      0.469
```

The conjunction model predicts the **first**. The gap between the two is **not** a retrieval
failure at all — it is evidence that reached the pool and did not survive packing. On this
corpus that is 84 of 207 questions, against 27 never retrieved at all: **the bottleneck is
three-to-one on the stage most people do not work on.**

The diagnostic that separates them:

```python
for r in rows:
    if r["full_chain_recall_at_N"] == 1.0 and r["full_chain_recall"] == 0.0:
        print(r["qid"], r["question_type"])   # found it, then dropped it
```

## Why widening N does not fix it

`k` bounds the conjunction. A two-hop comparison question needs both entities represented in the
packed context, and a **global relevance ranking cannot express a coverage constraint** — six of
eight slots can legitimately go to one entity. Adding 300 more candidates does not create a ninth
slot.

Measured, same reranker, same corpus:

```
                          full_chain   context_precision   tokens
k=8, no constraint            0.469          0.52           4,090
k=16                          0.548          0.31           7,910   (+93% tokens)
k=8, per-entity reservation   0.531          0.51           4,140   (+1.2% tokens)
```

The constraint belongs in the **packer**, not wished for in the reranker. Tracked as
[#47](https://github.com/akash-coded/nanorag/issues/47).

## What a strong answer adds

The general form, which transfers well beyond retrieval: **when a metric at stage `n` improves
and the metric at stage `n+1` does not, the bottleneck has moved.** That is not a disappointing
result — it is the measurement doing its job.

And the statistical consequence, which is the [bootstrap
question](paired-bootstrap-and-power.md) in disguise: full-chain recall is **binary per
question**, so its per-question variance is `p(1−p) ≈ 0.25` — maximal at the 0.5 accuracy where
interesting systems live. The same true effect needs far more questions to become visible on
full-chain recall than on continuous evidence recall. Worked through in
[discussion #29](https://github.com/akash-coded/nanorag/discussions/29).

## Measure it here

`nanorag/metrics.py` — `full_chain_recall`, `evidence_recall_at_k`.
[Notebook 01](https://github.com/akash-coded/nanorag/blob/main/notebooks/01_retrieval_and_evaluation_foundations.ipynb)
§1.3 reports both lines separately for exactly this reason.
