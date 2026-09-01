# Q3 · You upgraded the embedding model and Evidence Recall@10 fell from 0.86 to 0.71. Walk me through the diagnosis.


**Testing:** whether you check operational causes before model-quality causes; whether you
bisect rather than guess.

**Answer.**

A 15-point drop is almost never "the new model is worse." That is the seventh thing I check,
not the first. In order:

**1 · Mixed-version index.** Are some vectors still from the old model? One SQL query against
the model-version tag stored on each row. This is first because it is the cheapest check and
by far the most common cause — a partial re-ingest that failed halfway, or a backfill that ran
against a stale queue. Vectors from two encoders are not comparable and cosine similarity will
return perfectly well-formed numbers for the comparison, so nothing else in the system will
tell you.

**2 · Prefix asymmetry.** Many encoders require instruction prefixes — `query:` on one side,
`passage:` on the other. If the index was built with the passage prefix and the query path
lost the query prefix, recall drops and nothing errors. Check both sides read the same config.

**3 · Normalisation and metric.** Are the new vectors L2-normalised, and is the index still
configured for cosine rather than raw inner product or L2 distance? After normalisation cosine
and dot product give identical rankings; without it they do not, and a schema that "worked
before" quietly stops.

**4 · Dimension truncation.** Was the model output truncated to fit an existing column width?
This happens constantly when the schema is hard to change, and the recall cost is rarely
measured before it ships.

**5 · Context-length truncation.** Does the new encoder have a shorter input limit than the old
one? If so it is silently cutting the tail off your longest chunks — and the tail is often
where the answer is.

**6 · ANN parameters.** Was the graph rebuilt with the same `efConstruction` and `M`? Here is
the key move: **compare against flat exact search on a sample.** Flat search is ground truth.
If flat recall is fine and ANN recall is not, the loss is in the index, not the embedding, and
those have different fixes.

**7 · Only now: the model really is worse on this domain.** And even then I would slice the
misses by question type before concluding it, because "worse on average" and "worse on the
identifier queries that are 30% of our traffic" lead to different responses — the second one
is fixed by leaning harder on the lexical leg, not by reverting.

**Red flags:** starting at step 7; not knowing flat search gives you a ground-truth comparison;
having no plan to bisect.

> **Run it:** [notebook 04 §4.7](../../../../notebooks/04_retrieval_methods_and_reranking.ipynb)
> reproduces steps 1–6 on a live index, each with the measured recall drop.

---
