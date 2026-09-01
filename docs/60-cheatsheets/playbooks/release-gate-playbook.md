# 🚦 Release gate playbook

> **When:** deciding whether a change ships.

## The decision, in one pass

```text
1. Did the primary metric clear the band?          no  -> do not ship
2. Was the primary metric named before the run?    no  -> you cannot tell shipping
                                                          from cherry-picking. Fix the process
3. Did any secondary metric regress beyond ITS     yes -> ship only with the regression stated
   own band?                                              and accepted by name
4. Does it hold on the frozen slice?               no  -> overfitting. Do not ship
5. Cost, latency, storage inside budget?           no  -> a quality win you cannot afford
                                                          is not a win
                                                   all clear -> ship, and record the numbers
```

## The three sentences people get wrong

**"Inside the noise band" ≠ "regressed."** It means *not measurable at this `n`*. That is a
statement about your instrument. The usual correct response is to grow the eval set, not to
abandon the change.

**"The point estimate is positive" is not a result.** `+0.0338, CI [-0.0097, +0.0821]` is
compatible with a small regression.

**"We measured five metrics and one improved" is not a result either.** That is roughly what
chance produces. See the multiple-comparison note below.

## Pre-registration is the whole defence

Naming the primary metric **before** the number exists is what separates *shipping on the primary
metric* from *picking the one that agreed with you*. From outside, and in a review, those look
identical.

The mechanics that make it real:

- The primary metric is named in the PR template and in `eval-baseline.json`
- **Every** metric in the baseline appears in the PR body — cleared or not
- A change of primary metric is itself a reviewable decision, not an edit

## Per-slice regressions

An aggregate metric **cannot detect a failure confined to a minority class**. Averaging is
precisely the operation that hides it — that is how the FTS5 tokenizer bug survived, with
identifier queries inverted and the mean barely moving.

Gate on slices, with two cautions:

- **Each slice needs its own band.** A slice of 30 has a far wider interval than the full set;
  applying the aggregate band to it fails constantly on noise
- **Slices below a minimum size are reported, not gated** — and the report says which were skipped

Tracked as [#58](https://github.com/akash-coded/nanorag/issues/58).

## Multiple comparisons

Testing 12 slices at α=0.05 gives you roughly one significant result **by chance**. Before
celebrating a single slice:

- Apply Benjamini–Hochberg, not Bonferroni — FDR control is the practical choice
- Note that corrections apply to **significant** results. A null result does not need correcting,
  and "isn't that multiple comparisons?" aimed at a non-significant finding is a misfire

## What blocks a merge here

| Blocks | Does not block |
|---|---|
| Primary metric regression outside the band | Inside-band movement on a secondary metric |
| Any slice regression beyond its own band | A slice below the minimum size |
| Missing measurement on a `needs: eval-numbers` change | A negative result, honestly reported |
| Frozen-slice regression | A finding that contradicts the documentation |

**A negative result is not a blocked release. It is a release of a different kind** — the change
does not ship, the finding does.

## The failure mode of gates

A gate that blocks correct changes gets disabled, and **a disabled gate is worse than none
because it still looks like a control.** Watch the override rate: if more than about one in ten
blocked PRs is merged anyway after review, the threshold is wrong — and the fix is almost always
to grow the eval set, not to loosen the gate.
