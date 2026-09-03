# C06 · Compute the agreement you would get for free

🟢 **Easy** · 8 min · **implement** · from notebook 06 §6.3 · unlocks L09

## Look

Your judge says "correct" 90.5% of the time. You say "correct" 89.5% of the time. You agree on
94% of items.

How much of that 94% was available with **no model at all** — a judge that says "correct" to
everything, or flips a weighted coin?

## Attribute

Under independence, two raters agree on an item when they both say yes **or** both say no:

```text
p_e = P(both yes) + P(both no) = h·j + (1−h)·(1−j)
```

That is the floor. κ is `(p_o − p_e) / (1 − p_e)`: the share of the *remaining* agreement you
actually earned.

## Build

Implement `expected_agreement(h, j)` in `starter.py`. Two lines.

```bash
python scripts/lab.py run C06
```

## Debrief

`0.905 × 0.895 + 0.095 × 0.105 ≈ 0.82`. Of the 94% raw agreement, 82 points were chance. The
judge earned 12 points out of an available 18 — κ ≈ 0.67. Push the split to 95/5 and the same 94%
raw agreement is κ ≈ 0.37. **Never quote agreement without the base rate beside it.**
