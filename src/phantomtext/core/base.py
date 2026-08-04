"""Base classes for PhantomText attack techniques.

The two attack families have genuinely different shapes, so they get two
specialised abstract bases sharing one lightweight root:

* :class:`ObfuscationAttack` — a reversible ``str`` -> ``str`` transform
  (``apply`` / ``check`` / ``sanitize``). This is the string-first core.
* :class:`InjectionAttack` — embeds a payload into a document *file*
  (``apply`` / ``check``); it is not a pure string transform.

Both share :class:`Attack`, which carries the ``name``/``family`` metadata used
by the STATUS matrix, the (future) plugin registry, and reports.
"""

from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Any

__all__ = ["Attack", "ObfuscationAttack", "InjectionAttack"]


class Attack(ABC):  # noqa: B024  (intentional root: propagates ABCMeta, no abstract methods of its own)
    """Common root for every attack technique."""

    #: Attack family, set by each specialised base ("obfuscation" | "injection").
    family: str = ""
    #: Short technique identifier, set by each concrete class (e.g. "zero_width").
    name: str = ""

    def __init__(self, modality: str = "default", file_format: str = "pdf") -> None:
        self.modality = modality
        self.file_format = file_format


class ObfuscationAttack(Attack):
    """A reversible, string-in / string-out obfuscation technique."""

    family = "obfuscation"

    @abstractmethod
    def apply(self, text: str) -> str:
        """Return ``text`` with this obfuscation applied."""

    @abstractmethod
    def check(self, text: str) -> bool:
        """Return ``True`` if ``text`` shows signs of this obfuscation."""

    @abstractmethod
    def sanitize(self, text: str) -> str:
        """Return ``text`` with this obfuscation removed."""

    def sanitized(self, text: str) -> str:
        """Deprecated alias for :meth:`sanitize` (removed in 1.0)."""
        warnings.warn(
            "sanitized() is deprecated and will be removed in 1.0; use sanitize().",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.sanitize(text)


class InjectionAttack(Attack):
    """Embeds hidden content into a document (PDF/DOCX/HTML)."""

    family = "injection"

    @abstractmethod
    def apply(
        self,
        input_document: str,
        injection: str,
        *,
        output_path: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Embed ``injection`` into ``input_document``, writing to ``output_path``.

        Concrete techniques may accept extra keyword arguments (e.g. geometry);
        the full API is cleaned up in ARC-103.
        """

    @abstractmethod
    def check(self, input_document: str) -> bool:
        """Return ``True`` if ``input_document`` appears to contain an injection."""
