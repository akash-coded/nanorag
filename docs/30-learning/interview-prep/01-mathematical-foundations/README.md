# Mathematical foundations

The derivations behind the methods. This is where most candidates stop at the name of the
technique, and it is where a hard interview loop — Google, DeepMind, Palantir, a research lab —
spends its second half.

Each entry states the question the way an interviewer asks it, works the derivation, and names
**what a strong answer contains** beyond the algebra. Where the result is measurable in this
repository, the notebook cell is named.

## Retrieval and scoring

| | Question | Status |
|---|---|---|
| [BM25 from first principles](bm25-from-first-principles.md) | Derive the term-frequency component from the probabilistic relevance model. Why does it saturate, and what does `k₁` control? | ✅ |
| [Cosine, dot product and MIPS](cosine-dot-product-and-mips.md) | Why does L2 normalisation make them rank-equivalent, and when is that a bug? | ✅ |
| [Reciprocal rank fusion](reciprocal-rank-fusion.md) | Why `1/(k+rank)`? Why not `1/rank` or the nDCG discount? | ✅ |
| nDCG | Why a `log₂` discount, and what breaks when relevant-set sizes differ across queries? | ◻ planned |
| [Multi-hop recall](multi-hop-recall.md) | Per-passage recall is 0.938 and you need three passages. What is full-chain recall? | ✅ |

## Embeddings and approximate search

| | Question | Status |
|---|---|---|
| [Eckart–Young–Mirsky](eckart-young-and-svd.md) | Prove that truncating the SVD at rank `k` is the optimal rank-`k` approximation. In which norm? | ✅ |
| [Johnson–Lindenstrauss](johnson-lindenstrauss.md) | How many dimensions preserve pairwise distances among `n` points to within `ε`? | ✅ |
| [Navigable small-world graphs](navigable-small-world.md) | Why is greedy search `O(log n)`, and what breaks the guarantee? | ✅ |
| Product quantization | Derive the memory saving and the distortion cost. What is asymmetric distance computation? | ◻ planned |

## Evaluation and statistics

| | Question | Status |
|---|---|---|
| [Cohen's κ](cohens-kappa.md) | Derive it. Your judge and human agree 90% of the time — is that good? | ✅ |
| [The paired bootstrap and power](paired-bootstrap-and-power.md) | Why *paired*? How many eval questions to detect a 2-point gain? | ✅ |
| Multiple comparisons | You evaluate 12 slices and one is significant. What is wrong? | ◻ planned |
| Calibration and abstention | How do you know a score is calibrated? | ◻ planned |

---

**Contributing one:** open a thread in
[Q&A](https://github.com/akash-coded/nanorag/discussions/categories/q-a) with the derivation
before writing the file. Getting the argument reviewed is worth more than getting the file
merged, and the thread becomes the commentary the document does not have room for.
