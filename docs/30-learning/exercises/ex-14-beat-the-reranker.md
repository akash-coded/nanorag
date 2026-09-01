# EX-14 · Beat the reranker

> **Difficulty:** 🔴 · label [`difficulty: 3`](https://github.com/akash-coded/nanorag/labels/difficulty:%203)
> **Stuck?** Ask in the [clinic thread for EX-14](https://github.com/akash-coded/nanorag/discussions/75) — one long-running
> thread per exercise, so the answers accumulate where the next person will look.
> **Submit:** post it in [Show and Tell](https://github.com/akash-coded/nanorag/discussions/categories/show-and-tell) titled
> `[solution · EX-14] ...`, with your numbers and your interval.

**Notebook 04** · ~3 h · Seam ⑤ · *Skill: fit, verify, and be honest*

Improve `ProxyCrossEncoder`. Add features, change the model class, or replace it with a real
cross-encoder if you have the dependency.

**Acceptance criteria**

- Fitted on **dev only**; frozen slice looked at once
- Evidence recall *and* full-chain recall, each with an interval
- Added latency measured, not estimated
- If your gain does not clear the noise band, **say so** — that is a passing submission

---
