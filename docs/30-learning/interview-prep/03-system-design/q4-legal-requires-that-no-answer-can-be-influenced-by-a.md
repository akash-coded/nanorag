# Q4 · Legal requires that no answer can be influenced by a document the user is not allowed to read. Design for that

**Testing:** whether you hear "influenced" and realise post-filtering does not satisfy it;
whether caches, logs and traces are part of your security boundary; whether you name the
recall cost up front rather than discovering it in UAT.

**Answer.**

The word that matters is *influenced*, and it rules out the design most people reach for.

**Post-filtering does not satisfy this.** If you retrieve top-k globally and then drop what the
user may not see, the restricted documents were candidates: they occupied ranks, they shifted
every permitted document beneath them, and they were in the reranker's batch. The answer was
influenced by them even though none appear in it. There are two observable failures too — `k`
collapses, so a narrowly-scoped user gets two chunks instead of eight and a worse answer with
no explanation; and the existence of restricted documents is inferable from result counts and
latency.

**So: pre-filter, always.** The ACL predicate goes *into* the query — into the SQL `WHERE` for
the lexical leg and into the ANN search for the dense leg — so restricted chunks are never
candidates and never contribute to a score, a rank, or a rerank batch.

**Name what it costs, up front.** A highly selective pre-filter degrades graph-based ANN
indexes: the traversal can only walk through nodes it is allowed to see, so when those are
sparse it dead-ends in a region far from the answer, at the same `efSearch`. Mitigate with
per-tenant namespaces or a partitioned index, and — this is the part teams skip — **measure
recall with the real filters on**, not without them. A benchmark that reports 0.99 recall
unfiltered tells you nothing about production.

**Close the side channels**, because the index is not the whole boundary:

- Prompt caches keyed per tenant. A shared prefix cache across tenants is a data-leak class of
  bug, not a performance issue.
- Traces store retrieved text, so the trace store inherits the corpus's compliance boundary —
  including its retention policy and its jurisdiction.
- Result counts and latency should not vary observably with what exists but is hidden.

**Revocation has an SLA.** If ACLs are denormalised onto chunks for speed, they need their own
change-capture stream, and I should be able to state the propagation lag in minutes. If legal
needs sub-minute revocation, denormalisation is off the table and we resolve per request,
which costs latency on every query — that is a tradeoff for them to own.

**And prove it.** An automated test that runs the same query as two personas and asserts
disjoint evidence sets, in the release gate, not as a one-off review. If someone later changes
the filter, the chunking, or the ACL denormalisation, the build fails rather than UAT.

> **Run it:** [notebook 03 §3.7](../../../../notebooks/03_rag_system_design.ipynb) measures the
> k-collapse and runs the two-persona isolation test;
> `tests/test_retrieval.py` has it wired into CI.

---
