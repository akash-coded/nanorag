# ⚖️ The Calibration Triangle

> **The question:** can I trust this judge?

Three properties. A judge needs all three, and they fail independently — which is why "the judge
agrees with me 94% of the time" answers none of them.

```text
                 AGREEMENT
              (κ, not raw %)
                    /\
                   /  \
                  /    \
                 /      \
        CONSISTENCY —— INDEPENDENCE
       (same input,     (error uncorrelated
        same verdict)    with what you measure)
```

## 1 · Agreement — κ, never raw percentage

Raw agreement is uninterpretable without the class balance. **90% agreement on a 90/10 split is
κ ≈ 0.44. On a 95/5 split the same 90% is negative.**

$$
\kappa = \frac{p_o - p_e}{1 - p_e}
$$

Always report κ **with the base rate beside it**. A κ without its class balance is not comparable
to anyone else's.

## 2 · Consistency — same input, same verdict

Run the same 50 examples through the judge twice. Any disagreement with itself is pure noise
added to every measurement you will ever make with it.

- Temperature > 0 guarantees some.
- Order effects: swap the position of two answers and see if the verdict flips.
- Prompt drift: a judge whose rubric you edit mid-project has invalidated the runs before it.

## 3 · Independence — error uncorrelated with what you measure

**This is the one nobody tests, and it is the one that ruins a result.**

A judge that prefers longer answers is biased. That is survivable *if* both arms produce
similarly-long answers, because the bias applies equally and **cancels in the paired
comparison**. It is fatal if your change makes answers longer — then you cannot separate "better"
from "longer", and the judge will confirm your change every time.

The probe: hold content constant, vary only the suspected property, measure the score shift.

## The counter-intuitive conclusion

> **A judge with moderate but consistent κ can rank two systems correctly. A judge with high but
> erratic κ cannot.**

So the useful question is not *"is κ high enough"* — it is **"is the judge's error correlated
with the thing I am changing?"** A systematic bias is an offset. A random one is variance, and
variance is what hides your effect.

## The order to test in

1. **Consistency first.** It is free and an inconsistent judge invalidates everything after it.
2. **Agreement second**, on hand labels, reported with the base rate.
3. **Independence last**, with one probe per property your change plausibly moves.

## When this does not apply

**When the judge is the product**, not the instrument — a model grading student work, say. Then
its absolute quality matters, not just its rank-preserving behaviour, and κ against expert labels
becomes the headline rather than a prerequisite.

---

**Derivation:** [Cohen's κ](../../30-learning/interview-prep/01-mathematical-foundations/cohens-kappa.md) ·
**Practise:** [EX-19](../../30-learning/exercises/ex-19-calibrate-a-judge-against-humans.md), [EX-20](../../30-learning/exercises/ex-20-build-a-third-bias-probe.md)
