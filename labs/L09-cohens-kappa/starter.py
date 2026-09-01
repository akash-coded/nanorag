"""L09 · Cohen's kappa.

Labels are booleans: True means "correct".

Run:  python scripts/lab.py run L09
"""
from __future__ import annotations


def confusion(human: list[bool], judge: list[bool]) -> dict[str, int]:
    """Return {"tt": .., "tf": .., "ft": .., "ff": ..}

    tt = both said True,  tf = human True judge False,
    ft = human False judge True,  ff = both said False.
    Raise ValueError if the two lists differ in length.
    """
    # TODO
    raise NotImplementedError


def cohens_kappa(human: list[bool], judge: list[bool]) -> float:
    """(p_o - p_e) / (1 - p_e)

      p_o = observed agreement = (tt + ff) / n
      p_e = sum over classes of (human rate * judge rate)
          = (h_true * j_true) + (h_false * j_false)

    If p_e == 1.0 (both raters used exactly one class for everything) there is
    no agreement left to earn beyond chance: return 0.0 rather than dividing by
    zero. With no labels at all, return 0.0.
    """
    # TODO
    raise NotImplementedError


def agreement_report(human: list[bool], judge: list[bool]) -> dict:
    """{"n", "raw", "kappa", "base_rate"}

    `raw` is observed agreement, `base_rate` is the HUMAN positive rate.
    A kappa without its base rate is not comparable to anyone else's, so this
    function refuses to return one without the other.
    """
    # TODO
    raise NotImplementedError
