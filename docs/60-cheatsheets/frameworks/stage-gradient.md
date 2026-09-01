# 📶 The Stage Gradient

> **The question:** which stage is the bottleneck *now*?

A retrieval pipeline is a funnel. Every stage can only lose what the stage before it passed. The
gradient — where the metric stops improving — is the bottleneck, and it **moves** as you fix
things.

## The stages and their metric

```text
corpus  ->  candidates  ->  packed context  ->  answer
             Recall@N     full_chain_recall   answer_correct
                         full_chain_recall_at_N
```

| Read this | It measures |
|---|---|
| `Recall@N` | Did stage one find the evidence at all? |
| `full_chain_recall_at_N` | Did it find **all** the evidence for a question? |
| `full_chain_recall` | Did all of it **survive into the k chunks the model reads**? |
| `answer_correct` | Did the model use it? |

## The rule

> **When a metric at stage *n* improves and the metric at stage *n+1* does not, the bottleneck
> has moved.** That is not a disappointing result — it is the measurement doing its job.

## The diagnostic, in four lines

```python
for r in rows:
    if r["full_chain_recall_at_N"] == 1.0 and r["full_chain_recall"] == 0.0:
        print(r["qid"], r["question_type"])   # found it, then dropped it
```

A long list means your bottleneck is **packing**, and no amount of widening `N` will close it.
Measured here: 84 found-then-dropped against 27 never-retrieved. **Three to one on the stage
nobody was working on.**

## The trap this prevents

`Recall@N` keeps improving long after the funnel stops caring. Widening `N` from 100 to 400 moved
`Recall@N` from 0.938 → 0.974 and `full_chain_recall` from 0.469 → 0.481. **Real work, no
result** — because `k` was the binding constraint and adding 300 candidates does not create a
ninth slot.

## Why the packer, not the reranker

A two-hop comparison question needs both entities in the packed context. A **global relevance
ranking cannot express a constraint about coverage** — six of eight slots can legitimately go to
one entity, and every one of them is correctly ranked.

The constraint belongs where the decision is made. Measured:

```text
                          full_chain   context_precision   tokens
k=8, no constraint            0.469          0.52           4,090
k=16                          0.548          0.31           7,910   (+93% tokens)
k=8, per-entity reservation   0.531          0.51           4,140   (+1.2% tokens)
```

## When this does not apply

**When stages are not independent.** A chunking change moves every stage at once, so the gradient
is uninformative until the index is rebuilt and re-measured. Change one stage at a time or accept
that you cannot attribute the result.

---

**Practise:** [EX-22 — Fix evidence retention](../../30-learning/exercises/ex-22-fix-evidence-retention.md) ·
**Argued out in:** [#28](https://github.com/akash-coded/nanorag/discussions/28)
