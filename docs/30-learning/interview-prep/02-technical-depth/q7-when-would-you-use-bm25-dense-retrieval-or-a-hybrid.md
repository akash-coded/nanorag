# Q7 · When would you use BM25, dense retrieval, or a hybrid?

BM25 when the query carries identifiers, error codes, API names, SKUs, dates or exact
terminology — anything where the user typed the literal string that is in the document. It is
deterministic, explainable, cheap, easy to filter by metadata, and it benefits from domain
vocabulary an embedding model has never seen. Dense retrieval when the query wording differs
from the corpus wording: paraphrase, description instead of name, a user's register rather
than the author's.

Hybrid when both, which is most enterprise corpora. But I would add two things most answers
miss. First, **hybrid is not free** — fusing a strong retriever with a weak one at equal weight
moves you toward the weak one, and I have measured a corpus where naive equal-weight RRF was
worse than BM25 alone. Second, **the merge method is a real decision**: RRF is rank-based, needs
no tuning and survives score drift; weighted fusion keeps magnitude so a dominant exact match
can win outright, but it needs a labelled set to tune α and that α will not survive a corpus
refresh. Default to RRF, move to weighted only with a labelled set and a plan to re-tune on a
schedule.
