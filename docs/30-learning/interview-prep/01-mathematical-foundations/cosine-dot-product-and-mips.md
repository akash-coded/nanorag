# Cosine, dot product, and why MIPS is not a metric space

> **As asked:** *"You L2-normalise your embeddings and then use dot product. Why is that the
> same as cosine? And when is throwing away the magnitude a bug rather than a convenience?"*

## The easy half

Cosine similarity is the dot product divided by both norms:

$$
\cos(q, d) = \frac{q \cdot d}{\lVert q \rVert\, \lVert d \rVert}
$$

If every vector is normalised so `‖v‖ = 1`, the denominator is 1 and cosine **is** the dot
product. More usefully: even without normalising the query, dividing by `‖q‖` is the same
positive constant for every document, and dividing all scores by a positive constant **cannot
change their order**. So for ranking, normalising the documents alone is enough.

That is why every vector index stores normalised vectors and computes inner products: one
multiply-accumulate per dimension, no square roots, and the ranking is identical.

## The half that is actually the question

**Normalising discards magnitude, and magnitude is not always noise.**

For many encoders `‖v‖` correlates with something real — document length, or how confidently
the model has placed the text. Two cases where discarding it hurts:

- **Length.** If magnitude tracks length, normalising removes your only length signal in the
  dense leg. BM25's `b` parameter exists precisely because length matters; the dense leg
  silently has no equivalent.
- **Confidence.** Some encoders give near-zero-norm vectors to inputs they cannot represent —
  boilerplate, tables, code. Normalising a near-zero vector **amplifies whatever noise it
  contains to unit length**, and that document now competes on equal terms with everything
  else. Worth checking on your own corpus: histogram `‖v‖` before normalising and look at the
  bottom percentile.

## Why MIPS is the hard case

If you *do* keep magnitude — maximum inner product search rather than cosine — the geometry
changes in a way that breaks index structures.

Inner product is **not a metric**. It fails the basic requirements:

- Not a distance to itself: `q·q = ‖q‖²`, which is not zero and is not minimal.
- **No triangle inequality.** A document can have a large inner product with `q` and with `q'`
  while `q` and `q'` are far apart.

Every tree- and pivot-based index — ball trees, k-d trees, anything using the triangle
inequality to prune — is **invalid** under MIPS. Not slower: wrong. It prunes branches that
contain the answer.

The standard escape is a reduction to nearest-neighbour search. Augment each document with an
extra coordinate that absorbs the magnitude difference:

$$
\tilde{d} = \left[\, d,\ \sqrt{M^2 - \lVert d \rVert^2} \,\right], \qquad
\tilde{q} = [\, q,\ 0 \,]
$$

with `M = maxᵢ‖dᵢ‖`. Now every `‖d̃‖ = M`, so all documents lie on one sphere, and

$$
\lVert \tilde q - \tilde d \rVert^2 = \lVert q\rVert^2 + M^2 - 2\,(q \cdot d)
$$

Minimising Euclidean distance in the lifted space maximises the inner product in the original
one. **You have converted MIPS into NNS by adding a dimension**, and metric indexes become
valid again.

## What a strong answer adds

**Know which one your stack is doing.** "We use cosine" and "we use dot product on unnormalised
vectors" are different systems with different valid index structures, and teams routinely do
not know which they have. The check is one line: are the stored vectors unit norm?

**And the practical trap.** If you normalise at index time but not at query time — or normalise
with one library's default and not another's — you get a system that *works*, returns
plausible results, and is quietly mis-ranked. Nothing errors. It is the same shape of failure
as the mixed-`embedder_tag` index in [ADR-0004](../../../20-decisions/0004-stable-chunk-ids.md):
**cosine returns well-formed numbers for vectors that mean nothing to each other.**

## Measure it here

`nanorag/store.py` — `exact_vector()` computes cosine over a float32 block.
`nanorag/embed.py` — check whether each embedder normalises, and what its norm distribution
looks like on this corpus.
