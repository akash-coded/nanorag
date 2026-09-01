# EX-08 · Implement a new chunking strategy

> **Difficulty:** 🔴 · label [`difficulty: 3`](https://github.com/akash-coded/nanorag/labels/difficulty:%203)
> **Stuck?** Ask in the [clinic thread for EX-08](https://github.com/akash-coded/nanorag/discussions/69) — one long-running
> thread per exercise, so the answers accumulate where the next person will look.
> **Submit:** post it in [Show and Tell](https://github.com/akash-coded/nanorag/discussions/categories/show-and-tell) titled
> `[solution · EX-08] ...`, with your numbers and your interval.

**Notebook 03** · ~2 h · Seam ① · *Skill: extending a system through its seams*

Add an eighth strategy to `chunking.STRATEGIES`. Candidates: sliding-window with sentence
alignment, proposition-level chunking, table-aware chunking, or LLM-decided boundaries.

**Acceptance criteria**

- Registered in `STRATEGIES`, produces stable chunk ids, passes `test_corpus.py`
- Measured against at least three existing strategies
- Storage and index-cost columns next to the recall column

---
