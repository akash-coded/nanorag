# EX-15 · Make the dense leg earn its keep

> **Difficulty:** ⚫ · label [`difficulty: 4`](https://github.com/akash-coded/nanorag/labels/difficulty:%204)
> **Submit:** open a thread in [Solutions & Peer Review](https://github.com/akash-coded/nanorag/discussions) with your numbers, or a PR linking to it.

**Notebook 04** · open-ended · Seam ② · *Skill: understanding why embeddings work at all*

The offline LSA encoder is genuinely weaker than BM25 here. Close the gap without adding a
neural model: better vocabulary, n-grams, term weighting, dimension routing, or corpus
augmentation.

**Acceptance criteria**

- Dense-only evidence recall, before and after, sliced by query class
- An explanation of the mechanism — *why* your change helped
- Whether the hybrid improves once the dense leg does

---
