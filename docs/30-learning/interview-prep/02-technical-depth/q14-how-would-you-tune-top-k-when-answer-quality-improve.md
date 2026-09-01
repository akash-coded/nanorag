# Q14 · How would you tune top-k when answer quality improves but latency and cost rise?

I would ask what the latency and cost envelope is before answering, because k is a purchase
and I need to know the budget.

Then I would produce the curve: sweep k, and report marginal full-chain recall per thousand
additional tokens. That number falls off a cliff at some point, and the cliff is the operating
point — not a round number somebody liked. I would present it as a frontier with the chosen
point marked, so the client can see what a different choice would buy them.

Two things worth naming: context precision falls monotonically as k rises, so every extra slot
is more likely to hold a distractor than a gold chunk; and generation dominates the latency
budget anyway, so cutting retrieval quality to save 200 ms of a 2.5 s p95 is usually the wrong
trade.
