# FAQ

Every discussion whose answer has been marked, grouped by category.

**Generated** by `scripts/harvest_faq.py` and refreshed weekly by the
`FAQ` workflow — edit the thread, not this file. The extract is the opening of
the accepted answer; the thread itself carries the argument that got there, which
is usually the more useful half.

20 answered threads.

## Design Reviews

### [Retrieval for a regulated insurer — 40M docs, per-clause ACLs, 12 weeks](https://github.com/akash-coded/nanorag/discussions/34)

Synthesis of the three critiques, and what changes: What stays as designed and why: OpenSearch in-VPC, clause-level structural chunking, and hybrid-with-rerank all survive review unchanged.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/34)

### [Sufficiency check: a cheap model call, or a trained classifier?](https://github.com/akash-coded/nanorag/discussions/35)

Decision: Option A, with Marcus's gate, staged. Phase 1 — model call on every query. Ship the thing that works. Pay the 300 ms and the money. Do not optimise a component whose value you have not yet measured.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/35)

### [A support desk where a document edited five minutes ago must be findable](https://github.com/akash-coded/nanorag/discussions/149)

The design is sound. What is missing is what is missing from most freshness designs: how do you know the SLA is being met? "Retrievable within 60 seconds" is a claim about a distribution and nothing measures it.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/149)

### [Multi-tenant retrieval where two tenants want different encoders](https://github.com/akash-coded/nanorag/discussions/150)

What will actually hurt is neither of those. It is that you now have two code paths and one eval set. The shared path is exercised by 38 tenants continuously. The dedicated path holds your two largest accounts and is exercised rarely.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/150)

## Interview Prep

### [Critique my answer: 'How would you separate a retrieval failure from a generation failure?'](https://github.com/akash-coded/nanorag/discussions/41)

A stronger answer, roughly as I would say it out loud: Why this scores. Panels are not testing whether you know the word "reranker". They are testing three things: Do you reach for evidence or for intuition?

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/41)

### [How do I talk about a synthetic-corpus project without it sounding like a toy?](https://github.com/akash-coded/nanorag/discussions/42)

The reframe: synthetic is a methodological choice, and you should say so first. The defensive answer is "it is synthetic, but…".

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/42)

### [[round · deployment-engineer shape] 45 minutes: retrieval over classified documents](https://github.com/akash-coded/nanorag/discussions/90)

A strong answer, roughly as I would give it. How this is scored The single highest-scoring move is putting the isolation test before the retrieval work.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/90)

### [Critique my answer: 'How would you evaluate a RAG system?'](https://github.com/akash-coded/nanorag/discussions/151)

A stronger answer, roughly as I would say it out loud: Why this scores It leads with the constraint — no labels — rather than a finished system. The shape of the answer reveals whether you have done this before the content does.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/151)

### [[round · platform shape] Ten billion documents, fifty milliseconds](https://github.com/akash-coded/nanorag/discussions/152)

How it is scored The two answers that decide it 1 · "The dense leg cannot be stage one at this scale." Most candidates put the vector index first because that is what tutorials do.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/152)

### [[round · research-lab shape] Design the experiment that would falsify this paper](https://github.com/akash-coded/nanorag/discussions/154)

A strong answer, roughly as I would give it: Why this scores We ran this on ourselves #37 measured contextual chunking on this corpus: worse on both quality metrics at 2.4× storage.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/154)

## Q&A

### [Why does Recall@N go up but full-chain recall stay flat?](https://github.com/akash-coded/nanorag/discussions/28)

This is the most useful confusion in the whole curriculum, so it is worth answering at length. Recall@N and full_chain_recall measure different stages. Recall@N is about the candidate pool: did stage one find the evidence at all?

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/28)

### [My reranker improved evidence recall but full-chain recall is 'inside the noise band'. Do I ship it?](https://github.com/akash-coded/nanorag/discussions/29)

Both verdicts are correct, and understanding why is worth more than the answer to "should I ship". Why the intervals differ despite equal point estimates.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/29)

### [Should I use RRF or weighted fusion? The notebook says RRF is the default but then measures it losing.](https://github.com/akash-coded/nanorag/discussions/30)

Both statements are right, and the resolution is a procedure rather than a preference. The advice is: default to RRF, then measure.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/30)

### [Why is `answer_correct` so low on temporal questions when retrieval looks fine?](https://github.com/akash-coded/nanorag/discussions/31)

Retrieval is not lying. You have found the seam between the retrieval lane and the answer lane, and it is a good thing you looked. The offline reader is extractive. It selects and cites supporting sentences from the packed evidence.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/31)

### [Can I use these numbers in a client conversation?](https://github.com/akash-coded/nanorag/discussions/32)

The numbers, no. The arithmetic and the method, absolutely — and that is the more valuable half anyway. Three reasons the absolute values do not transfer: 1 · The corpus is synthetic.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/32)

### [The notebook gives different numbers than the README. Which is right?](https://github.com/akash-coded/nanorag/discussions/33)

Almost always a stale kernel holding an older nanorag module. Restart the kernel and run all cells from the top. bootstrap() pins the seed but it cannot un-import a module Python already loaded.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/33)

### [[maths] How small can I make my embeddings before retrieval degrades?](https://github.com/akash-coded/nanorag/discussions/92)

1 · It says nothing about your query. JL preserves distances among the projected points. Retrieval computes a similarity between a query, which was not in the set the projection was chosen for, and the documents.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/92)

### [[maths] My judge agrees with me 94% of the time. Why is that not good enough?](https://github.com/akash-coded/nanorag/discussions/93)

Three things to take from it. 1 · Raw agreement is uninterpretable without the marginals. The full derivation, including why κ has that particular denominator, is in Cohen's κ.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/93)

### [[maths] Should I normalise my embeddings? What actually breaks if I do not?](https://github.com/akash-coded/nanorag/discussions/94)

If you keep magnitude, you are doing MIPS, and MIPS is not a metric space. Inner product fails the requirements outright: q·q = ‖q‖² is neither zero nor minimal, and there is no triangle inequality.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/94)

## Reading Club

### [Lost in the Middle (Liu et al., 2023) — is the U-curve still true, and does it matter?](https://github.com/akash-coded/nanorag/discussions/38)

Where I would land on the three questions. 1 · Does it still hold? Directionally yes, magnitude unknown and model-specific. Priya's 0.071 is real on this setup and does not license a claim about GPT-scale models on long contexts.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/38)
