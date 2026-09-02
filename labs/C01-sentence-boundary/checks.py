from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from labs._harness import Check, Measured, expect  # noqa: E402

TEXT = "Rolled back to v2.1.4 after the page. Latency fell to 80ms! Was it the cache? Yes."


def no_blanks_left(m):
    src = (pathlib.Path(m.__file__)).read_text(encoding="utf-8")
    expect("____" not in src, "there are still ____ blanks in starter.py")


def keeps_version_strings_whole(m):
    got = m.split_sentences(TEXT)
    expect(any("v2.1.4" in s for s in got),
           f"'v2.1.4' was split apart: {got}. A terminator with no whitespace after it is not "
           "a boundary")
    return Measured(f"{len(got)} sentences from {len(TEXT)} chars")


def splits_on_all_three_terminators(m):
    got = m.split_sentences(TEXT)
    expect(len(got) == 4, f"expected 4 sentences ('.', '!', '?' all terminate), got {len(got)}: {got}")


def default_chunk_size_is_three(m):
    got = m.chunk(TEXT)
    expect(len(got) == 2, f"4 sentences at 3 per chunk is 2 chunks, got {len(got)}")
    expect(got[0].count(".") + got[0].count("!") + got[0].count("?") >= 3,
           "the first chunk should hold three sentences")


def digit_can_start_a_sentence(m):
    """Hidden: '2024 was a bad year.' is a sentence."""
    got = m.split_sentences("The outage ended. 2024 was worse. Fine.")
    expect(len(got) == 3, f"a digit can start a sentence; got {got}")


def lowercase_continuation_is_not_a_boundary(m):
    """Hidden: 'e.g. this' must not split."""
    got = m.split_sentences("Use a cache, e.g. redis, for this. Done.")
    expect(len(got) == 2, f"lowercase after a terminator is a continuation, not a boundary: {got}")


def empty_input(m):
    """Hidden."""
    expect(m.split_sentences("") == [], "empty text has no sentences")
    expect(m.chunk("   ") == [], "whitespace has no chunks")


CHECKS = [
    Check("no blanks left", "Fill all three", no_blanks_left),
    Check("keeps version strings whole", "The bug in the Look section", keeps_version_strings_whole),
    Check("splits on . ! and ?", "All three terminators", splits_on_all_three_terminators),
    Check("chunks three sentences by default", "The last blank", default_chunk_size_is_three),
    Check("a digit can start a sentence", "The lookahead class", digit_can_start_a_sentence, public=False),
    Check("lowercase continuation does not split", "e.g. this", lowercase_continuation_is_not_a_boundary, public=False),
    Check("empty input", "Degenerate", empty_input, public=False),
]
