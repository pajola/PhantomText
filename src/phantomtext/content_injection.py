"""Deprecated 0.1 facade — kept as a shim over the string-first API (ADR-009 / H4).

Prefer :func:`phantomtext.inject`. This class is removed at 1.0.
"""

from __future__ import annotations

import warnings

from .api import inject as _inject

#: Old Title-Case technique labels -> canonical names.
_LEGACY_TECHNIQUES = {
    "Zero-size": "zero_size",
    "Transparent": "transparent",
}


class ContentInjector:
    """Deprecated. Use :func:`phantomtext.inject`."""

    def __init__(self) -> None:
        warnings.warn(
            "ContentInjector is deprecated and will be removed in 1.0; use phantomtext.inject().",
            DeprecationWarning,
            stacklevel=2,
        )
        self.injection_techniques = list(_LEGACY_TECHNIQUES)

    def inject_content(self, document: str, content: str) -> str:
        """Deprecated. Injects ``content`` into the document at path ``document``.

        Delegates to :func:`phantomtext.inject` (default ``zero_size`` technique) and
        returns the output path. Raises ``ValueError`` for unsupported document formats.
        """
        warnings.warn(
            "ContentInjector.inject_content is deprecated and will be removed in 1.0; "
            "use phantomtext.inject().",
            DeprecationWarning,
            stacklevel=2,
        )
        return _inject(document, content)

    def inject(
        self,
        original_document: str,
        injection: str,
        obfuscation_technique: str,
        modality: str = "default",
        output_document: str | None = None,
    ) -> str:
        """Deprecated. Delegates to :func:`phantomtext.inject`.

        Accepts the old Title-Case technique labels (e.g. ``"Zero-size"``). Returns the
        path the injected document was written to.
        """
        warnings.warn(
            "ContentInjector.inject is deprecated and will be removed in 1.0; "
            "use phantomtext.inject().",
            DeprecationWarning,
            stacklevel=2,
        )
        if obfuscation_technique not in _LEGACY_TECHNIQUES:
            raise ValueError(f"Invalid or unsupported technique: {obfuscation_technique!r}")
        return _inject(
            original_document,
            injection,
            technique=_LEGACY_TECHNIQUES[obfuscation_technique],
            output_path=output_document,
            modality=modality,
        )
