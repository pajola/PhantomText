"""The ``Finding``/``Report`` data model (ARC-202, ADR-014).

This is a pure data model — no detector logic lives here, and nothing in this
module scans text. It exists so that a detector (Season 3), the ground-truth
corpus (ARC-203), and the evaluation harness (ARC-204) all have one settled
shape to build against.

Not re-exported from :mod:`phantomtext` — the top-level public API shape is a
Type-1 decision reserved for ARC-301. Import from this module directly:
``from phantomtext.core.report import Finding, Report``.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal

__all__ = ["Finding", "Provenance", "Report", "Severity", "Span"]

#: Current schema version (ADR-014, D2). Bump the minor component for
#: additive (new optional field) changes, the major component for anything
#: that could break an existing consumer (a field renamed, removed, or
#: retyped).
SCHEMA_VERSION = "1.0"

# frozen=True only, deliberately not slots=True: combining the two triggers a
# known CPython bug (dataclasses generates a broken __setattr__ that raises a
# confusing `TypeError: super(type, obj): obj must be an instance or subtype
# of type` instead of FrozenInstanceError when an unknown attribute is set --
# reproduced on 3.12.13). Not worth a memory-layout optimization for that.
_FROZEN: dict[str, bool] = {"frozen": True}

# Family IDs are `PT.<CLASS>.<FAMILY>` (ADR-013), e.g. `PT.INVIS.ZERO_WIDTH`.
# A regex format check, not a lookup against docs/spec/TAXONOMY.md (ADR-014,
# D7) -- the taxonomy doc is hand-written Markdown, not a machine-readable
# source an enum/literal could be generated from yet.
_FAMILY_ID_PATTERN = re.compile(r"^PT\.[A-Z]+\.[A-Z_]+$")

SourceKind = Literal["string", "html", "docx", "pdf"]


class Severity(str, Enum):
    """Impact if a :class:`Finding` is a true positive.

    Values match ``docs/spec/TAXONOMY.md``'s severity column verbatim (the
    4-level scale fixed 2026-09-11, DECISION-LOG), so the two documents stay
    directly cross-referenceable with no case-mapping needed.
    """

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


#: ADR-014, D3: severity -> SARIF `level`. SARIF's enum (error/warning/note/
#: none) has no fourth slot, so Critical and High both map to "error"; the
#: original 4-level value is preserved losslessly in a Finding's SARIF
#: `properties.phantomtext_severity` instead of being lost in this mapping.
_SARIF_LEVEL: dict[Severity, str] = {
    Severity.CRITICAL: "error",
    Severity.HIGH: "error",
    Severity.MEDIUM: "warning",
    Severity.LOW: "note",
}


@dataclass(**_FROZEN)
class Span:
    """A location within a scanned string.

    ``char_start``/``char_end`` (Python codepoint indices, half-open --
    ``text[char_start:char_end]``) are the primary, authoritative offsets,
    consistent with the string-first core (ADR-002). ``utf16_start``/
    ``utf16_end`` are optional companions for consumers that expect UTF-16
    code-unit offsets (SARIF viewers, JS-based editors) -- ADR-014, D1.
    """

    char_start: int
    char_end: int
    utf16_start: int | None = None
    utf16_end: int | None = None

    def __post_init__(self) -> None:
        if self.char_start < 0:
            raise ValueError(f"char_start must be >= 0, got {self.char_start}")
        if self.char_end < self.char_start:
            raise ValueError(
                f"char_end ({self.char_end}) must be >= char_start ({self.char_start})"
            )
        if (self.utf16_start is None) != (self.utf16_end is None):
            raise ValueError("utf16_start and utf16_end must both be set or both be None")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"char_start": self.char_start, "char_end": self.char_end}
        if self.utf16_start is not None:
            d["utf16_start"] = self.utf16_start
            d["utf16_end"] = self.utf16_end
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Span:
        return cls(
            char_start=data["char_start"],
            char_end=data["char_end"],
            utf16_start=data.get("utf16_start"),
            utf16_end=data.get("utf16_end"),
        )


@dataclass(**_FROZEN)
class Provenance:
    """Where a :class:`Finding` came from.

    Minimal and extensible (ADR-014, D1): only ``source_kind`` is populated
    for now. ``page``/``node``/``run`` are reserved for ARC-401's Loader
    protocol, which will map format-specific structure (a PDF page, a DOCX
    run, an HTML node) back onto a scanned string's offsets. A Finding
    produced before ARC-401 exists only fills ``source_kind``.
    """

    source_kind: SourceKind
    page: int | None = None
    node: str | None = None
    run: int | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"source_kind": self.source_kind}
        if self.page is not None:
            d["page"] = self.page
        if self.node is not None:
            d["node"] = self.node
        if self.run is not None:
            d["run"] = self.run
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Provenance:
        return cls(
            source_kind=data["source_kind"],
            page=data.get("page"),
            node=data.get("node"),
            run=data.get("run"),
        )


@dataclass(**_FROZEN)
class Finding:
    """One detected occurrence of a taxonomy family in a scanned string.

    ``severity`` and ``confidence`` are independent axes (ADR-014, D4):
    ``severity`` is the family's impact if this is a true positive (defaults
    from ``docs/spec/TAXONOMY.md``, but is per-Finding overridable -- e.g. a
    detector may downgrade a ZWJ hit it recognizes as part of an emoji
    sequence); ``confidence`` is this detector instance's certainty about
    this specific span, a continuous value so an evaluation harness (ARC-204)
    can threshold-sweep for a precision/recall curve rather than being stuck
    with a handful of discrete buckets.
    """

    id: str
    severity: Severity
    confidence: float
    span: Span
    message: str
    provenance: Provenance
    remediation: str | None = None

    def __post_init__(self) -> None:
        if not _FAMILY_ID_PATTERN.match(self.id):
            raise ValueError(
                f"Finding.id {self.id!r} does not match the PT.<CLASS>.<FAMILY> scheme (ADR-013)"
            )
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.id,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "span": self.span.to_dict(),
            "message": self.message,
            "provenance": self.provenance.to_dict(),
        }
        if self.remediation is not None:
            d["remediation"] = self.remediation
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Finding:
        return cls(
            id=data["id"],
            severity=Severity(data["severity"]),
            confidence=data["confidence"],
            span=Span.from_dict(data["span"]),
            message=data["message"],
            provenance=Provenance.from_dict(data["provenance"]),
            remediation=data.get("remediation"),
        )

    def to_sarif_result(self) -> dict[str, Any]:
        """One SARIF ``result`` object for this finding (ADR-014, D3)."""
        return {
            "ruleId": self.id,
            "level": _SARIF_LEVEL[self.severity],
            "message": {"text": self.message},
            "locations": [
                {
                    "physicalLocation": {
                        "region": {
                            "charOffset": self.span.char_start,
                            "charLength": self.span.char_end - self.span.char_start,
                        }
                    }
                }
            ],
            "properties": {
                "phantomtext_severity": self.severity.value,
                "confidence": self.confidence,
            },
        }


@dataclass(**_FROZEN)
class Report:
    """An ordered collection of :class:`Finding`\\ s from one scan."""

    findings: tuple[Finding, ...] = field(default_factory=tuple)
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "findings": [f.to_dict() for f in self.findings],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Report:
        return cls(
            findings=tuple(Finding.from_dict(f) for f in data["findings"]),
            schema_version=data.get("schema_version", SCHEMA_VERSION),
        )

    def to_json(self) -> str:
        # ensure_ascii=True (the json default) is deliberate, not an
        # oversight: it forces every non-ASCII codepoint in a Finding's
        # message/span-adjacent text into a visible \uXXXX escape, which is
        # exactly the property a tool built to make invisible/deceiving
        # characters visible wants from its own report format.
        return json.dumps(self.to_dict(), ensure_ascii=True)

    @classmethod
    def from_json(cls, text: str) -> Report:
        return cls.from_dict(json.loads(text))

    def to_sarif(self) -> dict[str, Any]:
        """A minimal, spec-shaped SARIF 2.1.0 log (ADR-014, D3).

        Covers the fields PhantomText's own findings need; it is not a
        general-purpose SARIF writer.
        """
        rule_ids = sorted({f.id for f in self.findings})
        return {
            "$schema": (
                "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/"
                "master/Schemata/sarif-schema-2.1.0.json"
            ),
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "phantomtext",
                            "informationUri": "https://github.com/pajola/PhantomText",
                            "rules": [{"id": rule_id} for rule_id in rule_ids],
                        }
                    },
                    "results": [f.to_sarif_result() for f in self.findings],
                }
            ],
        }
