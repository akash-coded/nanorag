# 🧾 Design review checklist

> **When:** someone is about to present a retrieval architecture and you are in the room.

Run it in this order. The first three catch most of what goes wrong, and none of them are about
retrieval.

## Before the design — the questions that change it

- [ ] **What is the evaluation plan?** If there is none, stop. A design with no definition of
      working cannot be reviewed, only admired.
- [ ] **Who writes the gold set, and when?** If it is the same engineer building the system, the
      eval set will lose. Say which wins.
- [ ] **Can a user know a document exists but not read it?** This decides the architecture, not a
      detail of it. See [The Inference Channel Audit](../frameworks/inference-channel-audit.md)
- [ ] **What is the abstention target?** In most domains a confident wrong answer costs more than
      a refusal. That asymmetry should be a number **before** the build

## The design itself

- [ ] **Filtering is inside the retrieval query**, never after it. Post-filtering collapses `k`
      unpredictably and leaks result counts
- [ ] **Chunk ids are stable** across re-ingest, or the incremental path silently becomes a
      rebuild
- [ ] **Encoder version is pinned per index version.** A mixed index throws no error
- [ ] **The reranker sees something the first stage did not** — [The Reranker Mirror](../frameworks/reranker-mirror.md)
- [ ] **Rerank depth exceeds `k`**, or the stage is decorative
- [ ] **There is a trace**, and it carries candidates, packed set, per-stage latency, and
      `k_collapse`

## Cost and operations

- [ ] The cost model has more than generation tokens — [The Cost Iceberg](../frameworks/cost-iceberg.md)
- [ ] **The re-embed trigger is a written policy, not an event.** "When we upgrade the encoder"
      is not a policy; a quality threshold that justifies a week of GPU is
- [ ] Index rollback is an **alias swap**, not a rebuild
- [ ] Someone owns the eval set after the engagement ends

## Numbers that must be present

- [ ] Every quality claim has an **interval**, not a point estimate
- [ ] The **noise band** for the eval-set size is stated
- [ ] Corpus size, change rate and query volume are stated as **inputs**, not assumed

## The four questions to ask out loud

1. *"What failure does this component fix, and have we confirmed we have it?"*
2. *"What would have to be true for this to be the wrong design?"*
3. *"How would we find out this had broken — before a user tells us?"*
4. *"What is week one?"*

The fourth is the most revealing. A candidate or colleague who designs the finished system and
cannot say what week one is has usually not shipped one.

## Reviewing without being useless

- **Attack the design, endorse the designer.** Say which parts survive review, explicitly.
  A review that lists only problems reads as a verdict on the person.
- **Disagree with evidence.** "I have seen this fail" is worth more than "I would not do that",
  and both are worth more than seniority.
- **Separate blocking from noting.** Three blocking issues get fixed; fifteen mixed comments get
  triaged into nothing.
