# Q2 · A retrieval change raises average answer quality 6%, but one business unit reports the system got worse. Do you ship it?

**Testing:** whether you treat an aggregate as evidence or as a summary that hides its own
counterexample; whether you will actually make a decision.

**Answer.**

Not yet — but I will decide this week, not "investigate further" indefinitely.

**Reproduce before believing.** Pull that unit's real queries, run both configurations, and
check whether the regression appears in the metrics at all. Perceived regressions are
sometimes a UI change, a change in what users started asking, or one loud incident. If it does
not reproduce, that is a conversation with the unit, not a rollback.

**If it reproduces, find the mechanism.** A unit-specific regression almost always has a
concrete cause. Two I have seen: their corpus is identifier-heavy and the change shifted
fusion weight toward the dense leg, so error codes stopped matching exactly; or their documents
are much shorter than average and a chunking change moved `avgdl`, which silently re-tuned
every BM25 score in the index. Both are findable in an afternoon by slicing the metrics by
tenant and looking at the queries that moved most.

**Then prefer a per-segment configuration over an all-or-nothing ship**, if the mechanism
supports it. Routing α by query class, or running that tenant on the previous fusion weights,
is usually cheaper than either losing the 6% or losing the stakeholder. It costs a second
configuration to maintain, and I would say that out loud rather than pretending it is free.

**And make the decision explicit and owned.** If I ship despite the regression, that unit's
owner hears it from me first, with the number, the mechanism, and a remediation date — not
from their users. If I hold the change, the rest of the business hears why they are not getting
the 6%.

The thing I would refuse to do is ship on the average and let the unit discover it. An
aggregate that improved while a named segment got worse is exactly the case my release gate
blocks by default, and overriding a gate is a decision that gets logged with a name on it.

> **Run it:** [notebook 06 §6.4](../../../../notebooks/06_evaluation_approaches.ipynb) executes the
> release-gate tree against a real candidate change, including the per-slice check.

---
