# 📏 The Noise Band Ladder

> **The question:** my metric moved. Is that real?

Six rungs. Climb until you can answer, and **stop at the first one that says no** — the rungs
above it cost more and cannot rescue a failure below.

## The ladder

| # | Rung | The check | If it fails |
|---|---|---|---|
| **1** | **Same eval set?** | Same slice, same `n`, same questions | Nothing else means anything. Fix this first |
| **2** | **Same config?** | Print `RagConfig` next to the number, every time | A stale kernel is the most common cause of a "real" delta |
| **3** | **Deterministic?** | Run it twice. Identical? | Non-determinism means your delta includes run-to-run variance |
| **4** | **Outside the band?** | `paired_bootstrap` — does the 95% interval exclude zero? | **Inside the band ≠ regressed.** It means *not measurable at this `n`* |
| **5** | **Pre-registered?** | Was this metric named primary *before* the number existed? | Otherwise you cannot distinguish it from picking the one that agreed with you |
| **6** | **Survives the frozen slice?** | Re-run on data not used while iterating | A dev-only gain is overfitting, and it is the failure that survives every rung above |

## The two sentences people get wrong

**"Inside the noise band" does not mean "no effect."** It means *this eval set cannot tell*. The
correct report is *"we cannot measure a difference at n=207"*, and the correct next move is
usually to grow the eval set, not to abandon the change.

**"The point estimate is positive" is not a result.** A delta of `+0.0338` with an interval of
`[-0.0097, +0.0821]` is compatible with a small regression. Report the interval or report
nothing.

## The arithmetic you should be able to do cold

```text
n_needed  ~=  n_current  x  (half_width / point_estimate)^2
```

Then **double it**, because a delta that only just missed significance is more likely than not an
overestimate — the winner's curse. Measured here: growing 207 → 812 questions moved a `+0.0338`
delta to `+0.0116`. **The curse was most of the original effect.**

## Two knobs people confuse

| | What it controls | Fixed by |
|---|---|---|
| **`n`** | *How much* uncertainty there is | More eval questions |
| **`n_boot`** | How *carefully* you measure that uncertainty | Patience |

Raising `n_boot` from 2,000 to 100,000 stabilises the printed digits and **does not narrow the
interval**. Widths measured here: 0.0918, 0.0918, 0.0917.

## Binary metrics need more data

`full_chain_recall` is binary per question, so per-question variance is `p(1-p) ≈ 0.25` —
maximal exactly at the 0.5 accuracy where interesting systems sit. The same true effect clears
the band on a continuous metric and not on a binary one. **That is one effect at two levels of
power, not two contradictory results.**

## When this does not apply

**Latency and cost.** They are not sampled from a question distribution; they are measured
directly. A 40% latency regression needs a percentile, not a bootstrap.

---

**Derivation:** [Paired bootstrap and power](../../30-learning/interview-prep/01-mathematical-foundations/paired-bootstrap-and-power.md) ·
**Argued out in:** [#29](https://github.com/akash-coded/nanorag/discussions/29)
