# 🚨 Retrieval incident runbook

> **When:** answer quality dropped, users noticed, and nobody knows why.

Work top to bottom. Each step is cheap and rules out a class of cause. **Do not skip to the
interesting hypothesis** — the boring ones are more likely and take two minutes.

## 0 · Before anything — establish that it is real

- [ ] Is the report a **measurement** or an **anecdote**? Three angry tickets is a signal, not a
      regression.
- [ ] Run the frozen eval slice. Does the metric move?
- [ ] **If the eval set says nothing changed, the change is in the query distribution, not the
      system.** Go to step 5.

## 1 · What changed? — in this order of likelihood

| Check | Command / where |
|---|---|
| Code deploy | `git log --since="2 days ago" --oneline` |
| **Index rebuild or partial re-embed** | version alias, `mixed_version_check()` |
| Config change | diff the effective `RagConfig`, not the file |
| Model version | provider-side changes need no deploy of yours |
| Corpus ingest | volume, and whether a new source family arrived |

**The mixed-index check first.** A partially re-embedded index throws no exception and returns
well-formed numbers for vectors that mean nothing to each other. It is the highest-damage,
lowest-visibility failure in the stack.

## 2 · Which stage? — attribute before you fix

Run [The Four Verdicts](../frameworks/four-verdicts.md) over 30 recent failures.

```text
retrieval miss   ->  index, analyzer, encoder
packing loss     ->  k, reranker, packing constraint
generation       ->  prompt, model version
right by accident->  your eval set was already lying
```

**A distribution that has shifted between two dates localises the fault faster than any log.**

## 3 · The five that account for most incidents

1. **Analyzer change** — a tokenizer or normaliser tweak silently re-partitions the term space.
   Symptom: identifier and code-like queries collapse, prose is fine.
2. **Mixed encoder versions** — see above.
3. **`k` or `N` changed by config drift** — often by someone tuning latency.
4. **ACL / filter scope widened or narrowed** — check `k_collapse` in traces.
5. **Corpus ingest changed the length distribution** — BM25's length normalisation is relative to
   `avgdl`, so a bulk import of long documents re-scores *everything*.

## 4 · Stabilise before you fix

- [ ] **Roll back the alias**, not the code, if an index version is implicated. Seconds, not a
      rebuild.
- [ ] If rollback is impossible, raise `k` as a **temporary** recall buffer and say out loud that
      it costs tokens and precision.
- [ ] Freeze ingest until attributed.

## 5 · When the system did not change

The query distribution did. This is common and rarely considered.

- New user cohort, new vocabulary
- A product launch introduced entities the index has never seen
- Seasonality — the same questions, different referents

**The fix is not retrieval tuning.** It is an eval slice that represents the new distribution,
which is [#57](https://github.com/akash-coded/nanorag/issues/57).

## 6 · Close it properly

- [ ] A **regression test** that fails against the broken state. Without it the incident will
      recur and you will diagnose it again from scratch.
- [ ] An entry in `docs/40-operations/incident-log.md`: symptom, wrong hypothesis, root cause,
      detection gap.
- [ ] **The detection gap is the most valuable line.** Not "what broke" but "why did we find out
      from a user".

## The sentence that ends the postmortem

> *"What measurement would have caught this before a user did?"* — then build it, or write down
> why it is not worth building.
