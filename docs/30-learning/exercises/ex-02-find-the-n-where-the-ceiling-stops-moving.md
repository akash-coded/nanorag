# EX-02 · Find the N where the ceiling stops moving

> **Difficulty:** 🟡 · label [`difficulty: 2`](https://github.com/akash-coded/nanorag/labels/difficulty:%202)
> **Submit:** open a thread in [Solutions & Peer Review](https://github.com/akash-coded/nanorag/discussions) with your numbers, or a PR linking to it.

**Notebook 01** · ~45 min · *Skill: sizing a first stage*

Sweep `n_candidates` and find the point where `Recall@N` flattens. Then argue for an operating
point using latency and cost, not just recall.

**Acceptance criteria**

- The sweep, plotted, with the chosen N marked
- The marginal recall per 100 additional candidates, as a table
- The latency cost of your choice from `costs.latency_model`
- One sentence a client would accept for why not simply N=1000

---
