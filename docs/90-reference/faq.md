# FAQ

Every discussion whose answer has been marked, grouped by category.

**Generated** by `scripts/harvest_faq.py` and refreshed weekly by the
`FAQ` workflow — edit the thread, not this file. The extract is the opening of
the accepted answer; the thread itself carries the argument that got there, which
is usually the more useful half.

11 answered threads.

## Design Reviews

### [Design review: retrieval for a regulated insurance client, 40M docs, strict ACLs](https://github.com/akash-coded/nanorag/discussions/34)

Synthesis of the three critiques, and what changes: What stays as designed and why: OpenSearch in-VPC, clause-level structural chunking, and hybrid-with-rerank all survive review unchanged.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/34)

### [Design review: should the sufficiency check be a model call or a classifier?](https://github.com/akash-coded/nanorag/discussions/35)

Decision: Option A, with Marcus's gate, staged. Phase 1 — model call on every query. Ship the thing that works. Pay the 300 ms and the money. Do not optimise a component whose value you have not yet measured.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/35)

## Interview Prep

### [Critique my answer: 'How would you separate a retrieval failure from a generation failure?'](https://github.com/akash-coded/nanorag/discussions/41)

A stronger answer, roughly as I would say it out loud: Why this scores. Panels are not testing whether you know the word "reranker". They are testing three things: Do you reach for evidence or for intuition?

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/41)

### [How do I talk about a synthetic-corpus project without it sounding like a toy?](https://github.com/akash-coded/nanorag/discussions/42)

The reframe: synthetic is a methodological choice, and you should say so first. The defensive answer is "it is synthetic, but…".

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/42)

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

## Reading Club

### [Lost in the Middle (Liu et al., 2023) — is the U-curve still true, and does it matter?](https://github.com/akash-coded/nanorag/discussions/38)

Where I would land on the three questions. 1 · Does it still hold? Directionally yes, magnitude unknown and model-specific. Priya's 0.071 is real on this setup and does not license a claim about GPT-scale models on long contexts.

[Read the thread →](https://github.com/akash-coded/nanorag/discussions/38)
