# 🔍 The question decoder

> **When:** mid-round. What they are actually asking.

Interview questions are rarely about their surface topic. Each row below is the same question
asked twice.

| They ask | They are testing | Answer that scores |
|---|---|---|
| "How would you improve retrieval quality?" | Whether you measure first | "I'd attribute fifty failures before changing anything — the distribution decides the work" |
| "Why did you choose BM25?" | Whether you know its failure mode | "It cannot produce a synonym. That is why the dense leg exists and why fusion is not optional on a corpus with vocabulary mismatch" |
| "How do you evaluate a RAG system?" | Whether you separate stages | The [four verdicts](../frameworks/four-verdicts.md), and the trace field that decides each |
| "Your metric improved 3%. Ship it?" | Whether you know what an interval is | "What is the noise band at that eval-set size, and was that metric named primary before the run?" |
| "How would you reduce cost?" | Whether you know where cost lives | "Generation tokens are about a third of the bill. I'd look at re-embed cadence and cluster sizing first" |
| "Would you use a vector database?" | Whether you have opinions or preferences | "What are the filter requirements and the residency constraint? Those decide it, not the vector part" |
| "How do you handle hallucination?" | Whether you know abstention is unsolved | "Grounding plus a sufficiency check. No retrieval-score threshold works — I've measured four and they sit near chance" |
| "How big should chunks be?" | Whether you know it is corpus-dependent | "It is a bake-off, not a constant. What's the natural retrievable unit in their corpus?" |
| "Tell me about a project that failed" | Whether you can be wrong out loud | A real one, with the wrong hypothesis you held and what changed your mind |
| "Do you have any questions?" | Whether you were listening | One question about something they said, not from a list |

## The four escalation levels

A depth round descends until you stop. Knowing which level you are on tells you what to say.

| Level | Question | Stops most people |
|---|---|---|
| 1 | "What is BM25?" | — |
| 2 | "Why does term frequency saturate?" | Some |
| 3 | "Derive that from the probabilistic relevance model" | **Most** |
| 4 | "When does the derivation's assumption break, and why does it work anyway?" | Almost all |

**Level 4 is where the offer is decided.** For BM25: term independence is false, and it works
anyway because ranking only needs the *ordering* approximately right, not the probabilities
calibrated. Knowing which assumption is violated and why it does not matter is the difference
between recall and understanding.

## Questions that are traps

| Question | The trap | The move |
|---|---|---|
| "Would you use technique X?" | Answering yes or no | "What failure does it fix, and do we have it?" |
| "What's the best chunk size?" | Giving a number | "There isn't one. Here's the bake-off I'd run" |
| "Can you make it 10× faster?" | Promising | "Which of latency, quality and cost am I allowed to trade?" |
| "Our accuracy is 80%, get it to 95%" | Accepting the frame | "Accuracy measured how, on what set, labelled by whom?" |

## Your questions at the end

Ask one that only makes sense if you were listening. Good ones:

- *"You mentioned the eval set is maintained by the team that ships. Has that ever caused a
  conflict?"*
- *"What is the last retrieval change you shipped that you later reverted?"*
- *"How do you decide a technique is not worth adopting?"*

The last one is the best question in this document. **The answer tells you whether they measure.**
