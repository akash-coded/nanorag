# 🗺️ Navigating the loop

> **When:** the day before. What each round is actually scoring.

Companies weight these differently, but the rounds themselves are recognisable across most
retrieval and applied-ML loops.

## The rounds

| Round | What it looks like | What is being scored | The way people lose it |
|---|---|---|---|
| **Screen** | "Walk me through a project" | Can you describe your own work at the right altitude? | Narrating the architecture instead of the decision. They want the fork in the road |
| **Technical depth** | "Why does X work?" | Do you know the mechanism or the name? | Reciting the name of the technique confidently. Every follow-up goes one level down until you stop |
| **System design** | "Design retrieval for…" | Do you find the constraint that makes it hard? | Designing the finished system and never saying what week one is |
| **Case / take-home** | Data and a vague goal | Do you measure before you tune? | Shipping a model. They wanted an eval set |
| **Behavioural** | "Tell me about a disagreement" | Do you change your mind on evidence? | Stories where you were right the whole time |

## The three things scored in every round

**1 · Do you reach for evidence or intuition?**
*"I'd check the trace"* beats *"I'd look at whether the right documents came back."* The first is
a procedure, the second is a wish.

**2 · Do you know what you cannot see?**
Naming a missing trace, a missing eval set, or a missing label as a **finding** — rather than as a
blocker — is the single clearest seniority signal available to you.

**3 · Have you actually done it?**
One concrete failure you lived through beats any amount of taxonomy. *"A team I worked with spent
a month on the encoder for a problem that was `k=5`"* does more work than a correct list.

## The first five minutes of a design round are scored

Most candidates start designing. The clarifying questions are the round.

Ask, in this order:

1. **What is the constraint that makes this hard?** — cost, latency, permissions, freshness,
   residency. There is always one; find it before you draw anything
2. **How would we know it works?** — if they have no answer, that *is* the first deliverable
3. **What is the cost of a wrong answer versus a refusal?** — decides abstention, and almost
   nobody asks

## Two sentences that reliably score

> *"Before I design this — can a user know a document exists but not read it? That changes the
> architecture, not just a detail of it."*

And:

> *"Week one is not any of this. Week one is an eval set and a test that fails when we break it,
> because otherwise we cannot tell in March whether March was better."*

## Managing the 45 minutes

| Minutes | Do |
|---|---|
| 0–5 | Clarify. Write the constraint on the board. **Do not start designing** |
| 5–20 | Design out loud. Say the alternative you rejected and why |
| 20–35 | They will pressure one weak point. **They have already chosen it** — it is usually the thing you glossed |
| 35–42 | "What would you do first?" Answer with week one, not the architecture |
| 42–45 | Your questions. Ask one real one |

## When you do not know

Say so, then say what you would do. *"I don't know how HNSW handles deletes specifically. I'd
expect a tombstone-and-compact scheme because rebuilding the graph per delete is too expensive,
and I'd verify that before designing around it."*

**That scores better than a confident wrong answer, and better than "I don't know" alone.** The
reasoning is the thing being measured.
