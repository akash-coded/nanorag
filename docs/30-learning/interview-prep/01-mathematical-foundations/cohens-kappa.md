# Cohen's κ — why raw agreement lies

> **As asked:** *"You calibrated your LLM judge against human labels and they agree 90% of the
> time. Is that good?"*

## The answer is "I cannot tell yet"

Raw agreement is uninterpretable without the class balance. If 90% of your examples are the
positive class, a rater that **always says positive** achieves 90% agreement while carrying zero
information.

κ corrects for the agreement you would expect by chance:

$$
\kappa = \frac{p_o - p_e}{1 - p_e}
$$

`p_o` is observed agreement. `p_e` is expected agreement under independence, computed from the
**marginals** — for each class, multiply the two raters' rates of using it and sum:

$$
p_e = \sum_c P_1(c)\,P_2(c)
$$

The denominator `1 − p_e` is the agreement that was available to be earned beyond chance. So κ
is *the share of the achievable non-chance agreement that was actually achieved.*

## Work the example

Judge and human both label 90% of items "correct".

$$
p_e = (0.9)(0.9) + (0.1)(0.1) = 0.82
$$
$$
\kappa = \frac{0.90 - 0.82}{1 - 0.82} = \frac{0.08}{0.18} \approx 0.44
$$

**90% agreement is κ ≈ 0.44** — moderate, and nowhere near good enough to replace a human. Push
the imbalance to 95/5 and the same 90% raw agreement gives a κ that is **negative**: worse than
chance.

This is why `nanorag/judge.py` calibrates on κ and not on accuracy, and it is the single most
useful thing in the evaluation material.

## Reading the number

| κ | Conventional reading | What it means for a judge |
|---|---|---|
| < 0 | Worse than chance | Something is inverted. Check your label mapping first |
| 0.0 – 0.20 | Slight | Unusable |
| 0.21 – 0.40 | Fair | Unusable for gating a release |
| 0.41 – 0.60 | Moderate | Usable for *relative* comparisons, not absolute claims |
| 0.61 – 0.80 | Substantial | Usable |
| > 0.80 | Almost perfect | Check for leakage before believing it |

Landis and Koch's bands are conventions, not theorems. Say so if you quote them.

## What a strong answer adds

**1 · κ's own weakness — the prevalence paradox.** κ is *itself* sensitive to the marginals. Two
rater pairs with identical `p_o` can have very different κ if their class distributions differ,
which makes κ hard to compare **across** datasets. Within one eval set, tracked over time, it is
the right statistic. Across two different corpora it is not.

**2 · When Cohen's κ is the wrong tool.**

- **More than two raters** → Fleiss' κ.
- **Ordinal or graded labels** → *weighted* κ, so disagreeing by one grade costs less than
  disagreeing by three. Unweighted κ on a 1–5 rubric throws away most of the information.
- **Missing labels, or mixed measurement levels** → Krippendorff's α, which handles both and
  degenerates to κ in the simple case.

**3 · The point that separates a practitioner.** A judge with **moderate but consistent** κ can
still rank two systems correctly, because a systematic bias applies equally to both arms and
cancels in the paired comparison. A judge with **high but erratic** κ cannot. So the right
follow-up question is not "is κ high enough" but **"is the judge's error correlated with the
thing I am trying to measure?"** — which is what the bias probes in `judge.py` test.

## Measure it here

`nanorag/metrics.py` — `cohens_kappa()` and `agreement_report()`.
[Notebook 06](https://github.com/akash-coded/nanorag/blob/main/notebooks/06_evaluation_approaches.ipynb)
calibrates the judge against hand labels.
[EX-19](../../exercises/ex-19-calibrate-a-judge-against-humans.md) has you label 50 examples by
hand first — which is also the fastest way to discover that your rubric is ambiguous.
