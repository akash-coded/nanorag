# 🧊 The Cost Iceberg

> **The question:** what does this system actually cost?

The per-query token price is the part above the water. It is **roughly a third** of a real
monthly bill, and it is the only part most people can quote.

## The shape

```text
generation tokens             31%   <- the number everyone quotes
embedding, initial backfill   18%   one-off, and it lands in month one
embedding, re-embed on drift  14%   recurring, always forgotten
vector store / cluster        22%   fixed, does not scale down
reranker inference             9%
trace + eval storage           6%
```

Quote "about a cent a query" and you have described 31% with high confidence and implied the
other 69% is rounding. **That conversation goes badly in month three precisely because the number
you gave was accurate.**

## The four inputs that decide everything

Ask for these before quoting anything:

1. **Corpus size** — drives backfill and index
2. **Change rate** — drives the re-embed cycle, and nobody volunteers it
3. **Query volume** — drives generation and rerank
4. **Encoder dimension** — drives storage and RAM, quadratically with corpus size

If you have none of them, say so. *"Give me your document count and change rate and I will turn
this into a real number in a week"* is more credible than a confident cent-per-query, not less.

## Capex versus opex

| Shape | Items | Why it matters |
|---|---|---|
| **Capex-like** | Backfill, index build, encoder upgrade | Large, infrequent, plannable. A decision you make twice a year |
| **Opex-like** | Generation, rerank, serving | Continuous, scales with traffic. A bill you pay daily |

Blending them into one per-query number hides that one is a decision and the other is a
consequence.

## The multiplier that is not about money

A technique that multiplies **storage** usually multiplies something worse. Contextual chunking
at 2.4× storage costs fractions of a cent per GB-month — and:

- 2.4× the tokens through the encoder on **every** backfill
- a bigger BM25 postings list, which is RAM on the serving path, not object storage
- and the one that hurts: **a parent document edit now invalidates every chunk in it**, so
  chunks that were independent are coupled and the incremental path partly collapses into a
  rebuild

The storage bill is a rounding error. **The dependency-structure change it signals is not**, and
it is invisible in the storage column.

## The sentence that survives scrutiny

> *"Per-query token cost is around X and I can show you the model. It is roughly a third of the
> total — the cluster and the re-embedding cycle dominate, and both depend on facts about your
> corpus I do not have yet."*

**The methodology transfers; the constants do not.** Saying which is which is what makes a client
trust the next number you give them.

## When this does not apply

**Self-hosted, already-paid-for hardware.** Then the marginal cost of a query is near zero and
the real currency is latency and capacity. The iceberg still has the same shape; the units change.

---

**Practise:** [EX-21](../../30-learning/exercises/ex-21-cost-model-for-a-real-client-shape.md) ·
**Tracked in:** [#44](https://github.com/akash-coded/nanorag/issues/44) ·
**Argued out in:** [#32](https://github.com/akash-coded/nanorag/discussions/32)
