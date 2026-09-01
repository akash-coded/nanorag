# Q1 · Your client's assistant answers correctly about 80% of the time. They want 95%. You have four weeks. What do you do in week one?


**Testing:** whether you interrogate the number before acting on it; whether your instinct is
to build or to measure; whether you can tell a client that 95% may not be achievable.

**Answer.**

Before anything else I would ask three questions about the 80%, because the plan changes
completely depending on the answers. *Who measured it, on what set, and correct by whose
judgment?* If it came from a demo with twenty hand-picked questions, I do not have a baseline,
I have an anecdote — and week one is about replacing it.

Assuming there is something to work with, week one is:

**Days 1–2 — label 100 real failures.** Not synthetic ones. Pull them from production traffic
if there is any, from the client's own support queue if there is not. Hand-label each against
a fault-isolation procedure: was the gold evidence in the packed context at all? If not, was
it in the candidate pool? If it was in the context, is the answer entailed by it? That gives
four buckets — first-stage recall, ranking/packing, generation, and "the label or the question
is wrong."

**Day 3 — the distribution decides the plan.** If 70% of failures are retrieval misses, this
is a chunking and hybrid-retrieval engagement and I will spend three weeks there. If 70% are
grounding failures with correct evidence present, retrieval is fine and this is a prompt
contract, abstention and possibly a model-choice problem. Those are completely different
four-week plans, and picking the wrong one costs the whole engagement. I have seen teams spend
a month swapping embedding models to fix what turned out to be a packing bug.

**Days 4–5 — stand up a regression set.** Those 100 cases plus null questions the corpus
genuinely cannot answer. Freeze 15% of it and do not look at it again until the end. Without
the frozen slice, every number I report in week four is a number I tuned against.

**And I would reframe the target.** Some fraction of that 20% is unanswerable from the corpus
— the document does not exist, or it exists and is out of date. I would split the goal into
"answer correctly" and "refuse correctly", because refusing well is often the faster path to a
client-acceptable system, and it is nearly always the cheaper one. If after labelling I find
that 8% of queries are unanswerable, then 95% correct-or-correctly-refused is achievable and
95% correct is not, and that is a conversation to have in week one rather than week four.

**Red flags I would avoid:** jumping to "I'd try a better embedding model"; proposing three
changes at once so that no delta is attributable; accepting 95% as well-defined.

> **Run it:** [notebook 01 §1.6](../../../../notebooks/01_retrieval_and_evaluation_foundations.ipynb)
> executes exactly this tree over the full failure set and produces the distribution.

---
