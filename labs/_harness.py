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
import importlib.util
import pathlib
import traceback
from collections.abc import Callable


class Blank(str):
    """What a ____ evaluates to before the learner fills it.

    Fill-format starters have blanks at module level (`ANSWER = ____`), and a bare
    NameError there stops the module importing at all -- so no check ever runs and
    the learner sees a traceback instead of "you have a blank left".

    It is a `str` holding the literal text "____" rather than a custom sentinel, on
    purpose: a str works everywhere a value is expected -- re.escape, concatenation,
    .strip() -- so the module imports and every CHECK gets to explain, in its own
    domain terms, what an unfilled blank does to the result. A sentinel that raised
    on every operation could only ever say "blank unfilled" -- true, but less useful
    than "'v2.1.4' was split apart". The one thing a blank must not be is callable.
    """

    def __new__(cls):
        return super().__new__(cls, "____")

    def __repr__(self) -> str:
        return "____"

    def __bool__(self) -> bool:
        return False

    def __call__(self, *_a, **_k):
        raise CheckFailed("a ____ blank is being called like a function -- it is still unfilled")


def load_solution(path, name: str | None = None):
    """Import a starter or reference with ____ pre-bound to the Blank sentinel.

    Every loader in the repo goes through here so the four formats behave the same
    in `lab.py run`, in CI, and in the discussion reviewer.
    """
    path = pathlib.Path(path)
    spec = importlib.util.spec_from_file_location(name or f"sol_{path.parent.name}", path)
    module = importlib.util.module_from_spec(spec)
    module.____ = Blank()
    spec.loader.exec_module(module)
    return module


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


class ImportFailed(Exception):
    """The learner's file did not import. Carries a message written for them."""


def try_load(path, name: str | None = None):
    """load_solution, but an import-time failure becomes an ImportFailed whose
    message a learner can act on -- a leftover blank, a syntax error, a bad
    import -- instead of a traceback through the harness."""
    try:
        return load_solution(path, name)
    except CheckFailed as exc:                       # a ____ used at module level
        raise ImportFailed(f"starter.py could not be imported: {exc}") from exc
    except SyntaxError as exc:
        raise ImportFailed(
            f"starter.py has a syntax error on line {exc.lineno}: {exc.msg}") from exc
    except Exception as exc:  # noqa: BLE001
        raise ImportFailed(
            f"starter.py raised {type(exc).__name__} while importing: {exc}") from exc


def import_failure(checks: list[Check], error: ImportFailed,
                   include_hidden: bool = False) -> list[Result]:
    """Every check fails with the same reason: the file never loaded."""
    return [Result(c.name, False, detail=str(error))
            for c in checks if c.public or include_hidden]


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
