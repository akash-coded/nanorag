# C04 · Weighted fusion is quietly favouring one leg

🟡 **Medium** · 10 min · **fix the code** · from notebook 04 §4.9 · unlocks L05

## Look

Two legs, scores already "normalised", then fused at α=0.5:

```text
                 raw          after _normalise      fused
dense  doc-A     0.81         1.00
dense  doc-B     0.74         0.91
lex    doc-A    18.4          1.00
lex    doc-B     8.8          0.48   <- 8.8 is nowhere near the bottom of this leg
```

The lexical leg's lowest score in the pool was 8.8. After normalisation it reads 0.48, as if it
were halfway up. Something is off, and it is one token.

## Attribute

Min-max normalisation maps the leg's minimum to 0 and maximum to 1. That needs the **range** in
the denominator. Divide by the maximum alone and you have only rescaled — a leg whose scores sit
between 8 and 18 never gets near 0, and it silently outvotes a leg that does.

## Build

`starter.py` has one wrong expression. Fix it.

```bash
python scripts/lab.py run C04
```

## Debrief

This is why RRF exists. Any score-based fusion needs each leg on a comparable scale, and the
moment you write a normaliser you own its edge cases — flat legs, negative scores, a leg with one
candidate. RRF consumes ranks and has none of them. On this corpus weighted fusion still won,
but only after somebody found exactly this bug.
