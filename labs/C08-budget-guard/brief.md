# C08 · The agent takes one step past its budget

🟡 **Medium** · 10 min · **fix the code** · from notebook 08 §8.3 · unlocks L11

## Look

```text
budget: 300 tokens
step 1  spent 120   total 120   continue
step 2  spent 110   total 230   continue
step 3  spent 130   total 360   stop: "budget"
```

The trace says it stopped on budget. It stopped **60 tokens over** it. Finance will notice
before you do.

## Attribute

A budget guard has to answer one question: *can I afford the next step?* — and it has to answer
it **before** taking the step. This loop checks after, with a comparison that only fires once the
line has already been crossed. Two small things, same failure.

## Build

Fix `run_loop` so it never spends past `budget`, and the trace still names the reason it stopped.

```bash
python scripts/lab.py run C08
```

## Debrief

The subtle half: the loop cannot know the *next* step's exact cost, so the guard is *"is there
enough left for a step of the size I expect?"* — an estimate, which is why `est_step` is an
argument. A guard with no estimate either overspends or stops one step early every time. Either
is defensible; **silently overspending while reporting "stopped on budget" is not.**
