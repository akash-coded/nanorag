# Johnson–Lindenstrauss, and what it does not promise

> **As asked:** *"You want to cut embedding dimension from 1536 to 256 to save memory. How many
> dimensions do you actually need to preserve the geometry?"*

## The lemma

For any set of `n` points in any dimension, and any `ε ∈ (0, 1)`, there is a linear map into

$$
d = O\!\left(\frac{\log n}{\varepsilon^{2}}\right)
$$

dimensions that preserves all pairwise distances to within a factor `(1 ± ε)`. A random
projection — Gaussian entries, or `±1` entries scaled by `1/√d` — works with high probability.

Two properties make it striking:

- **The target dimension does not depend on the original dimension.** 1536 or 15,360, the
  bound is the same. It depends on how many points you have and how much distortion you accept.
- **It is logarithmic in `n`.** Ten times the corpus costs you a constant factor more
  dimensions, not ten times.

Put numbers on it, because the constant is where the surprise lives. For `n = 10⁶` and
`ε = 0.1`, the standard bound `d ≥ 8 ln n / ε²` gives roughly

$$
d \approx \frac{8 \times 13.8}{0.01} \approx 11{,}000
$$

**Eleven thousand dimensions to guarantee 10% distortion on a million points.** The lemma is not
telling you to compress to 256.

## Why 256 works anyway

Because the bound is a **worst-case guarantee over adversarial point sets**, and real embeddings
are nothing like adversarial. They lie close to a low-dimensional manifold, so their *intrinsic*
dimension is far below their ambient dimension, and random projection preserves what matters far
better than the bound requires.

The honest statement in an interview: *"JL says how many dimensions I would need to guarantee it
for arbitrary points. It is a bound, not a target. In practice I would sweep the dimension and
measure recall, and I would expect to go far below the bound because the data has structure the
lemma is not allowed to assume."*

## The three things it does not promise

**1 · It says nothing about inner products with a query outside the set.** JL preserves
distances *among the projected points*. Retrieval computes a similarity between a **query** —
which was not in the set the projection was chosen for — and the documents. Related results
cover this, but the plain lemma does not, and this is the gap the question is usually probing.

**2 · Preserving distance is not preserving *ranking*.** A `(1 ± ε)` distortion can reorder two
documents whose true distances are within `2ε` of each other. **Retrieval is a ranking problem,
and near-ties are exactly where the interesting decisions live.** Distance-preservation is a
weaker guarantee than it sounds.

**3 · A random projection is not a learned one.** Learned reduction — PCA, an autoencoder,
Matryoshka-style training — beats random projection at a fixed budget, because it can use the
data distribution. JL's advantage is that it needs no training and no data, and degrades
gracefully. That is a real advantage when you cannot retrain.

## What a strong answer adds

**Name the practical alternative.** If the encoder was trained with nested representations, the
first `k` dimensions are *already* a usable embedding — truncate and renormalise, no projection
matrix. Cheaper and better than JL, when available.

**And name the measurement.** Whatever the theory says, the decision is made by sweeping `d`
against evidence recall on your own corpus and finding where the curve bends. The lemma tells
you the shape to expect — graceful degradation, then a cliff — and roughly where not to bother
looking.

## Measure it here

[Notebook 04](https://github.com/akash-coded/nanorag/blob/main/notebooks/04_retrieval_methods_and_reranking.ipynb)
§4.5 treats dimension as a generalisation knob rather than only a cost knob, and shows the
non-monotone curve. `nanorag/embed.py` includes a hashing embedder, which is a random
projection of the term space and the closest thing here to JL in practice.
