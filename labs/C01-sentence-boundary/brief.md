# C01 · Fill the sentence-boundary rule

🟢 **Easy** · 8 min · **fill in the blanks** · from notebook 03 §3.3 · unlocks L01

## Look

A chunker that splits on `.` produces this from one sentence of an incident report:

```text
"Rolled back to v2"   "1"   "4 after Dr"   " Patel signed off"
```

Four chunks, none retrievable, from *"Rolled back to v2.1.4 after Dr. Patel signed off."*

## Attribute

A sentence boundary is not a character. It is a **pattern**: a terminator, then whitespace,
then something that starts a sentence. `v2.1.4` has terminators but no whitespace after them.
`Dr.` has whitespace but is followed by a capital that continues the name — that one is a
genuine limitation of this rule, and the debrief says so.

## Build

`starter.py` has three blanks written as `____`. Fill them so the checks pass. Do not restructure
the function — the point is the *rule*, and it fits in one regular expression.

```bash
python scripts/lab.py run C01
```

## Debrief

The rule you wrote still splits *"Dr. Patel"*, because "Dr." is a terminator followed by
whitespace and a capital. Fixing that needs an abbreviation list, which is corpus-specific — a
medical corpus has hundreds. **This is the first precondition test you have run without noticing:
is the failure you are fixing actually in your corpus?** Count the abbreviations before you
build the list.
