# Office hours log

Newest first. One entry per session, with the questions that came up and where they were answered.

The point of writing these down is that **the same three questions come up every cohort**, and a
searchable log turns the fourth asking into a link.

---

## 2026-09-08 · Eval sets, noise bands, and why your delta is not real

**Thread:** [#87](https://github.com/akash-coded/nanorag/discussions/87)

**Agenda:** the two-metrics-disagree case; building an eval set with no labels; open floor.

**What came up:**

| Question | Where it landed |
|---|---|
| A change clears the band on evidence recall and not on full-chain. Ship it? | [#29](https://github.com/akash-coded/nanorag/discussions/29) — one effect, two levels of statistical power |
| My eval set is 96 questions, not 207. Does the ~380 figure scale? | It scales, and something else breaks: below ~100 the bootstrap's *coverage* is off, not just wide |
| How do I build an eval set when the client has no labels? | Notebook 02; [EX-04](https://github.com/akash-coded/nanorag/blob/main/docs/30-learning/exercises/ex-04-manufacture-an-eval-set-for-a-new-domain.md). The part people skip is null questions |

**The thing worth repeating:** *"inside the noise band"* is a statement about your instrument, not
about your change. The usual correct next move is to grow the eval set, not to abandon the change.

---

## How to add an entry

Copy this shape. Date descending, keep it short, **link rather than restate**.

```markdown
## YYYY-MM-DD · One-line topic

**Thread:** #NNN

**Agenda:** two or three items.

**What came up:**

| Question | Where it landed |
|---|---|
| ... | ... |

**The thing worth repeating:** one sentence.
```

If a question came up that has **no** good answer yet, say so and link the open issue. A log that
only records successes is a log nobody trusts.
