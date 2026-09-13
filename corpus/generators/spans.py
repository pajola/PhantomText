"""Span-derivation helpers shared by the per-family generators (ARC-203)."""

from __future__ import annotations

from collections.abc import Callable

from corpus.manifest import CorpusSpan


def spans_from_membership(text: str, is_inserted: Callable[[str], bool]) -> tuple[CorpusSpan, ...]:
    """Merge contiguous runs of codepoints satisfying ``is_inserted`` into spans.

    Correct for insertion-only attacks (the original characters are all still
    present, unmodified, interleaved with newly-inserted ones) -- zero-width,
    bidi, Zalgo-style stacking, soft hyphen, tag characters, and similar.
    """
    spans: list[CorpusSpan] = []
    start: int | None = None
    for i, ch in enumerate(text):
        if is_inserted(ch):
            if start is None:
                start = i
        elif start is not None:
            spans.append(CorpusSpan(start, i))
            start = None
    if start is not None:
        spans.append(CorpusSpan(start, len(text)))
    return tuple(spans)


def spans_from_diff(clean: str, attacked: str) -> tuple[CorpusSpan, ...]:
    """Merge contiguous runs of differing codepoints between two equal-length strings.

    Correct for substitution attacks (homoglyphs, confusables, styled
    alphanumerics, whitespace substitution) where a character is replaced
    in-place rather than inserted.
    """
    if len(clean) != len(attacked):
        raise ValueError("spans_from_diff requires equal-length clean/attacked text")
    spans: list[CorpusSpan] = []
    start: int | None = None
    for i, (c, a) in enumerate(zip(clean, attacked)):
        if c != a:
            if start is None:
                start = i
        elif start is not None:
            spans.append(CorpusSpan(start, i))
            start = None
    if start is not None:
        spans.append(CorpusSpan(start, len(attacked)))
    return tuple(spans)
