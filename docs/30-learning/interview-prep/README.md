# Interview preparation

Eighteen questions AI-engineer, applied-ML and forward-deployed-engineer panels actually ask about retrieval, with
the answer a strong senior candidate gives — not a definition, but the *procedure* they walk,
the tradeoff they name unprompted, and the number they reach for.

**How to use this.** Read the "what the panel is testing" column first and answer out loud
before reading the model answer. The gap between your answer and the model one is your study
plan. Every question links to the notebook where you can *run* the thing you are describing,
because an answer you have executed sounds different from one you have read.

---

## How panels actually score

Before the questions, the sheet they are scoring against. Most candidates lose points on
**Tradeoffs** and **Numbers**, not on knowledge.

| Dimension | Signal | Anti-signal |
|---|---|---|
| **Problem framing** | Asks what is being measured, and on which set, before proposing anything | Starts naming tools and vendors in the first minute |
| **Debugging** | Bisects: isolates a stage, compares against a known-good reference | Lists plausible causes with no way to eliminate any of them |
| **Tradeoffs** | States the cost of their own recommendation, unprompted | Presents an option with only upsides |
| **Numbers** | Estimates cost and latency out loud, then sanity-checks the magnitude | "It depends on the workload", with no attempt at an estimate |
| **Scope control** | Sequences work; says what they would *not* do in the time available | Proposes a full rebuild for a four-week engagement |
| **Client posture** | Turns a demand into a quantified choice the client can own | Either agrees to everything, or refuses with no alternative |
| **Honesty** | "I don't know — here is how I'd find out in a day" | Confident numbers that fall apart on one follow-up |

---

---

## The question bank

### Scenario and system design

| | Question |
|---|---|
| [`Q1`](03-system-design/q1-your-client-s-assistant-answers-correctly-about-80-o.md) | Your client's assistant answers correctly about 80% of the time. They want 95%. You have four weeks. What do you do in week one? |
| [`Q2`](03-system-design/q2-a-retrieval-change-raises-average-answer-quality-6-b.md) | A retrieval change raises average answer quality 6%, but one business unit reports the system got worse. Do you ship it? |
| [`Q3`](03-system-design/q3-you-upgraded-the-embedding-model-and-evidence-recall.md) | You upgraded the embedding model and Evidence Recall@10 fell from 0.86 to 0.71. Walk me through the diagnosis. |
| [`Q4`](03-system-design/q4-legal-requires-that-no-answer-can-be-influenced-by-a.md) | Legal requires that no answer can be influenced by a document the user is not allowed to read. Design for that. |
| [`Q5`](03-system-design/q5-agentic-search-costs-0-90-on-hard-questions-finance-.md) | Agentic search costs $0.90 on hard questions. Finance wants $0.15. What do you change, and what do you refuse to change? |
| [`Q6`](03-system-design/q6-your-llm-judge-says-quality-went-up-how-would-you-kn.md) | Your LLM judge says quality went up. How would you know if the judge is wrong? |

### Technical depth

| | Question |
|---|---|
| [`Q7`](02-technical-depth/q7-when-would-you-use-bm25-dense-retrieval-or-a-hybrid.md) | When would you use BM25, dense retrieval, or a hybrid? |
| [`Q8`](02-technical-depth/q8-why-does-l2-normalisation-change-the-relationship-be.md) | Why does L2 normalisation change the relationship between cosine similarity and dot product? |
| [`Q9`](02-technical-depth/q9-how-do-early-interaction-and-late-interaction-rerank.md) | How do early-interaction and late-interaction rerankers differ? |
| [`Q10`](02-technical-depth/q10-how-do-you-select-chunk-size-and-overlap-for-a-mixed.md) | How do you select chunk size and overlap for a mixed-format corpus? |
| [`Q11`](02-technical-depth/q11-what-trace-data-is-required-to-reproduce-an-answer-f.md) | What trace data is required to reproduce an answer failure? |
| [`Q12`](02-technical-depth/q12-how-would-you-design-a-rag-pipeline-for-documents-th.md) | How would you design a RAG pipeline for documents that change daily? |
| [`Q13`](02-technical-depth/q13-which-metadata-belongs-in-the-index-and-which-belong.md) | Which metadata belongs in the index, and which belongs in the prompt? |
| [`Q14`](02-technical-depth/q14-how-would-you-tune-top-k-when-answer-quality-improve.md) | How would you tune top-k when answer quality improves but latency and cost rise? |
| [`Q15`](02-technical-depth/q15-how-do-you-detect-and-mitigate-lost-in-the-middle.md) | How do you detect and mitigate "lost in the middle"? |
| [`Q16`](02-technical-depth/q16-when-should-a-rag-system-abstain-instead-of-answerin.md) | When should a RAG system abstain instead of answering? |
| [`Q17`](02-technical-depth/q17-how-do-offline-evaluation-and-production-monitoring-.md) | How do offline evaluation and production monitoring complement each other? |
| [`Q18`](02-technical-depth/q18-what-would-block-a-retrieval-model-release-in-your-e.md) | What would block a retrieval-model release in your evaluation pipeline? |

### Mathematical foundations

The derivations behind the methods — where most candidates stop at the name of the
technique. See [`01-mathematical-foundations/`](01-mathematical-foundations/).

# Part 3 — Questions to ask *them*

Panels score you on the questions you ask, and these also tell you whether the role is real.

1. **"How do you currently know when retrieval quality regresses?"** — If the answer is "users
   tell us", you would be building the measurement layer, and that is worth knowing before you
   sign.
2. **"What is in your eval set, and who labelled it?"** — Reveals whether there is a
   ground-truth culture or a demo culture.
3. **"What is the cost of a wrong answer reaching a user in this product?"** — Determines
   whether you need an inline guardrail on day one or after the pilot. It is the single most
   architecture-shaping question you can ask.
4. **"How does a document change reach the index, and how long does it take?"** — Tells you
   whether the freshness path exists or whether somebody re-runs a notebook.
5. **"When did you last re-run your index-time enrichment?"** — A great question because most
   teams have never thought about it.
6. **"Who owns the decision when the average improves and one segment regresses?"** — Tells you
   whether there is an owner or a committee.

---

## A note on how to answer

The single biggest difference between a mid-level and a senior answer in these interviews is
not knowledge. It is that the senior candidate **states the cost of their own recommendation
before being asked**, and **reaches for a number where a mid-level candidate reaches for an
adjective**.

If you take one habit from this document: after every recommendation you make in an interview,
add one sentence beginning *"what this costs us is…"*. It is the fastest way to move from the
anti-signal column to the signal column on the sheet at the top of this page.
