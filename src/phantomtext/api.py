"""The string-first public API (ADR-009).

Top-level verbs that operate on ``str``, with a thin file layer wrapping them:

* :func:`obfuscate` / :func:`scan` / :func:`sanitize` — pure ``str`` transforms.
* :func:`inject` — document-level (embeds a payload into a real file).
* :func:`scan_file` / :func:`sanitize_file` — ``load -> string core -> (write)`` wrappers.

Technique dispatch is registry-driven (``core/registry.py``); there are no if/elif ladders.
"""

from __future__ import annotations

import os
from typing import Any

from .core.registry import (
    Technique,
    get_technique,
    injection_techniques,
    obfuscation_techniques,
    resolve_name,
)
from .core.report import Finding, ScanReport

__all__ = [
    "obfuscate",
    "scan",
    "sanitize",
    "inject",
    "scan_file",
    "sanitize_file",
]

# Obfuscation is a pure string transform; the underlying technique classes still carry a
# vestigial ``file_format`` (removed for real in a later arc). "html" is supported by every
# obfuscator and is used purely as an internal, invisible default here — see ADR-009 / H5.
_STRING_FORMAT = "html"

_TEXT_EXTENSIONS = {".txt", ".md"}


# --------------------------------------------------------------------------- string core


def obfuscate(
    text: str,
    target: str,
    technique: str | Technique = Technique.ZERO_WIDTH,
    *,
    modality: str = "default",
) -> str:
    """Return ``text`` with every occurrence of ``target`` obfuscated.

    Args:
        text: The full source string.
        target: The substring to obfuscate; must occur in ``text``.
        technique: Canonical name or :class:`Technique` (default ``zero_width``).
        modality: Technique-specific intensity (e.g. ``"default"`` / ``"heavy"``).

    Raises:
        ValueError: if ``target`` is not found in ``text`` or ``technique`` is unknown
            (or is an injection technique, which is not a string transform).
    """
    if target not in text:
        raise ValueError("target must be a substring of text")
    cls = _obfuscator(technique)
    attack = cls(modality=modality, file_format=_STRING_FORMAT)
    return text.replace(target, attack.apply(target))


def scan(text: str) -> ScanReport:
    """Scan ``text`` for every registered obfuscation technique.

    Returns a :class:`~phantomtext.core.report.ScanReport` listing each technique detected.
    """
    findings: list[Finding] = []
    for name, cls in obfuscation_techniques().items():
        if cls(file_format=_STRING_FORMAT).check(text):
            findings.append(Finding(technique=name, family=cls.family))
    return ScanReport(findings=findings)


def sanitize(text: str) -> str:
    """Return ``text`` with **all** obfuscation removed (every registered technique)."""
    for cls in obfuscation_techniques().values():
        text = cls(file_format=_STRING_FORMAT).sanitize(text)
    return text


# --------------------------------------------------------------------------- document ops


def inject(
    document_path: str,
    payload: str,
    technique: str | Technique = Technique.ZERO_SIZE,
    *,
    output_path: str | None = None,
    **kwargs: Any,
) -> str:
    """Embed ``payload`` into the document at ``document_path``.

    Args:
        document_path: Path to a ``.pdf`` / ``.docx`` / ``.html`` document.
        payload: The hidden content to embed.
        technique: Canonical name or :class:`Technique` (default ``zero_size``).
        output_path: Where to write the result; defaults next to the input.
        **kwargs: Passed through to the technique (e.g. geometry / ``modality``).

    Returns:
        The path the injected document was written to.

    Raises:
        ValueError: if ``technique`` is unknown, is not an injection technique, or the
            file format is unsupported.
    """
    cls = _injector(technique)
    file_format = _document_format(document_path)
    modality = kwargs.pop("modality", "default")
    if output_path is None:
        stem, _ = os.path.splitext(document_path)
        output_path = f"{stem}_injected.{file_format}"
    attack = cls(modality=modality, file_format=file_format)
    attack.apply(document_path, payload, output_path=output_path, **kwargs)
    return output_path


def scan_file(path: str) -> ScanReport:
    """Load ``path`` as text and :func:`scan` it. Returns a :class:`ScanReport`."""
    report = scan(_read_text(path))
    report.source = path
    return report


def sanitize_file(path: str, *, output_path: str | None = None) -> str:
    """Load ``path``, :func:`sanitize` its text, and write it back.

    Writes in place unless ``output_path`` is given. Returns the sanitized text.
    """
    clean = sanitize(_read_text(path))
    _write_text(output_path or path, clean)
    return clean


# --------------------------------------------------------------------------- internals


def _obfuscator(technique: str | Technique):
    name = resolve_name(technique)
    if name not in obfuscation_techniques():
        raise ValueError(f"{technique!r} is not an obfuscation technique")
    return get_technique(name)


def _injector(technique: str | Technique):
    name = resolve_name(technique)
    if name not in injection_techniques():
        raise ValueError(f"{technique!r} is not an injection technique")
    return get_technique(name)


def _document_format(path: str) -> str:
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext not in {"pdf", "docx", "html"}:
        raise ValueError(f"Unsupported document format: {path!r}")
    return ext


def _read_text(path: str) -> str:
    """Extract text from a file, wiring the plain-text path (ADR-009 / H8)."""
    if os.path.splitext(path)[1].lower() in _TEXT_EXTENSIONS:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    from .text_loader import TextLoader

    return TextLoader().load_text(path)


def _write_text(path: str, text: str) -> None:
    if os.path.splitext(path)[1].lower() in _TEXT_EXTENSIONS:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return
    from .text_saver import TextSaver

    TextSaver().save_text(path, text)
