# EX-04 · Manufacture an eval set for a new domain

> **Difficulty:** 🟡 · label [`difficulty: 2`](https://github.com/akash-coded/nanorag/labels/difficulty:%202)
> **Submit:** open a thread in [Solutions & Peer Review](https://github.com/akash-coded/nanorag/discussions) with your numbers, or a PR linking to it.

**Notebook 02** · ~2 h · *Skill: the thing clients actually need*

Add a new document family to `corpus.py` (regulatory filings, product manuals, meeting minutes
— your choice) and generate questions for it through the SEED → FILTER → MAINTAIN pipeline.

**Acceptance criteria**

- At least 20 new questions across ≥3 types, with gold evidence that resolves
  (`test_every_gold_anchor_resolves_under_the_shipped_chunking` must pass)
- The filter drop-rate per gate, reported
- At least two *planted flaws* that your filters catch, with the catch demonstrated
- Baseline metrics on the new slice, and one sentence on why they differ from the existing slices

---
