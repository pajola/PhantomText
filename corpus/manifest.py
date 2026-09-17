"""The ground-truth corpus manifest data model (ARC-203, ADR-015 D1).

A manifest entry is a *label* -- what a future detector should (or must not)
find -- not a detection result. Deliberately not a serialized
``phantomtext.core.report.Finding``: coupling the corpus's frozen on-disk
shape to ``Finding``'s own future evolution (new provenance fields, a
confidence-model change, ...) would make every detector-schema change also a
corpus-baseline break. ``CorpusSpan`` mirrors ``Span``'s offset convention
only so the two remain easy to diff against each other later.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

__all__ = ["CorpusSample", "CorpusSpan", "dump_manifest", "load_manifest"]

_FAMILY_ID_PATTERN = re.compile(r"^PT\.[A-Z]+\.[A-Z_]+$")

SampleKind = Literal["positive", "benign"]


@dataclass(frozen=True)
class CorpusSpan:
    """A labelled character-offset region within a sample's ``attacked_text``.

    Codepoint indices, half-open (``text[char_start:char_end]``) -- same
    convention as ``phantomtext.core.report.Span.char_start``/``char_end``.
    """

    char_start: int
    char_end: int

    def __post_init__(self) -> None:
        if self.char_start < 0:
            raise ValueError(f"char_start must be >= 0, got {self.char_start}")
        if self.char_end < self.char_start:
            raise ValueError(
                f"char_end ({self.char_end}) must be >= char_start ({self.char_start})"
            )

    def to_dict(self) -> dict[str, Any]:
        return {"char_start": self.char_start, "char_end": self.char_end}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CorpusSpan:
        return cls(char_start=data["char_start"], char_end=data["char_end"])


@dataclass(frozen=True)
class CorpusSample:
    """One labelled clean/attacked or benign example for a taxonomy family.

    ``kind="positive"`` samples must carry a non-null ``attacked_text`` and at
    least one ``spans`` entry (the region a detector is expected to flag).
    ``kind="benign"`` samples carry no ``attacked_text`` and no spans --
    ``clean_text`` alone is the example a detector must *not* flag.
    """

    id: str
    family: str
    kind: SampleKind
    clean_text: str
    attacked_text: str | None
    spans: tuple[CorpusSpan, ...]
    source: str
    generator_seed: str
    locale: str | None = None
    script: str | None = None

    def __post_init__(self) -> None:
        if not _FAMILY_ID_PATTERN.match(self.family):
            raise ValueError(
                f"CorpusSample.family {self.family!r} does not match the "
                "PT.<CLASS>.<FAMILY> scheme (ADR-013)"
            )
        if self.kind == "positive":
            if self.attacked_text is None:
                raise ValueError(f"{self.id}: positive sample must set attacked_text")
            if not self.spans:
                raise ValueError(f"{self.id}: positive sample must have at least one span")
            for s in self.spans:
                if s.char_end > len(self.attacked_text):
                    raise ValueError(
                        f"{self.id}: span {s} out of bounds for attacked_text "
                        f"(len={len(self.attacked_text)})"
                    )
        elif self.kind == "benign":
            if self.attacked_text is not None:
                raise ValueError(f"{self.id}: benign sample must not set attacked_text")
            if self.spans:
                raise ValueError(f"{self.id}: benign sample must not carry spans")
        else:
            raise ValueError(f"{self.id}: kind must be 'positive' or 'benign', got {self.kind!r}")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.id,
            "family": self.family,
            "kind": self.kind,
            "clean_text": self.clean_text,
            "attacked_text": self.attacked_text,
            "spans": [s.to_dict() for s in self.spans],
            "source": self.source,
            "generator_seed": self.generator_seed,
        }
        if self.locale is not None:
            d["locale"] = self.locale
        if self.script is not None:
            d["script"] = self.script
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CorpusSample:
        return cls(
            id=data["id"],
            family=data["family"],
            kind=data["kind"],
            clean_text=data["clean_text"],
            attacked_text=data.get("attacked_text"),
            spans=tuple(CorpusSpan.from_dict(s) for s in data.get("spans", [])),
            source=data["source"],
            generator_seed=data["generator_seed"],
            locale=data.get("locale"),
            script=data.get("script"),
        )


def dump_manifest(samples: list[CorpusSample], path: str | Path) -> None:
    """Write ``samples`` to ``path`` as JSONL, one sample per line."""
    lines = [json.dumps(s.to_dict(), ensure_ascii=True) for s in samples]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_manifest(path: str | Path) -> list[CorpusSample]:
    """Read a JSONL manifest back into ``CorpusSample`` objects."""
    text = Path(path).read_text(encoding="utf-8")
    return [CorpusSample.from_dict(json.loads(line)) for line in text.splitlines() if line.strip()]
