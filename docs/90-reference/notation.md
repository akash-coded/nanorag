# Notation

Symbols used across the notebooks, the docs and the discussion threads. Where a symbol is
overloaded in the literature, the meaning used *here* is the one given.

## Retrieval

| Symbol | Meaning | Note |
|---|---|---|
| `N` | Candidate pool size from stage one | Not the corpus size |
| `k` | Chunks packed into the prompt | The binding constraint on full-chain recall |
| `α` | Fusion weight, lexical vs dense | `score = α·dense + (1−α)·lexical`. Fitted per corpus; do not copy ours |
| `ef` | ANN search visit budget | Larger is more accurate and slower |
| `k₁`, `b` | BM25 saturation and length-normalisation constants | `k₁` controls how fast term frequency saturates; `b` interpolates between no length normalisation (`b=0`) and full (`b=1`) |
| `θ` | Abstention threshold | Swept, never assumed |

## Metrics

| Symbol | Meaning |
|---|---|
| **Evidence recall@k** | Share of a question's gold evidence present in the packed context. Continuous |
| **Full-chain recall** | 1 if **every** gold item for a question is present, else 0. Binary, so higher variance |
| **Full-chain recall@N** | The same conjunction measured over the candidate pool rather than the packed context. The gap between this and full-chain recall is packing loss |
| **Context precision** | Share of packed chunks that are gold. Falls as `k` rises |
| **nDCG@k** | Discounted cumulative gain, normalised per query by that query's ideal ordering |
| **κ** | Cohen's kappa — agreement corrected for chance: `(pₒ − pₑ)/(1 − pₑ)` |

## Statistics

| Term | Meaning here |
|---|---|
| **Noise band** | The 95% interval of the paired bootstrap on the *unchanged* system. A delta inside it is not a result |
| **Paired bootstrap** | Resamples questions with replacement, keeping both arms on the same questions. Pairing removes per-question difficulty, which is the dominant variance term |
| `n_boot` | Number of bootstrap resamples. Controls how precisely the interval is *estimated*, **not** how wide it is |
| `n` | Number of eval questions. This is what controls interval width |
| **Winner's curse** | A delta that only just reached significance is more likely than not an overestimate. Budget for it when sizing a follow-up |

## The distinction people get wrong most often

`n_boot` and `n` are not interchangeable.

- **`n` is how much uncertainty there is.** Set by the eval set.
- **`n_boot` is how carefully you measure that uncertainty.** Set by your patience.

Raising `n_boot` from 2,000 to 100,000 stabilises the digits and does not narrow the
interval. Worked through in
[discussion #29](https://github.com/akash-coded/nanorag/discussions/29).
