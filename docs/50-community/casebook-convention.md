# The casebook convention

Some discussion threads in this repository are **casebook threads**: reconstructed
conversations written for teaching, published by the maintainer, with illustrative roles.
This document exists so nobody has to guess which ones.

## Why they exist

The most useful thing a technical discussion can show is not the right answer. It is the
route to it: the plausible wrong turn, the correction that came with a measurement, and the
moment someone changed their mind. A repository that has only correct answers teaches half
the subject.

A new repository has no such conversations, because it has no participants yet. Rather than
wait, the maintainer writes them — openly labelled, so the reader knows exactly what they
are reading.

## The rules

1. **Every casebook thread is labelled.** The first line of the opening post carries the
   banner, and the thread carries the [`casebook`](https://github.com/akash-coded/nanorag/labels/casebook) label.
2. **Every number is real.** A casebook comment may not contain a figure that cannot be
   reproduced by running a named cell in this repository. Roles are illustrative; results
   are not. This is the line between a teaching transcript and fiction, and it is not
   negotiable.
3. **The wrong answers are ones people actually give.** Not strawmen. Most are drawn from
   the issue tracker — [#4](https://github.com/akash-coded/nanorag/issues/4) and
   [#7](https://github.com/akash-coded/nanorag/issues/7) both began as confident,
   reasonable, wrong hypotheses.
4. **Disagreement resolves on evidence, never on authority.** The maintainer does not win an
   argument by being the maintainer. If a thread ends with someone deferring rather than
   measuring, it is a bad thread.
5. **Not every thread resolves.** Some end unresolved and linked to an open issue, because
   that is what a real tracker looks like.

## The three tiers

| Tier | What it is | Where |
|---|---|---|
| **A · Casebook** | Written by the maintainer, roles illustrative, banner and label present | Q&A, Design Reviews, Interview Prep, Show and Tell |
| **B · Live** | Genuinely open. Real questions from real people, answered as they arrive | Exercise Clinic, Errata, Office Hours |
| **C · Curated** | A live thread that turned out well — re-titled, summarised, answer marked, linked from the docs | Anywhere |

Over time the centre of gravity moves from A to C. That is the intent.

## The roles

The same voices recur, so their perspective is predictable:

| Role | Perspective |
|---|---|
| **Priya** | Sharp on method. Asks whether the reasoning is sound, not whether the code runs |
| **Marcus** | Reaches for the plausible textbook answer first. Frequently wrong, always in an instructive way |
| **Dana** | Owns the eval harness. Arrives with numbers and an interval |
| **Rafael** | Search infrastructure background. Thinks about what breaks at scale |
| **Noor** | Regulated industry. Asks about permissions, audit and retention before anything else |

## What this is not

It is not a substitute for real participation, and it does not pretend to be. There are no
additional accounts: every casebook comment is published by the repository owner, which is
visible on every comment. If you want to disagree with one, the reply box works normally —
that is the point.
