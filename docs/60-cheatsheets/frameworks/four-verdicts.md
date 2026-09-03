# 🧭 The Four Verdicts

> **The question:** an answer was wrong. Where did it actually fail?

Most people have two buckets — "retrieval problem" or "generation problem". Two buckets hide the
case that matters most and merge two failures with completely different owners.

## The four

| Verdict | Gold in pool? | Survived packing? | Answer right? | Owner | First fix |
|---|:---:|:---:|:---:|---|---|
| **Retrieval miss** | ✗ | — | ✗ | Index | Chunking, analyzer, encoder, N, fusion |
| **Packing loss** | ✓ | ✗ | ✗ | Ranker | `k`, reranker, packing constraint |
| **Generation failure** | ✓ | ✓ | ✗ | Model / prompt | Generator, prompt contract, grounding |
| **Right by accident** | ✗ | ✗ | ✓ | **Nobody, yet** | This is the dangerous one |

## The trace fields that decide it

```python
gold_in_pool   = bool(set(gold) & {c.chunk_id for c in trace.candidates})
gold_in_packed = bool(set(gold) & {b.chunk_id for b in trace.packed})
correct        = row["answer_correct"] == 1.0
```

That is the whole classifier. If your traces cannot produce those three booleans, **that is the
first finding** — say so on day one rather than promising a number you cannot compute.

## Why row four is the point

**Right by accident** means the model answered from parametric memory and retrieval contributed
nothing. Measured on answer quality alone it looks like success. It means:

- your evaluation is crediting the model for the system's work
- the same query on a private corpus the model has never seen will fail
- and you will not find out until it does

**Measure your floor.** Run the eval set with an ungrounded generator — no retrieved context at
all. Whatever it scores is what the model knew already. Every `answer_correct` you report should
be read against that number, and if you have never computed it you do not know what your system
is worth.

## The distribution is the work plan

One failure tells you nothing. **Fifty tell you where to spend the month.**

```text
retrieval miss    27   ->  index work
packing loss      84   ->  ranker / packer work      <- 3x the other
generation        41   ->  prompt or model
right by accident  9   ->  eval-set problem
```

Those are this repository's real numbers at `N=100, k=8`. The bottleneck was three-to-one on the
stage nobody was working on.

## When this does not apply

**When you have no gold labels** — a production query has none. Then the four verdicts are a
*sampling* frame, not a classifier: you hand-label fifty failures and attribute them. That is a
day of work and it is almost always the right first day.

---

**Practise:** [EX-01 — Attribute ten failures](../../30-learning/exercises/ex-01-attribute-ten-failures.md) ·
**Argued out in:** [#41](https://github.com/akash-coded/nanorag/discussions/41), [#31](https://github.com/akash-coded/nanorag/discussions/31)

**Standalone:** [gist](https://gist.github.com/akash-coded/8d4412f8b4ebff6dd9447970ab389acc) — the classifier and the distribution, standalone. Stdlib only, no clone needed.
