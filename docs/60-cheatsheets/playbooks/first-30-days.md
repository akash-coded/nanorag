# 📅 First 30 days on a RAG engagement

> **When:** you have just been handed a client, a corpus, and a promise someone else made.

The single most common failure is spending week one improving retrieval. **You cannot improve
what you cannot measure**, and on day one you cannot measure anything.

## Week 1 — Refuse to tune anything

| Day | Do |
|---|---|
| 1–2 | **Read 50 documents and 50 real queries.** Not summaries. The actual text. Nothing else this week matters more |
| 2 | Ask the four cost inputs: corpus size, **change rate**, query volume, encoder dimension |
| 3 | Ask the permission question: *can a user know a document exists but not read it?* It decides the architecture |
| 3–4 | Establish whether a **trace** exists. If not, that is finding #1 and you say so immediately |
| 5 | Write down what "better" would mean, in a number, and get someone to disagree with it |

**Deliverable:** a one-page memo saying what you can and cannot currently measure. Not a plan.

**The trap:** they will ask for a quick win. The honest answer is *"I can give you one, and
neither of us will be able to tell whether it worked."*

## Week 2 — Build the instrument

| | |
|---|---|
| **Eval set** | 150–200 questions minimum. Include **null questions** at their real base rate — without them you cannot measure abstention at all |
| **Gold evidence** | Per question, not just answers. Answer-only scoring cannot distinguish [right by accident](../frameworks/four-verdicts.md) |
| **Frozen slice** | Agreed in writing, held back, **never** iterated against |
| **The noise band** | Bootstrap the *unchanged* system. This number is what makes every later delta interpretable |

**Deliverable:** a baseline with intervals. The first defensible number of the engagement.

**The trap:** they will want the eval set to be big. It is more useful for it to be *representative
and honestly labelled* — and 200 good questions beat 2,000 generated ones.

## Week 3 — Attribute, then choose

- Run [The Four Verdicts](../frameworks/four-verdicts.md) over 50 failures.
- Apply [The Precondition Test](../frameworks/precondition-test.md) to every technique someone has
  already suggested. Most will fail it.
- Rank candidate work by **expected movement ÷ cost**, using the distribution — not by what is
  interesting.

**Deliverable:** a ranked list of three things, each with the number it should move and by how
much to be worth doing.

**The trap:** the distribution will usually say the bottleneck is dull — chunking, an analyzer,
`k`. Say so anyway.

## Week 4 — Ship one thing, with the gate

- Implement the top item **only**.
- Measure with a paired bootstrap on the frozen slice.
- **Put the gate in CI now**, while you are the person who cares about it, not later.
- Write the decision record: what you chose, what lost, what would change your mind.

**Deliverable:** one shipped change with an interval, and a gate that will block the next
regression without you.

## What you have at day 30

Not a better system, necessarily. **A system whose quality is now a number**, a gate that
protects it, and a ranked list of what to do next — which is worth more than four weeks of
untracked tuning and is the thing that gets the contract extended.

## The sentence for the week-one steering call

> *"I am not going to change retrieval this month until we can both see the number it moves.
> Otherwise we will disagree in March about whether it worked, and neither of us will have
> evidence."*
