"""Deprecated 0.1 facade — kept as a shim over the string-first API (ADR-009 / H4).

Prefer :func:`phantomtext.obfuscate`. This class is removed at 1.0.
"""

from __future__ import annotations

import warnings

from .api import obfuscate as _obfuscate

_SUPPORTED_FORMATS = {"html", "pdf", "docx", "markdown"}


class ContentObfuscator:
    """Deprecated. Use :func:`phantomtext.obfuscate`."""

    def __init__(self) -> None:
        warnings.warn(
            "ContentObfuscator is deprecated and will be removed in 1.0; "
            "use phantomtext.obfuscate().",
            DeprecationWarning,
            stacklevel=2,
        )

    def obfuscate_content(self, content: str) -> str:
        """Deprecated placeholder retained for source compatibility."""
        warnings.warn(
            "ContentObfuscator.obfuscate_content is deprecated and will be removed in 1.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        return content.replace("sensitive_info", "[REDACTED]")

    def obfuscate(
        self,
        x: str,
        y: str,
        obfuscation_technique: str,
        modality: str = "default",
        file_format: str = "html",
    ) -> str:
        """Deprecated. Delegates to :func:`phantomtext.obfuscate`.

        ``file_format`` is validated for backwards compatibility but no longer affects the
        (pure string) transform. The old camelCase ``obfuscation_technique`` values are
        translated to canonical names by the new API (with their own deprecation warning).
        """
        if y not in x:
            raise ValueError("The target context (y) must be contained in the source string (x).")
        if file_format not in _SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {file_format}")
        return _obfuscate(x, y, technique=obfuscation_technique, modality=modality)
