# Q6 · Your LLM judge says quality went up. How would you know if the judge is wrong?


**Testing:** whether you treat the evaluator as a component that can regress; whether you know
agreement statistics rather than accuracy; whether you can name specific biases and controls.

**Answer.**

I would treat the judge exactly like the retriever: a component with a version, a test set,
and a way to regress.

**A held-out human-labelled calibration set**, re-scored on every judge, rubric or model
change. Track Cohen's κ over time as a metric in its own right, not raw agreement — on a skewed
set a judge that always says "pass" scores 90% accuracy and has learned nothing. κ corrects for
chance and that difference is the whole point.

**Compare judge–human agreement against human–human agreement.** This is the step people skip
and it changes the interpretation completely. If two trained humans following the same rubric
only agree 70% of the time, a judge at 72% is doing fine and the *rubric* is the problem — it
is ambiguous, and fixing the judge will not help. You cannot know that without running the
human pass, and it costs about a day.

**Adversarial probes.** Feed known-bad answers that are long, fluent and confidently wrong. A
judge that passes them has verbosity bias, not quality signal. Same for position: in pairwise
comparison, swap A and B and require the verdict to hold. And self-preference — a judge tends
to favour output from its own model family, so I use a different family from the generator
where I can, and note it in the report where I cannot.

**Cross-check with an independent production signal.** If judged quality rises while citation
click-through, escalation rate and thumbs-down do not move at all, I believe the production
signal. A quality improvement that no user experiences is a measurement artefact until proven
otherwise.

**Version everything** — judge model, temperature, rubric text, few-shot examples. An
unexplained score jump with no system change is judge drift until proven otherwise, and
without versioning you cannot even tell whether something changed.

One more thing I would say unprompted: I use the judge for *relative* comparisons between two
versions of the system. Its absolute score is a dashboard number, not a client-facing quality
claim, and I would push back on anyone who wanted to put it in a contract.

**Red flags:** "we'd spot-check some outputs"; raw agreement on a skewed set; same model family
as generator and judge with no note about it.

> **Run it:** [notebook 06 §6.3](../../../../notebooks/06_evaluation_approaches.ipynb) computes κ, runs
> the verbosity and position probes, and demonstrates judge drift from a single rubric
> parameter.

---
