"""Deprecated 0.1 facade — kept as a shim over the string-first API (ADR-009 / H4, H8).

Prefer :func:`phantomtext.sanitize_file`. In 0.1 ``sanitize_file`` was a no-op (``pass``);
it now actually removes obfuscation via the string core. This class is removed at 1.0.
"""

from __future__ import annotations

import warnings

from .api import sanitize_file as _sanitize_file


class FileSanitizer:
    """Deprecated. Use :func:`phantomtext.sanitize_file`."""

    def __init__(self) -> None:
        warnings.warn(
            "FileSanitizer is deprecated and will be removed in 1.0; "
            "use phantomtext.sanitize_file().",
            DeprecationWarning,
            stacklevel=2,
        )

    def sanitize_file(self, file_path: str, output_path: str | None = None) -> bool:
        """Remove obfuscation from ``file_path`` (in place unless ``output_path`` given).

        Returns ``True`` on success (delegates to :func:`phantomtext.sanitize_file`).
        """
        _sanitize_file(file_path, output_path=output_path)
        return True
