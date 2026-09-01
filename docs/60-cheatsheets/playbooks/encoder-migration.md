# 🔄 Encoder migration playbook

> **When:** swapping the embedding model without taking retrieval down.

The failure mode that defines this job: **a mixed-encoder index throws no exception.** Cosine
returns well-formed numbers for vectors that mean nothing to each other. Nothing errors, results
stay plausible, and quality quietly falls.

## The invariant

> **One index version has exactly one `embedder_tag`. Always. No exceptions, including "just this
> one document".**

Everything below exists to protect that sentence.

## The sequence

**1 · Prove the new encoder is better — before touching production.**

- [ ] Build `v_{n+1}` **alongside** `v_n`. Never into it
- [ ] Evaluate on the frozen slice, paired bootstrap
- [ ] **Slice by query class.** An encoder swap almost always helps some classes and hurts
      others; the aggregate hides it and the aggregate is what people quote
- [ ] Compare cost: dimension drives storage and RAM, and RAM is on the serving path

**2 · Shadow.**

- [ ] Serve from `v_n`, evaluate `v_{n+1}` on live traffic
- [ ] Compare on the **query distribution you actually have**, which is not your eval set

**3 · Swap.**

- [ ] Atomic **alias** swap. Not a rebuild, not a config deploy
- [ ] `mixed_version_check()` on the new version *before* the alias moves
- [ ] Rollback is the same swap in reverse — seconds

**4 · After.**

- [ ] Keep `v_n` warm for at least one full incident cycle
- [ ] **Invalidate every cache keyed on embeddings** — a semantic cache keyed on old vectors will
      serve confidently wrong hits
- [ ] Re-tune `α` if you fuse. A stronger dense leg moves the optimum, usually a lot; the old `α`
      is fitted to the old encoder

## What people forget, in order of how much it hurts

| Forgotten | Consequence |
|---|---|
| **Re-tune `α`** | The new encoder is better and the fusion weight still assumes it is weak |
| **Cache invalidation** | Confident wrong answers from vectors that no longer mean anything |
| **Per-class evaluation** | Aggregate improved, your most important class regressed |
| **Dimension change** | RAM and index size move; capacity planning was done for the old one |
| **Backfill cost** | Budgeted as a one-off, then incurred again at the next upgrade |
| **Downstream thresholds** | Abstention and cache thresholds were fitted to the old score distribution |

That last one is subtle: **score distributions are not comparable across encoders.** Every
threshold anywhere in the system that was tuned against cosine values has to be re-fitted.

## The check that catches the disaster

```python
report = index.mixed_version_check(version)
assert report["distinct_embedder_tags"] == 1, report
```

Run it in CI, and run it before every alias swap. It is the only thing standing between you and
a failure that produces no error.

## When to refuse the migration

- The new encoder wins on aggregate and **loses on your highest-value class**
- The re-embed cost exceeds the measured quality gain for a year
- You have **no rollback path** — no version aliasing, so a swap is a rebuild

The third is a reason to build aliasing first and migrate second.

---

**Practise:** [EX-09 — Survive an encoder upgrade](../../30-learning/exercises/ex-09-survive-an-encoder-upgrade.md) ·
**Decision:** [ADR-0004](../../20-decisions/0004-stable-chunk-ids.md)
