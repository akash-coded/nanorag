# C05 · Which stage is the bottleneck?

🟢 **Easy** · 5 min · **predict** · from notebook 01 §1.3 · unlocks L07

## Look

```text
                          N=100     N=400
Recall@N                  0.938     0.974      candidate pool
full_chain_recall@N       0.871     0.902      pool, all hops
full_chain_recall         0.469     0.481      packed context, k=8
```

Widening the pool moved the top two rows and barely touched the third.

## Attribute

Three stages: **retrieval** fills the pool, **packing** picks `k` from it, **generation** reads
what was packed. Each row is measured at one of those stages. Where is the largest drop between
adjacent rows, and which stage sits between them?

## Build

Set `ANSWER` in `starter.py` to `"retrieval"`, `"packing"`, or `"generation"`.

```bash
python scripts/lab.py run C05
```

## Debrief

Packing: the pool had every hop for 87% of questions and only 47% survived into `k=8`. Adding
300 candidates cannot create a ninth slot. On this corpus the count was **84 found-then-dropped
against 27 never-retrieved** — the bottleneck was three-to-one on the stage nobody was working
on. L07 makes you compute those two numbers.
