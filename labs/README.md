# L.A.B. simulator

**L**ook · **A**ttribute · **B**uild — one loop, twelve labs, eight tracks.

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

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🟢 | [`L01`](L01-stable-chunk-ids/brief.md) | Give a chunk an id that survives an edit | 15m | — |
| 🟡 | [`L02`](L02-heading-path/brief.md) | Carry the heading path into every chunk | 25m | `L01` |

## T2 · Indexing & Retrieval

**Design** — hands on an ADR: the retrieval design, and the alternative that lost.

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🟢 | [`L03`](L03-idf-by-hand/brief.md) | Compute BM25's IDF, and find where it goes negative | 15m | — |
| 🟡 | [`L04`](L04-analyzer-trap/brief.md) | Stop the tokenizer shredding your identifiers | 25m | `L03` |

## T3 · Ranking & Packing

**Development** — hands on an implementation with a measurement attached.

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🟢 | [`L05`](L05-rank-fusion/brief.md) | Fuse two rankings without comparing their scores | 20m | `L03` |
| 🟡 | [`L06`](L06-pack-to-budget/brief.md) | Pack a prompt to a hard token budget | 25m | `L05` |

## T4 · Measurement

**Testing** — hands on an eval set and the noise band that makes it interpretable.

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🟢 | [`L07`](L07-two-recalls/brief.md) | The two recalls, and the gap between them | 20m | `L06` |
| 🟡 | [`L08`](L08-paired-bootstrap/brief.md) | Decide whether a delta is real | 30m | `L07` |

## T5 · Judgement

**Quality** — hands on a quality gate somebody else can run without you.

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🟡 | [`L09`](L09-cohens-kappa/brief.md) | Find out your judge agrees with you by accident | 25m | `L08` |

## T6 · Economics

**Viability** — hands on a cost model whose inputs are named.

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🟡 | [`L10`](L10-cost-and-cache/brief.md) | Price the 69% of the bill that is not generation | 25m | `L06` |

## T7 · Agents & Traces

**Operations** — hands on a trace that makes a failure reproducible after the fact.

| | Lab | | Time | After |
|---|---|---|---:|---|
| 🔴 | [`L11`](L11-replayable-trace/brief.md) | Make a failure reproducible after the fact | 35m | `L07`, `L06` |

## T8 · Shipping

**Release** — hands on a decision record: ship, do not ship, or not yet measurable.

| | Lab | | Time | After |
|---|---|---|---:|---|
| ⚫ | [`L12`](L12-release-gate/brief.md) | Decide whether it ships | 50m | `L08`, `L09`, `L10`, `L11` |

---

12 labs · 310 minutes of work · every reference solution is tested against its own checks in CI.
