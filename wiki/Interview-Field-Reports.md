# Interview field reports

What people were **actually asked**, and how it went. Anonymised, community-contributed, and more
useful than any list of predicted questions — because the gap between what a company says it tests
and what it tests is where preparation goes wrong.

This page lives in the wiki rather than in `docs/` deliberately: it should be editable by whoever
just came out of a loop, without a pull request and without review.

---

## What to include

**Do include:** the round shapes, the kind of questions, what surprised you, what you wish you had
prepared, and the follow-up that caught you out.

**Do not include:** the company's name if you signed anything saying not to, verbatim take-home
prompts, or anything you were told was confidential. **A round shape is not a leak; a verbatim
problem statement usually is.**

Use the shape below. Keep it honest about what went badly — a report where everything went well
teaches nobody.

```markdown
### YYYY-MM · Role shape · outcome

**Rounds:** screen → technical depth → system design → behavioural

**What they actually probed:**
- ...

**The follow-up I did not have ready:**
> "..."

**What I would prepare differently:**
- ...
```

---

## Reports

### 2026-08 · Forward-deployed / deployment engineer · offer

**Rounds:** screen → case study (take-home, 4h) → system design → behavioural

**What they actually probed:** almost nothing about model internals. The case study handed over a
messy corpus and a vague goal, and the scoring was **whether you built an eval set before you built
anything else.** Two of the three people I compared notes with went straight to improving retrieval
and did not pass.

**The follow-up I did not have ready:**

> *"How many questions would your eval set need to detect the improvement you are claiming?"*

I said "a few hundred" and could not defend it. The
[power arithmetic](https://github.com/akash-coded/nanorag/blob/main/docs/30-learning/interview-prep/01-mathematical-foundations/paired-bootstrap-and-power.md)
takes ten minutes to learn.

**What I would prepare differently:** rehearse saying *"week one is the eval set"* out loud. It
feels like stalling when you say it and it is the highest-scoring sentence in that round.

---

### 2026-07 · ML engineer, search team · rejected at system design

**Rounds:** screen → coding → system design → hiring manager

**What they actually probed:** the coding round was ordinary. The design round was **entirely about
what breaks at scale**, and I had prepared architecture rather than failure modes.

**The follow-up I did not have ready:**

> *"You said you would filter by permission. Where does that filter run?"*

I said "after retrieval" and watched the interviewer's face change. Post-filtering collapses `k`
unpredictably **and** leaks — the result count is a function of content the user cannot see. It is
in [The Inference Channel Audit](https://github.com/akash-coded/nanorag/blob/main/docs/60-cheatsheets/frameworks/inference-channel-audit.md)
and I had not read it.

**What I would prepare differently:** for every component, know **the failure mode**, not just what
it does. They ask about failure.

---

### 2026-06 · Applied research · offer, declined

**Rounds:** paper discussion → experiment design → coding → team fit

**What they actually probed:** the paper round was not "do you know this paper". It was *"design
the experiment that would show they are wrong."* Falsification, not comprehension.

**The follow-up I did not have ready:**

> *"What result would make you believe them?"*

A critique you cannot satisfy is not a critique, and I had only prepared attacks.

**What I would prepare differently:** for any technique, be able to state its **precondition** —
what failure it fixes — and how you would check whether you have that failure. That single habit
answered about half of this loop. It is [The Precondition
Test](https://github.com/akash-coded/nanorag/blob/main/docs/60-cheatsheets/frameworks/precondition-test.md).

---

## Patterns across reports so far

Three, from a small sample — treat as hypotheses, not findings:

1. **The eval set is the differentiator in FDE-shaped loops.** Candidates who tune before measuring
   do not pass, and they usually do not know why.
2. **Design rounds ask about failure, not architecture.** Preparing a clean diagram prepares you for
   the wrong twenty minutes.
3. **The second follow-up is where it is decided.** Everyone survives the first. Level 3 and 4 of
   [the question decoder](https://github.com/akash-coded/nanorag/blob/main/docs/60-cheatsheets/interviews/question-decoder.md)
   is where offers separate.

**Add yours.** Three reports is an anecdote; thirty is a signal.
