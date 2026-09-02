# C02 · The tokenizer has a bug. Find it

🟢 **Easy** · 10 min · **fix the code** · from notebook 04 §4.3 · unlocks L04

## Look

```text
query: ERR_CONN_RESET
matches: 1,842 of 1,842 incident reports
```

Every document matched. Nothing errored. The scoring function is correct.

## Attribute

The analyzer is splitting `ERR_CONN_RESET` into three terms that every incident report contains.
After that, IDF for all three is near zero and the query ranks nothing. **The bug is one
character in a character class.** Find it by reading, not by running — then run to confirm.

## Build

`starter.py` is complete and wrong. Change as little as you can.

```bash
python scripts/lab.py run C02
```

## Debrief

You removed `_` from the split set. Now ask the question the fix does not answer: **what else is
in that class that should not be?** `-` splits `post-mortem`. `/` splits `docs/adr`. And `.` —
which you may be tempted to add to the keep-set — would stop sentence-ending periods separating
tokens across the *entire* corpus to rescue 208 chunks with version strings. That trade is
[EX-12](../../docs/30-learning/exercises/ex-12-the-analyzer-audit.md), and someone measured it as
a regression.
