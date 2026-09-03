# C07 · Which of these bills comes back every month?

🟢 **Easy** · 8 min · **fill in the blanks** · from notebook 07 §7.1 · unlocks L10

## Look

Six line items on a RAG deployment's bill. The per-query token cost is the one everybody quotes.
It is about a third.

## Attribute

Each item is either **recurring** — it scales with traffic or time and you pay it every month —
or **one-off** — it happens when you build or rebuild. Mixing them into one per-query figure is
how "about a cent a query" turns into a bad conversation in month three.

The one people get wrong: *re-embedding on drift*. It feels like a rebuild. It is a **recurring**
bill, because the corpus keeps changing.

## Build

`starter.py` has six blanks, each `"recurring"` or `"one-off"`. Fill them.

```bash
python scripts/lab.py run C07
```

## Debrief

Four recurring, two one-off. The recurring set is the *bill*; the one-off set is a *decision*
you make when you upgrade the encoder. L10 turns this classification into a model with numbers.
