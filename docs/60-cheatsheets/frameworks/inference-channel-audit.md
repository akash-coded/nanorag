# 🔒 The Inference Channel Audit

> **The question:** can someone learn about content they are not allowed to read?

Access control asks *can they read it*. That is the easy half. The hard half is whether the
system's **behaviour** is a function of content they cannot read — because if it is, they can
infer it without ever seeing it.

## The five channels, in the order they get missed

| # | Channel | The leak | The fix, and what it costs |
|---|---|---|---|
| **1** | **Result count** | Ask for `k=10`, get 3. You have learned 7 permitted-looking matches exist above your clearance | Pre-filter **inside** the query, never after. Free — and it is also the correct design |
| **2** | **Ranking** | A permitted document's *position* shifts depending on classified neighbours | Score within the permitted set only |
| **3** | **Latency** | A query touching a large classified region does more index work and returns slower | Constant-time padding or a latency floor. **Costs real performance** |
| **4** | **Error behaviour** | "No results" vs. a timeout vs. an error distinguishes *absent* from *forbidden* | One indistinguishable response for both |
| **5** | **Aggregates** | Counts, facets, "did you mean" and analytics are computed over everything | Compute them per-permission-scope, or not at all |

## The rule that generates all five

> **Any output whose value depends on content the caller cannot read is a channel.** Including
> outputs that are not the answer: counts, timings, errors, suggestions.

## Post-filtering is always wrong here

It fails twice, and the second failure is the one people miss:

1. It **collapses `k` unpredictably** — ask for 10, get 3, with no signal that it happened. In
   this repo that damage is measurable as `k_collapse` in the trace.
2. It **is** channel 1. The number of results you get back is a direct function of how much
   classified content matched.

Pre-filter in the retrieval query — `store.lexical(..., acl_groups=...)`, filtering in SQL rather
than after it.

## The approximate path needs its own design

Pre-filtering an ANN graph by removing nodes can **disconnect the region containing the answer**.
"We pre-filter" is therefore not one design — it is a different design for the exact and the
approximate paths, and the approximate one must be validated on measured recall inside the
permitted subset.

## What to say when you cannot close a channel

Latency is usually the one you cannot close cheaply. **Name it, price it, hand the decision
back:**

> *"There is a timing channel here. Closing it costs a fixed latency floor at roughly the p95 of
> the slowest permitted query. That is a decision for your security team against their threat
> model, not one I should make on a whiteboard."*

That scores better in a review than a confident fix, because a confident fix to a threat model
you have not been told is a guess wearing a suit.

## When this does not apply

**When existence is not secret.** If a user is permitted to know a document exists but not read
it — a common corporate setting — channels 1, 2 and 5 stop being leaks and the design gets much
cheaper. **Ask this first.** It is the single question that decides the architecture.

---

**Practise:** [EX-10 — Prove permission isolation](../../30-learning/exercises/ex-10-prove-permission-isolation.md) ·
**Worked through in:** [the deployment-engineer round](https://github.com/akash-coded/nanorag/discussions/categories/interview-prep), [#34](https://github.com/akash-coded/nanorag/discussions/34)
