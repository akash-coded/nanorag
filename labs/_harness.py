"""The check harness every lab runs against.

Two things separate a lab from a code kata, and both live here.

**Checks are split public / hidden.** Public checks are visible in the brief and
tell you whether you have understood the task. Hidden checks run on submit and
cover the cases the brief deliberately does not mention -- empty input, a
duplicate id, a boundary. A solution that passes the public checks and fails the
hidden ones is the normal experience, and it is the point: the gap between them
is where the brief's assumptions were doing work you did not notice.

**Checks can return a measurement, not just a verdict.** A lab that only says
pass or fail teaches you to satisfy a test. A lab that says "passes, and your
packer used 6,100 tokens where the reference used 4,140" teaches you that
correctness was the easy half. Any check may attach `measure=` and the runner
prints it next to the result.
"""
from __future__ import annotations

import dataclasses
import traceback
from collections.abc import Callable


@dataclasses.dataclass
class Result:
    name: str
    passed: bool
    detail: str = ""
    measure: str = ""


@dataclasses.dataclass
class Check:
    """One assertion about a learner's solution.

    `fn` receives the learner's module and either returns None (pass), a string
    (fail, with the reason), or a Measured (pass, with a number worth seeing).
    """
    name: str
    why: str
    fn: Callable
    public: bool = True


@dataclasses.dataclass
class Measured:
    """Returned by a check that passed and has a number worth reporting."""
    value: str


class CheckFailed(AssertionError):
    """Raised inside a check to fail it with a specific, useful message."""


def expect(condition: bool, message: str) -> None:
    """Assert with a message written for the learner, not for the author.

    Use this rather than bare `assert`: a check that fails with
    `assert result == expected` tells the learner nothing they did not know.
    """
    if not condition:
        raise CheckFailed(message)


def run_checks(module, checks: list[Check], include_hidden: bool = False) -> list[Result]:
    results: list[Result] = []
    for check in checks:
        if not check.public and not include_hidden:
            continue
        try:
            outcome = check.fn(module)
            measure = outcome.value if isinstance(outcome, Measured) else ""
            results.append(Result(check.name, True, measure=measure))
        except CheckFailed as exc:
            results.append(Result(check.name, False, detail=str(exc)))
        except NotImplementedError:
            results.append(Result(check.name, False, detail="not implemented yet"))
        except Exception as exc:  # noqa: BLE001 - the learner's exception is the message
            line = traceback.format_exc().strip().split("\n")[-1]
            results.append(Result(check.name, False,
                                  detail=f"{type(exc).__name__}: {exc}".strip() or line))
    return results
