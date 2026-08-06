"""Minimal report model returned by :func:`phantomtext.scan` / :func:`phantomtext.scan_file`.

Deliberately small (ADR-009 / H2): a ``ScanReport`` is just an ordered list of
``Finding`` records plus a couple of conveniences. Severity, security policy, and
JSON serialisation are out of scope here and arrive with ARC-201 / ARC-204.
"""

from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["Finding", "ScanReport"]


@dataclass(frozen=True)
class Finding:
    """A single obfuscation technique detected in the scanned text."""

    #: Canonical technique name, e.g. ``"zero_width"``.
    technique: str
    #: Attack family the technique belongs to, e.g. ``"obfuscation"``.
    family: str

    def __str__(self) -> str:
        return f"{self.family}:{self.technique}"


@dataclass
class ScanReport:
    """The result of scanning a string (or file) for obfuscation.

    Truthiness follows detection: ``bool(report)`` is ``True`` when anything was
    found. Use :attr:`clean` for the opposite, more explicit reading.
    """

    findings: list[Finding] = field(default_factory=list)
    #: Path scanned, when the report came from :func:`phantomtext.scan_file`.
    source: str | None = None

    @property
    def clean(self) -> bool:
        """``True`` when no obfuscation was detected."""
        return not self.findings

    @property
    def techniques(self) -> list[str]:
        """Canonical names of the detected techniques, in scan order."""
        return [f.technique for f in self.findings]

    def __bool__(self) -> bool:
        return bool(self.findings)
