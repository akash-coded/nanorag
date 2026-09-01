# EX-18 · Solve abstention

> **Difficulty:** ⚫ · label [`difficulty: 4`](https://github.com/akash-coded/nanorag/labels/difficulty:%204)
> **Stuck?** Ask in the [clinic thread for EX-18](https://github.com/akash-coded/nanorag/discussions/80) — one long-running
> thread per exercise, so the answers accumulate where the next person will look.
> **Submit:** post it in [Show and Tell](https://github.com/akash-coded/nanorag/discussions/categories/show-and-tell) titled
> `[solution · EX-18] ...`, with your numbers and your interval.

**Notebook 05 + 06** · open-ended · Seam ⑧⑨ · *Skill: the hardest open item in the repo*

No retrieval-score threshold separates answerable from unanswerable here (best F1 0.38). Build
something that does.

**Directions worth trying:** a cheap sufficiency call with a strict schema; answer-type
checking; a trained classifier over pair features; an NLI-style entailment check; a
two-stage contract where the model must name the evidence span before asserting.

**Acceptance criteria**

- Abstention precision/recall on the full null set with the real base rate
- The cost per query of your approach
- What it does to over-refusal on answerable questions — the failure nobody measures
- An honest statement of what it still gets wrong

---
