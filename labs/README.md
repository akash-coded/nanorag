# L.A.B. simulator

**L**ook · **A**ttribute · **B**uild — one loop, eight tracks.

Two sizes. **Challenges** (`C`) are 5–15 minutes and one mechanism each, in four
shapes — `implement`, `fill` (blanks), `fix` (a planted bug), `predict` (submit the
number). Finishing one points you at the **lab** (`L`) it unlocks: 15–50 minutes,
a real decision, and public plus hidden checks.

Read [the method](../docs/80-lab/README.md) first. Then:

```bash
python scripts/lab.py next        # what you can start now
python scripts/lab.py run L01     # public checks
python scripts/lab.py run L01 --hidden
python scripts/lab.py status      # how far through you are
```

Difficulty: 🟢 easy · 🟡 medium · 🔴 hard · ⚫ boss (a track capstone)

## T1 · Corpus & Chunking

**Discovery** — hands on a corpus spec: what is in scope, what the retrievable unit is.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟢 | [`C01`](C01-sentence-boundary/brief.md) | fill | Fill the sentence-boundary rule | 8m | — |
| 🟢 | [`L01`](L01-stable-chunk-ids/brief.md) | lab | Give a chunk an id that survives an edit | 15m | — |
| 🟡 | [`L02`](L02-heading-path/brief.md) | lab | Carry the heading path into every chunk | 25m | `L01` |

## T2 · Indexing & Retrieval

**Design** — hands on an ADR: the retrieval design, and the alternative that lost.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟢 | [`C02`](C02-tokenizer-bug/brief.md) | fix | The tokenizer has a bug. Find it. | 10m | — |
| 🟢 | [`C03`](C03-idf-sign/brief.md) | predict | Predict the sign of IDF for a common term | 5m | — |
| 🟢 | [`L03`](L03-idf-by-hand/brief.md) | lab | Compute BM25's IDF, and find where it goes negative | 15m | — |
| 🟡 | [`L04`](L04-analyzer-trap/brief.md) | lab | Stop the tokenizer shredding your identifiers | 25m | `L03` |

## T3 · Ranking & Packing

**Development** — hands on an implementation with a measurement attached.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟡 | [`C04`](C04-fusion-normalisation/brief.md) | fix | Weighted fusion is quietly favouring one leg | 10m | — |
| 🟢 | [`L05`](L05-rank-fusion/brief.md) | lab | Fuse two rankings without comparing their scores | 20m | `L03` |
| 🟡 | [`L06`](L06-pack-to-budget/brief.md) | lab | Pack a prompt to a hard token budget | 25m | `L05` |

## T4 · Measurement

**Testing** — hands on an eval set and the noise band that makes it interpretable.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟢 | [`C05`](C05-which-stage/brief.md) | predict | Which stage is the bottleneck? | 5m | — |
| 🟢 | [`L07`](L07-two-recalls/brief.md) | lab | The two recalls, and the gap between them | 20m | `L06` |
| 🟡 | [`L08`](L08-paired-bootstrap/brief.md) | lab | Decide whether a delta is real | 30m | `L07` |

## T5 · Judgement

**Quality** — hands on a quality gate somebody else can run without you.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟢 | [`C06`](C06-expected-agreement/brief.md) | implement | Compute the agreement you would get for free | 8m | — |
| 🟡 | [`L09`](L09-cohens-kappa/brief.md) | lab | Find out your judge agrees with you by accident | 25m | `L08` |

## T6 · Economics

**Viability** — hands on a cost model whose inputs are named.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟢 | [`C07`](C07-recurring-or-one-off/brief.md) | fill | Which of these bills comes back every month? | 8m | — |
| 🟡 | [`L10`](L10-cost-and-cache/brief.md) | lab | Price the 69% of the bill that is not generation | 25m | `L06` |

## T7 · Agents & Traces

**Operations** — hands on a trace that makes a failure reproducible after the fact.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| 🟡 | [`C08`](C08-budget-guard/brief.md) | fix | The agent takes one step past its budget | 10m | — |
| 🔴 | [`L11`](L11-replayable-trace/brief.md) | lab | Make a failure reproducible after the fact | 35m | `L07`, `L06` |

## T8 · Shipping

**Release** — hands on a decision record: ship, do not ship, or not yet measurable.

| | Item | Format | | Time | After |
|---|---|---|---|---:|---|
| ⚫ | [`L12`](L12-release-gate/brief.md) | lab | Decide whether it ships | 50m | `L08`, `L09`, `L10`, `L11` |

---

20 labs · 374 minutes of work · every reference solution is tested against its own checks in CI.
