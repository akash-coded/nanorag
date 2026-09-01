# EX-08 · Implement a new chunking strategy

> **Difficulty:** 🔴 · label [`difficulty: 3`](https://github.com/akash-coded/nanorag/labels/difficulty:%203)
> **Submit:** open a thread in [Solutions & Peer Review](https://github.com/akash-coded/nanorag/discussions) with your numbers, or a PR linking to it.

**Notebook 03** · ~2 h · Seam ① · *Skill: extending a system through its seams*

Add an eighth strategy to `chunking.STRATEGIES`. Candidates: sliding-window with sentence
alignment, proposition-level chunking, table-aware chunking, or LLM-decided boundaries.

**Acceptance criteria**

- Registered in `STRATEGIES`, produces stable chunk ids, passes `test_corpus.py`
- Measured against at least three existing strategies
- Storage and index-cost columns next to the recall column

---
