# Q15 · How do you detect and mitigate "lost in the middle"?


Detect by measuring it on your own eval set rather than citing the paper: hold the evidence set
constant and force the gold chunk into position 1, the middle, and last. The spread is your
position sensitivity. It varies by model and by task, so somebody else's U-curve is a
hypothesis, not your number.

Mitigate in order of cost. Keep k small — fewer chunks in the middle at all, and it saves money
too. Order by reranker score then interleave, putting the two highest-scoring chunks at the
head and the tail. Restate the question briefly after the evidence, which puts the task in the
strong end position for about fifteen tokens.
