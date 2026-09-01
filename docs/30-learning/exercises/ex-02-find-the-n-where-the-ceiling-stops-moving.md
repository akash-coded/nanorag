# EX-02 · Find the N where the ceiling stops moving

> **Difficulty:** 🟡 · label [`difficulty: 2`](https://github.com/akash-coded/nanorag/labels/difficulty:%202)
> **Stuck?** Ask in the [clinic thread for EX-02](https://github.com/akash-coded/nanorag/discussions/63) — one long-running
> thread per exercise, so the answers accumulate where the next person will look.
> **Submit:** post it in [Show and Tell](https://github.com/akash-coded/nanorag/discussions/categories/show-and-tell) titled
> `[solution · EX-02] ...`, with your numbers and your interval.

**Notebook 01** · ~45 min · *Skill: sizing a first stage*

Sweep `n_candidates` and find the point where `Recall@N` flattens. Then argue for an operating
point using latency and cost, not just recall.

**Acceptance criteria**

- The sweep, plotted, with the chosen N marked
- The marginal recall per 100 additional candidates, as a table
- The latency cost of your choice from `costs.latency_model`
- One sentence a client would accept for why not simply N=1000

---
