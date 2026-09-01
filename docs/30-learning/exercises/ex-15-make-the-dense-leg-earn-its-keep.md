# EX-15 · Make the dense leg earn its keep

> **Difficulty:** ⚫ · label [`difficulty: 4`](https://github.com/akash-coded/nanorag/labels/difficulty:%204)
> **Stuck?** Ask in the [clinic thread for EX-15](https://github.com/akash-coded/nanorag/discussions/76) — one long-running
> thread per exercise, so the answers accumulate where the next person will look.
> **Submit:** post it in [Show and Tell](https://github.com/akash-coded/nanorag/discussions/categories/show-and-tell) titled
> `[solution · EX-15] ...`, with your numbers and your interval.

**Notebook 04** · open-ended · Seam ② · *Skill: understanding why embeddings work at all*

The offline LSA encoder is genuinely weaker than BM25 here. Close the gap without adding a
neural model: better vocabulary, n-grams, term weighting, dimension routing, or corpus
augmentation.

**Acceptance criteria**

- Dense-only evidence recall, before and after, sliced by query class
- An explanation of the mechanism — *why* your change helped
- Whether the hybrid improves once the dense leg does

---
