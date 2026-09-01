# BM25 from first principles

> **As asked:** *"Everyone uses BM25. Derive the term-frequency component from the probabilistic
> relevance model, and tell me what `k₁` and `b` actually control."*

## Where the formula comes from

Start from the **probabilistic relevance framework**: rank documents by the odds that a document
is relevant given the query. Under a term-independence assumption, taking logs turns the product
over query terms into a sum, and the weight for each term is the log odds ratio

$$
\text{IDF}(t) \;=\; \log \frac{N - n_t + 0.5}{n_t + 0.5}
$$

where `N` is the number of documents and `n_t` the number containing `t`. The `0.5` terms are a
smoothing correction; the shape is the point. **This is the Robertson–Sparck Jones weight**, and
it falls out of the odds ratio rather than being chosen for convenience.

Note it goes **negative** once a term appears in more than about half the collection. A term in
most documents is weak evidence *against* relevance, which is the principled version of a stop
list.

## Why term frequency saturates

The naive model treats each occurrence of a term as independent evidence, so evidence grows
linearly with `tf`. That is wrong, and the **2-Poisson model** says why: documents are a mixture
of an *elite* set, about which the term is genuinely a topic, and a non-elite set where it
occurs incidentally. What we want to estimate is the probability of eliteness given `tf`, and
that probability is **concave and bounded** — it rises quickly over the first few occurrences
and then flattens, because a document mentioning a term twenty times is not twice as on-topic as
one mentioning it ten times.

The 2-Poisson estimate has no closed form that is cheap to compute, so BM25 uses the simplest
function with the right shape:

$$
\frac{tf}{k_1 + tf} \quad\longrightarrow\quad 1 \text{ as } tf \to \infty
$$

**`k₁` is the saturation rate.** At `k₁ → 0` the function becomes a step: presence or absence,
and BM25 degenerates toward a boolean model. At large `k₁` it is nearly linear over the range of
real `tf` values, recovering the naive count model. Typical values sit around `1.2–2.0`, where
the third occurrence of a term is worth noticeably less than the first and the tenth is worth
almost nothing extra.

## Why length normalisation is interpolated

A long document has more term occurrences by construction, so raw `tf` rewards length. But
length is ambiguous evidence: a document can be long because it is *verbose* (should be
penalised) or because it is *comprehensive* (should not). BM25 refuses to choose and
interpolates:

$$
\text{norm} = 1 - b + b\cdot\frac{|d|}{\text{avgdl}}
$$

**`b = 0`** applies no length normalisation. **`b = 1`** applies it fully, scaling `tf` by the
ratio of document length to the collection average. `b ≈ 0.75` is the usual compromise. Putting
it together:

$$
\text{BM25}(q,d) = \sum_{t \in q} \text{IDF}(t)\cdot\frac{tf_{t,d}\,(k_1+1)}{tf_{t,d} + k_1\left(1-b+b\frac{|d|}{\text{avgdl}}\right)}
$$

The `(k₁+1)` in the numerator is cosmetic — it makes a single-occurrence term score `1` when
`|d| = avgdl`, and changes no ranking.

## What a strong answer adds

**1 · The failure mode that is not in the formula.** BM25 scores whatever the *analyzer* gives
it. This repository shipped a bug — [#1](https://github.com/akash-coded/nanorag/issues/1) —
where SQLite's default `unicode61` tokenizer split `ERR_CONN_RESET` into `err`, `conn`, `reset`,
each appearing in every incident report. IDF for all three was near zero, so the query matched
everything and ranked nothing. **The scoring function was flawless and the results were wrong.**
Nothing errored. That is the answer that separates someone who has run BM25 from someone who has
read about it.

**2 · Where the derivation's assumptions break.** Term independence is false — "machine" and
"learning" are not independent. BM25 works anyway because ranking only needs the *ordering* to be
approximately right, not the probabilities to be calibrated. Being able to say which assumption
is violated and why it does not matter is the mark of understanding rather than recall.

**3 · What it structurally cannot do.** No setting of `k₁` or `b` gives BM25 a synonym. It is
exact lexical matching with a good weighting scheme, which is exactly why the dense leg exists
and why fusion is not optional on a corpus with vocabulary mismatch.

## Measure it here

`nanorag/store.py` implements BM25 over SQLite FTS5.
[Notebook 04](https://github.com/akash-coded/nanorag/blob/main/notebooks/04_retrieval_methods_and_reranking.ipynb)
§4.3 builds the inverted index by hand and sweeps `k₁` and `b`, and
[EX-11](../../exercises/ex-11-bm25-by-hand.md) has you score three documents with a pen before
running anything.
