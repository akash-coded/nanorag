# Eckart–Young–Mirsky, and why optimal reconstruction is not optimal retrieval

> **As asked:** *"Your LSA encoder truncates the SVD at rank k. Prove that is the best rank-k
> approximation you can make, and say in which norm. Then tell me why that does not mean it is
> the best encoder."*

## The theorem

Take the SVD of the term–document matrix, `A = UΣVᵀ`, with singular values ordered
`σ₁ ≥ σ₂ ≥ … ≥ σᵣ`. Keep the largest `k`:

$$
A_k = U_k \Sigma_k V_k^{\top}
$$

**Eckart–Young–Mirsky:** for any matrix `B` of rank at most `k`,

$$
\lVert A - A_k \rVert \;\le\; \lVert A - B \rVert
$$

and this holds in **both** the Frobenius norm and the spectral norm — which is the part worth
saying, because most people remember only one. The residual is exactly the energy in the
discarded singular values:

$$
\lVert A - A_k \rVert_F = \sqrt{\textstyle\sum_{i=k+1}^{r} \sigma_i^{2}}
$$

That gives you the practical rule for choosing `k`: plot the cumulative share of `Σσᵢ²` and pick
the knee. If 200 dimensions hold 90% of the energy, dimensions 201 onward are buying 10%.

## Why that is the wrong optimality for retrieval

Here is the trap, and it is the actual question:

**Eckart–Young optimises reconstruction. Retrieval does not care about reconstruction.**

Retrieval cares about whether the *ranking* of documents against a query is correct. Those are
different objectives, and the directions the SVD discards are the ones with the least variance
— which is not the same as the ones with the least **discriminative power**.

Concretely: a direction that separates two rare but frequently-confused entities may carry very
little total variance across the corpus and be truncated away. Reconstruction error barely
moves. Retrieval on exactly the queries that needed that distinction collapses.

This is why dimension is a **generalisation knob, not only a cost knob** — the framing notebook
04 §4.5 uses. Increasing `k` does not monotonically improve retrieval:

- too small — genuinely different documents collapse together
- too large — you retain noise directions, and the tail singular vectors are mostly sampling
  artefacts of your particular corpus

There is a middle, it is corpus-specific, and **it is found by measuring recall, not by
measuring reconstruction error.**

## What a strong answer adds

**LSA's actual failure mode.** It is linear and it is fitted to *this* corpus. A modern encoder
is trained on far more text and captures relations LSA structurally cannot — but LSA has one
property nothing else does here: **no download, no import, no network.** That is the entire
argument for it as the default, and it is written down as
[ADR-0003](../../../20-decisions/0003-lsa-default-encoder.md) with the falsifier attached.

**Where else the theorem shows up.** Product quantization, low-rank adapters, and PCA
whitening all lean on the same result. If asked to compress an existing embedding table, the
Eckart–Young answer — SVD and truncate — is correct **and** you should immediately say that you
would validate it on retrieval metrics rather than on reconstruction error, for the reason
above.

**The honest caveat about LSA specifically.** Applying SVD to raw counts is not quite the
classical setup; term weighting before the decomposition changes what "variance" means, and
sublinear TF scaling matters more than the choice of `k` over a wide range.

## Measure it here

`nanorag/embed.py` — the LSA embedder and its `dim` parameter.
[Notebook 04](https://github.com/akash-coded/nanorag/blob/main/notebooks/04_retrieval_methods_and_reranking.ipynb)
§4.5 sweeps dimension against evidence recall and shows the curve is not monotone.
