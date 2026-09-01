# Q5 · Agentic search costs $0.90 on hard questions. Finance wants $0.15. What do you change, and what do you refuse to change?


**Testing:** whether you can decompose a per-query cost from memory; whether you optimise the
distribution or the worst case; whether you push back with a quantified consequence.

**Answer.**

First, I would not accept the framing. $0.90 is a worst case, and Finance is almost certainly
looking at a blended bill.

**Get the distribution before redesigning anything.** If 8% of queries are hard and the rest
cost $0.02, the blended number is about $0.09 and we are already under target — the whole
exercise was about a number nobody had computed. I have seen that outcome more than once. If
30% are hard, we have a real problem and I want to know that before I start.

Assuming it is real, the levers in order, with what each costs:

**Escalate rather than loop by default.** Run single-shot, and enter the loop only when a
sufficiency check on the first pass fails. Most traffic never pays the multiplier. This alone
usually removes most of it, and it costs nothing in quality because the escalation trigger is
the same check the loop uses internally.

**Cache the stable prefix and the tool schemas.** Fifteen to thirty percent of input spend,
for a prompt-ordering change. Free.

**Carry a compacted evidence summary between turns** instead of the full text of everything
found so far. This turns the loop's token growth from roughly quadratic to roughly linear.
Small risk of dropping a detail — summarise, do not truncate.

**Cap turns**, typically four to eight. This bounds the tail, which is what actually hurts:
the p95 is where an agentic bill lives, not the median.

**Use a small model for decomposition and the sufficiency check**, and the large one only for
synthesis. Thirty to sixty percent of the loop's overhead. The cost is a router you must also
evaluate — a second system with its own failure modes.

**What I refuse:** removing the grounding and abstention checks, and removing the trace. Both
are cheap. Both are what stop a wrong answer becoming an incident, and the trace is the only
reason we can have this conversation with numbers at all.

**Then quantify the residual rather than agreeing to the target.** "I can reach $0.22 blended
without any quality loss. Getting to $0.15 means capping at two turns, which costs roughly X
points of full-chain recall on multi-hop questions — here is the measurement. That is a
business decision and I am happy to make either call, but I want it made with the number
visible."

**Red flags:** agreeing to $0.15 without a plan; "we'll use a cheaper model" as the whole
answer; naming no quality cost for any lever.

> **Run it:** [notebook 07 §7.6](../../../../notebooks/07_cost_and_token_optimization.ipynb) computes
> the blended cost under different hard-traffic shares;
> [notebook 08 §8.4](../../../../notebooks/08_agentic_search_and_evaluation.ipynb) measures the
> escalation policy against always-loop.

---
