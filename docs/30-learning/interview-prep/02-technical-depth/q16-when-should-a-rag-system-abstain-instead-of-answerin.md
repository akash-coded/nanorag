# Q16 · When should a RAG system abstain instead of answering?


When the evidence does not entail an answer. That sounds obvious and the important part is
what it rules out: **it is an entailment judgment, not a similarity score.**

I have measured this. On an eval set with deliberately-constructed unanswerable questions, no
retrieval-side signal separated answerable from unanswerable — not the reranker score, not
IDF-weighted coverage, not sentence-level rare-term coverage, not a conjunctive corpus-presence
check. Best F1 was 0.38. The reason is visible once you look at the questions rather than the
scores: unanswerable questions often name real entities in the corpus's own vocabulary, while
real user questions paraphrase. The unanswerable ones are *lexically closer* to the corpus.

So abstention lives in the generation contract — one exact refusal token so it is parseable,
not "I'm not sure" — verified by a cheap sufficiency check as a separate call, and scored
against a null set that is part of your eval set from day one. In a regulated product you also
want an inline guardrail that blocks before the reply is sent, which is a different component
from the offline judge that teaches you what to fix.
