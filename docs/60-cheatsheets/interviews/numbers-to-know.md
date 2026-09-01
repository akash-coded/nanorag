# 📐 Numbers worth memorising

> **When:** you want to be able to produce a number cold, without a laptop.

Not trivia. Each of these settles an argument, and each one is either an arithmetic you can do in
your head or a measured result you can cite with its condition attached.

## Arithmetic you should be able to do out loud

| Quantity | The calculation | Worked |
|---|---|---|
| **Multi-hop recall floor** | `r^hops` under independence | `0.86³ ≈ 0.64` — and it is a *lower bound*, because hops correlate |
| **Eval-set size for a delta** | `n × (half_width / point_estimate)²`, then **double it** | `207 × (0.046/0.034)² ≈ 383` → budget ~750 |
| **Chance agreement** | `p₁p₂ + (1−p₁)(1−p₂)` | 90/10 split: `pₑ = 0.82`, so 94% raw agreement is `κ ≈ 0.67` |
| **JL bound** | `d ≈ 8 ln n / ε²` | `n=10⁶, ε=0.1` → **≈11,000 dimensions**, which is the surprise |
| **Binary metric variance** | `p(1−p)`, maximal at `p=0.5` | `0.25` — worst exactly where interesting systems live |
| **Noise band, rough** | `≈ 2 / √n` for a binary metric | `n=200` → about ±0.14 at worst; ±0.06 typical |

## Measured here — cite with the condition

| Number | What it is | The condition that makes it true |
|---|---|---|
| **31%** | Share of a monthly bill that is generation tokens | Mid-size deployment, self-hosted encoder |
| **0.469 → 0.531** | Full-chain recall from a per-entity packing constraint | `k=8`, +1.2% tokens |
| **0.469 → 0.548** | Same metric from raising `k` to 16 | **+93% tokens**, `context_precision` 0.52 → 0.31 |
| **84 vs 27** | Found-then-dropped vs never-retrieved | The bottleneck was 3:1 on the packing stage |
| **0.849 → 0.752** | Evidence recall *after* adding a lexical-only reranker | A reranker over the same signals is worse than none |
| **0.38** | Best abstention F1 by retrieval-score threshold | Full eval set at its real 15% null base rate |
| **+0.0338 → +0.0116** | The same delta re-measured at n=812 | The winner's curse was most of the effect |

## Orders of magnitude

| | |
|---|---|
| Vector storage | `4 × dim` bytes per chunk, float32. 1M chunks × 768 dim ≈ **3 GB** |
| BM25 index | Roughly the size of the text, often less |
| Rerank cost | **Linear in candidates**, nothing precomputable — this is why depth matters |
| Cross-encoder latency | ~10–50 ms per pair. At depth 50 that is the latency budget |
| Embedding throughput | Plan in GPU-hours per million chunks, not seconds per chunk |

## The three constants not to memorise

- **`α = 0.2`** — fitted to *this* corpus and *this* encoder. Quoting it elsewhere is the error
  the README warns about
- **`k = 8`** — a budget decision, not a fact
- **`chunk size = 512`** — there is no right answer; it is a bake-off

**Knowing which numbers do not transfer is worth more than knowing the ones that do**, and saying
so unprompted is a strong signal.

## The one to lead with

> *"On a binary metric, per-question variance is `p(1−p)` — about 0.25, and it peaks at the 0.5
> accuracy where interesting systems sit. So the same true effect will clear the band on a
> continuous metric and not on a binary one. That is one effect at two levels of statistical
> power, not two contradictory results."*

It is short, it is exactly right, and it demonstrates the thing most candidates cannot: that you
know why your own metrics disagree.
