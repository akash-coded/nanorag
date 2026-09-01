from __future__ import annotations

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

CORPUS = [
    "the service returned ERR_CONN_RESET after a timeout",
    "the service was healthy",
    "the timeout was increased",
    "a service restart cleared the timeout",
]


def counts_documents_not_occurrences(m):
    df = m.df_from_corpus(["the the the cat", "the dog"])
    expect(df["the"] == 2,
           f"df['the'] should be 2 (it appears in 2 documents), got {df['the']} — "
           "you are counting occurrences, not documents")
    expect(df["cat"] == 1, f"df['cat'] should be 1, got {df.get('cat')}")


def rare_term_scores_high(m):
    got = m.idf(1000, 3)
    expect(abs(got - 5.6525) < 0.01, f"idf(1000, 3) should be ≈5.6525, got {got:.4f}")
    return Measured("a term in 3 of 1000 documents is worth +5.65")


def goes_negative(m):
    got = m.idf(1000, 890)
    expect(got < 0,
           f"idf(1000, 890) should be NEGATIVE, got {got:.4f}. A term in 89% of the corpus is "
           "evidence against relevance. If you floored at zero, remove the floor")
    expect(abs(got - (-2.0868)) < 0.01, f"expected ≈ -2.0868, got {got:.4f}")
    return Measured("a term in 890 of 1000 documents is worth −2.09 — the stop list, derived")


def crossover_near_half(m):
    below = m.idf(1000, 499)
    above = m.idf(1000, 501)
    expect(below > 0 > above,
           f"IDF should cross zero near df = N/2; got {below:.4f} at 499 and {above:.4f} at 501")
    return Measured("sign flips between df=499 and df=501 — half the collection is the pivot")


def df_zero_is_finite(m):
    """Hidden: the 0.5 smoothing exists to make this finite."""
    got = m.idf(1000, 0)
    expect(math.isfinite(got),
           "idf(1000, 0) is not finite — you dropped the 0.5 smoothing and divided by zero")


def df_equals_n_is_finite(m):
    """Hidden: the other end of the same smoothing."""
    got = m.idf(1000, 1000)
    expect(math.isfinite(got),
           "idf(1000, 1000) is not finite — with df = N the numerator is zero without smoothing")
    expect(got < 0, f"a term in every document should score negative, got {got:.4f}")


def monotone_decreasing(m):
    """Hidden: more documents must never mean more weight."""
    values = [m.idf(1000, d) for d in (1, 10, 100, 500, 900)]
    pairs = list(zip(values, values[1:]))
    expect(all(a > b for a, b in pairs),
           f"IDF must decrease as df rises; got {[round(v, 3) for v in values]}")


def integrates_with_df(m):
    """Hidden: the two functions have to work together."""
    df = m.df_from_corpus(CORPUS)
    n = len(CORPUS)
    the = m.idf(n, df["the"])
    err = m.idf(n, df["err_conn_reset"])
    expect(err > the,
           f"ERR_CONN_RESET ({err:.3f}) should outscore 'the' ({the:.3f}) on this corpus")
    return Measured(f"on a 4-doc corpus: err_conn_reset {err:+.2f} vs the {the:+.2f}")


CHECKS = [
    Check("df counts documents, not occurrences", "The classic off-by-many", counts_documents_not_occurrences),
    Check("a rare term scores high", "idf(1000, 3) ≈ 5.71", rare_term_scores_high),
    Check("a ubiquitous term goes negative", "The sign is the lesson", goes_negative),
    Check("the sign flips near half the collection", "Where the pivot is", crossover_near_half),
    Check("df=0 stays finite", "Why the 0.5 is there", df_zero_is_finite, public=False),
    Check("df=N stays finite and negative", "The other end", df_equals_n_is_finite, public=False),
    Check("IDF decreases monotonically with df", "No accidental sign errors", monotone_decreasing, public=False),
    Check("df and idf compose on a real corpus", "End to end", integrates_with_df, public=False),
]
