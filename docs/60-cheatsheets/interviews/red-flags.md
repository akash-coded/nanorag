# 🚩 Red flags you emit without noticing

> **When:** rehearsing. The sentences that cost you the round.

Each of these is something a competent person says while meaning something reasonable. The
problem is what it sounds like from the other side of the table.

## About measurement

| You say | They hear | Say instead |
|---|---|---|
| "It improved by 3%" | You do not know what an interval is | "+3 points, 95% CI +1.2 to +4.9, on 400 questions" |
| "It works well" | You have not measured it | "On our eval set it scores X; here is what that set does not cover" |
| "Accuracy is 92%" | You do not know the base rate | "92%, against an ungrounded floor of 61%" |
| "The model is very accurate" | You have not separated retrieval from generation | Which of the four verdicts, and their proportions |
| "We A/B tested it" | Possibly nothing | Sample size, duration, and what the metric's variance was |

## About design

| You say | They hear | Say instead |
|---|---|---|
| "We use a vector database" | You chose a category, not a design | The filter and residency requirements that decided it |
| "We chunk at 512 tokens" | You copied a default | "We bake off; on this corpus structural at ~400 won by X" |
| "We use RAG" | You have not thought about the alternative | What retrieval buys here that a longer context would not |
| "We added a reranker" | You may have added an identity function | What the reranker sees that the first stage did not |
| "We'll fine-tune the embeddings" | You are reaching for the expensive option first | What you measured that says the base encoder is the bottleneck |
| "We filter results by permission" | **Post-filtering.** A leak and a `k` collapse | "We pre-filter inside the query" |

## About judgement

| You say | They hear | Say instead |
|---|---|---|
| "The client wanted X so we built X" | You do not push back | "They asked for X; I showed them Y was the actual constraint" |
| "It's a hard problem" | You are avoiding the question | Name the specific hard part |
| "We didn't have time to evaluate" | You will do this to them too | "We shipped without a gate and here is what that cost us" |
| "That was before I joined" | You do not own the system | What you would change now, and why it has not been changed |
| "I'd need to look that up" *(and stop)* | You have no model | Look it up **out loud**: what you'd expect, and why |

## The subtle ones

**Being right in every story.** A behavioural round asking about disagreement wants to hear you
change your mind on evidence. A candidate who was right every time has either not worked with
good people or is not telling you the truth.

**Fluency without a number.** The most dangerous failure mode for a strong communicator: a
beautifully argued answer with nothing measurable in it. Interviewers who have been burned listen
specifically for this.

**Naming techniques as a substitute for mechanisms.** "We'd use HyDE, maybe ColBERT, possibly
RAPTOR" sounds like breadth and reads as a reading list. One technique with its precondition
stated beats five names.

**Never saying "I don't know."** It reads as either dishonesty or lack of self-awareness, and
both are worse than the gap.

## The single strongest move available to you

**Volunteer a limitation before you are asked.**

> *"What this does not give me is distributional realism — my corpus is synthetic, so the absolute
> numbers will move on real data. What transfers is the harness, not the constants."*

You have demonstrated the thing they are screening for: **knowing which parts of your own result
generalise.** A candidate who defends their numbers as universally valid is a risk. One who says
"the method transfers, the constants do not" is describing how they will behave on the client's
data — which is the only thing the interview is really about.
