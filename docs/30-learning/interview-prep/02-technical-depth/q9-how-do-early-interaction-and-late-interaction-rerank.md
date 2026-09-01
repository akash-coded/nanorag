# Q9 · How do early-interaction and late-interaction rerankers differ?

A cross-encoder (early interaction) concatenates query and passage and runs full attention over
both, so every query token can attend to every passage token. Highest quality. Nothing can be
precomputed because the representation depends on the pair, so cost is linear in N — reranking
100 candidates is 100 forward passes, per query, every query. Typically 50–300 ms batched at
N≈50, and *batched* is doing real work in that sentence: the difference between batching and
looping is often 90 ms versus 900 ms.

Late interaction (ColBERT-style) encodes query and passage tokens independently, keeps
token-level vectors, and scores with MaxSim at query time. Passage representations are
precomputable, so online latency drops to 10–40 ms. The cost is storage: 10–100× a single
vector per chunk. That multiplier is the part candidates forget, and it is the reason late
interaction is a strict-SLA choice rather than a default.

The default is a cross-encoder at N≈50. Everything else needs a reason.
