# Start here

Ten minutes, in order. If you only have one, read step 2.

## 1 · Run it

```bash
git clone https://github.com/akash-coded/nanorag.git
cd nanorag
make setup      # pip install -e ".[dev]" — the dev extras are required
make lab
```

There is no dataset to download, no API key to set and no service to start. The whole
retrieval stack lives inside `sqlite3.connect(":memory:")`. If something is downloading, you
have gone wrong.

## 2 · Read one notebook

[`notebooks/01_retrieval_and_evaluation_foundations.ipynb`](../../notebooks/01_retrieval_and_evaluation_foundations.ipynb),
end to end, then §1.3 again.

This is the one that matters even if you never read another. It establishes the idea the rest
of the repository is organised around: **a number without an interval is an anecdote.** If you
skip it and go straight to the toolkit, the retrieval code looks over-engineered, because you
cannot see what the harness is protecting against.

## 3 · Read one discussion

[#28 — why Recall@N goes up but full-chain recall stays flat](https://github.com/akash-coded/nanorag/discussions/28).

It is the most useful confusion in the material, and the thread shows the shape of how
questions get answered here: a measurement, a wrong turn, a correction with numbers.

## 4 · Pick your path

| You are… | Go to |
|---|---|
| working through the material | [`curriculum.md`](curriculum.md) |
| here to practise | [`../30-learning/exercises/`](../30-learning/exercises/) |
| preparing for an interview | [`../30-learning/interview-prep/`](../30-learning/interview-prep/) |
| going to change the code | [`../10-architecture/overview.md`](../10-architecture/overview.md) |
| putting this on a CV | [`portfolio.md`](portfolio.md) |
| stuck | [Discussions](https://github.com/akash-coded/nanorag/discussions) |

## What this is not

It is **not** a production RAG framework, and it is not trying to become one. Every component
you would normally install — the inverted index, the encoder, the ANN graph, the fusion, the
reranker, the judge, the cost model — is implemented here in readable Python so the mechanism
is visible rather than configured.

The corpus is **synthetic on purpose**: it is generated from a fact graph, so gold labels are
true by construction and there is no annotation-error floor under any number. That choice buys
measurement clarity and costs distributional realism, and both halves of that trade are stated
wherever the numbers appear.
