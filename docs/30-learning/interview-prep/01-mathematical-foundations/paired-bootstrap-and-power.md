# The paired bootstrap, and how many questions you actually need

> **As asked:** *"Your change improves recall by 2 points. How do you know that is real? And how
> many eval questions would you need to be sure?"*

## Why paired

The quantity of interest is the **per-question difference** `dᵢ = Bᵢ − Aᵢ`, not the difference of
two means. Questions vary enormously in difficulty, and that variance is usually far larger than
the effect you are chasing. Two independent samples carry it twice:

$$
\mathrm{Var}(\bar{B} - \bar{A}) = \mathrm{Var}(\bar A) + \mathrm{Var}(\bar B) - 2\,\mathrm{Cov}(\bar A, \bar B)
$$

Evaluating both arms on the **same questions** makes `Cov` large and positive, and the covariance
term cancels most of the difficulty variance. That is why a paired design detects effects an
unpaired one cannot, at the same `n`.

Mechanically: resample **questions** with replacement, keep both arms on whichever questions were
drawn, recompute the delta, repeat. The 2.5th and 97.5th percentiles of the resampled deltas are
the interval.

## The distinction people get wrong

There are two errors, and only one of them is under your control after the eval set is fixed.

| | What it is | Scales as | Fixed by |
|---|---|---|---|
| **Sampling variability** | You measured `n` questions, not all possible questions. This is what the interval *reports* | `1/√n` | More questions |
| **Monte Carlo error** | The bootstrap *estimates* those endpoints by resampling, and that estimate is noisy | `1/√B` | More resamples |

Raising `n_boot` from 2,000 to 100,000 makes the endpoints you print more **stable** — the digits
stop moving — and does **not** narrow the interval:

```
n_boot=  2,000  [-0.0097, +0.0821]  width=0.0918
n_boot= 10,000  [-0.0094, +0.0818]  width=0.0918
n_boot=100,000  [-0.0095, +0.0817]  width=0.0917
```

**`n_boot` is how carefully you measure the uncertainty. `n` is how much uncertainty there is.**
Confusing them is the most common bootstrap mistake and it is worth being able to say this in one
sentence.

## How many questions

Observed: `n = 207`, delta `+0.0338`, 95% half-width `≈ 0.046`.

For the interval to just exclude zero, half-width must drop below the point estimate. Half-width
scales as `1/√n`:

$$
n \;\approx\; 207 \times \left(\frac{0.046}{0.0338}\right)^2 \;\approx\; 383
$$

**Do not quote 383.** It assumes the true effect equals the measured one, and a delta that only
just missed significance is more likely than not an **overestimate** — the winner's curse.
Selection on significance biases the observed effect upward. Budget roughly double:

$$
\approx 700\text{–}800 \text{ questions for 80\% power at this effect size}
$$

This was checked. Growing the frozen slice to 812 and re-running the identical change moved the
point estimate from `+0.0338` to `+0.0116` — **the winner's curse was most of the original
effect.** Recorded in
[discussion #29](https://github.com/akash-coded/nanorag/discussions/29).

## Why binary metrics need more data

`full_chain_recall` is binary per question, so per-question variance is `p(1−p)`, maximised at
`p = 0.5` — precisely where interesting systems sit. `evidence_recall` is continuous over
`{0, 0.5, 1.0}` and has lower variance.

**The same true effect will clear the band on the continuous metric and not on the binary one.**
That is not two contradictory results; it is one effect measured at two levels of statistical
power, and saying so is the difference between a confused report and a clear one.

## What a strong answer adds

**1 · The practical conclusion.** Growing an eval set from 207 to 800 questions is about a day of
generator work. Every engineering option on the table costs more and moves the metric less.
**Grow the eval set before optimising anything.** Almost nobody does this and it is almost always
right.

**2 · Interval method.** `paired_bootstrap` uses **percentile** intervals. BCa corrects for bias
and skew in the bootstrap distribution and shifts the endpoints — but not reliably narrower, and
never enough to rescue an underpowered comparison.

**3 · Pre-registration.** An interval is only meaningful if the metric was chosen before the
number existed. Reporting the metric that cleared, out of several measured, is indistinguishable
from p-hacking from the outside — which is why the PR template names a primary metric and
requires every baseline metric to be reported, cleared or not.

## Measure it here

`nanorag/metrics.py` — `paired_bootstrap(rows_a, rows_b, key=..., n_boot=2000, seed=11)` returns
`delta`, `ci`, `p_better`, `n` and a `verdict`.
[EX-02](../../exercises/ex-02-find-the-n-where-the-ceiling-stops-moving.md) makes you find the
`n` at which your own measurements stop moving.
