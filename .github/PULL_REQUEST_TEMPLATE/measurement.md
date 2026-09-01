<!-- For any change that could move a number: retrieval, metrics, chunking, packing, the judge.
     Open with ?template=measurement.md -->

## What this changes

<!-- One or two sentences. -->

Closes #

## The measurement

<!-- Required. A point estimate is not a result — every row needs an interval.
     `python scripts/run_eval.py` prints this table. -->

| Metric | Before | After | Delta | 95% CI | Verdict |
|---|---:|---:|---:|---|---|
| `evidence_recall` ⭑ | | | | | |
| `full_chain_recall` | | | | | |
| `context_precision` | | | | | |
| `answer_correct` | | | | | |

**Primary metric:** `evidence_recall`
**Pre-registered?** <!-- Was it named primary BEFORE this run? If not, say so. -->
**Eval set:** n = , slice =
**Noise band at this n:** ±

### By slice

<!-- An aggregate cannot detect a failure confined to a minority class. Small slices are
     reported, not gated — say which were too small. -->

| Slice | n | Delta | 95% CI | Verdict |
|---|---:|---:|---|---|
| | | | | |

**Slices below the minimum size (reported, not gated):**

## Cost

| | Before | After | Δ |
|---|---:|---:|---:|
| Prompt tokens | | | |
| p95 latency | | | |

## What I tried that did not work

<!-- Not optional. The path that failed is usually more informative than the one that worked. -->

## Checklist

- [ ] Every metric in the baseline appears above, **cleared or not**
- [ ] Intervals, not point estimates
- [ ] Ran on the **frozen slice**, not only dev
- [ ] Notebook outputs stripped (`make strip`)
- [ ] A regression test exists for anything this fixes
