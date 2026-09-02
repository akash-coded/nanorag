# C03 · Predict the sign of IDF for a common term

🟢 **Easy** · 5 min · **predict** · from notebook 04 §4.2 · unlocks L03

## Look

A 1,000-document corpus. The term `service` appears in **620** of them.

```text
IDF(t) = log( (N - df + 0.5) / (df + 0.5) )
```

## Attribute

Do not compute it. Read the fraction: documents *without* the term over documents *with* it.
When more than half the collection has the term, which way does that ratio fall relative to 1,
and what does `log` do to a number on that side of 1?

## Build

Set `ANSWER` in `starter.py` to `"positive"`, `"negative"`, or `"zero"`.

```bash
python scripts/lab.py run C03
```

In a discussion, just post the word.

## Debrief

Negative, and it is the design: a term in most documents is evidence *against* this one being
special. That is the principled stop list — no word list to maintain, and it adapts per corpus.
The sign flips at `df ≈ N/2`; L03 makes you find the exact pivot.
