# Troubleshooting

For the failures that **produce no error at all**. If you have an error string, try
[Common Errors](Common-Errors) first.

Everything here follows the same shape: a symptom you can observe, the causes ordered by how often
they turn out to be the answer, and a check that takes under a minute.

---

## Retrieval returns plausible results that are subtly wrong

The hardest class, because every component reports success.

| # | Cause | One-minute check |
|---|---|---|
| 1 | **Mixed encoder versions in one index.** Cosine returns well-formed numbers for vectors that mean nothing to each other | `index.mixed_version_check(version)` — `distinct_embedder_tags` must be 1 |
| 2 | **The analyzer split your identifiers.** `ERR_CONN_RESET` indexed as `err`+`conn`+`reset`, each in every document | Query a literal identifier and count matches. Zero or everything are both wrong |
| 3 | **Normalised at index time, not at query time** (or vice versa) | Are the stored vectors unit norm? Is the query vector? |
| 4 | **A post-filter collapsed `k`** | `k_collapse` in the trace. Asked for 8, got 3? |
| 5 | **Stale kernel** — you changed a parameter and re-ran the eval cell but not the indexing cell | Print the config fingerprint next to the number |

**Start with 1.** It is the highest-damage, lowest-visibility failure in the stack, and it is one
call to rule out.

---

## A metric moved and I cannot tell whether it is real

Work down [The Noise Band Ladder](https://github.com/akash-coded/nanorag/blob/main/docs/60-cheatsheets/frameworks/noise-band-ladder.md).
Stop at the first "no".

The two people get wrong most:

- **"Inside the noise band" is not "regressed."** It means *not measurable at this `n`*. That is a
  statement about your instrument.
- **Raising `n_boot` does not narrow the interval.** It stabilises the digits. Width is set by `n`.

---

## Recall improved and answer quality did not

The bottleneck moved. Run the diagnostic rather than guessing:

```python
for r in rows:
    if r["full_chain_recall_at_N"] == 1.0 and r["full_chain_recall"] == 0.0:
        print(r["qid"], r["question_type"])   # found it, then dropped it
```

A long list means **packing**, not retrieval, and no amount of widening `N` closes it. On this
repo's corpus that list was 84 questions against 27 never-retrieved.

---

## The eval set says nothing changed but users say it got worse

The system probably did not change. **The query distribution did.**

- A new user cohort with different vocabulary
- A product launch introduced entities the index has never seen
- Seasonality — same questions, different referents

The fix is not retrieval tuning. It is an eval slice representing the new distribution.

---

## Every chunking strategy scores identically

Almost always **documents too short for the strategies to differ**. Check the length distribution
before believing the result.

If documents are genuinely long enough, check that the bake-off is comparing at the same chunk
*count* — fewer, larger chunks change what `k` means, so it is not a like-for-like comparison.

---

## ANN recall is zero regardless of `ef`

**Zero regardless of `ef` is not a degraded result — it is a structurally impossible one.**

- Recall that **degrades gracefully** as `ef` falls → the visit budget is too small
- Recall **pinned at zero** at every `ef` → the graph is disconnected

Those have different fixes and it is a one-line distinction. The usual cause is a pure k-NN graph
with no long-range links, or heavy pre-filtering that removed the nodes on the path.

---

## The judge agrees with me and the numbers still feel wrong

Check in this order:

1. **Self-consistency** — same input twice, same verdict? An inconsistent judge adds noise to every
   measurement made with it, and no amount of κ fixes that
2. **κ, with the base rate beside it** — 90% agreement on a 90/10 split is κ ≈ 0.44
3. **Independence** — is the judge's error correlated with what you are changing? A judge that
   prefers longer answers is fine until your change makes answers longer

Most people check only 2, which is the least informative of the three.

---

## Notebooks pass locally and fail in CI

- **Execution order.** Locally you ran cells in the order you edited them. CI runs top to bottom
- **A cached artefact** — an index or eval set from an earlier run
- **Non-determinism** — an unseeded RNG. Two runs must produce identical numbers, or a delta is
  not a delta

```bash
make strip && python scripts/verify_notebooks.py
```

---

## Nothing here matches

Open a thread in [Q&A](https://github.com/akash-coded/nanorag/discussions/categories/q-a) with the
numbers, the config, and what you already tried — and check
[the discussion map](https://github.com/akash-coded/nanorag/blob/main/docs/50-community/discussion-map.md)
first, because roughly half of new questions are already answered in a clinic thread.

**Then add what you learn to this page.**
