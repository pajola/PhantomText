"""Technique registry — the single source of truth for dispatch (ADR-009 / H6).

The public verbs (``obfuscate`` / ``scan`` / ``sanitize`` / ``inject``) look techniques
up here by canonical ``name`` instead of hard-coding if/elif ladders. Built-in techniques
are registered at import time; :func:`register` is the same hook external plugins will use
in ARC-302, and it also sets up the future auto-generated STATUS matrix.
"""

from __future__ import annotations

import warnings
from enum import Enum

from .base import Attack, InjectionAttack, ObfuscationAttack

__all__ = [
    "Technique",
    "register",
    "get_technique",
    "obfuscation_techniques",
    "injection_techniques",
    "resolve_name",
]


class Technique(str, Enum):
    """Canonical technique names, for typed selection and autocomplete.

    A ``str`` enum, so members compare equal to their value and can be passed
    anywhere a name string is accepted.
    """

    # Obfuscation
    ZERO_WIDTH = "zero_width"
    HOMOGLYPH = "homoglyph"
    DIACRITICAL = "diacritical"
    BIDI = "bidi"
    # Injection
    ZERO_SIZE = "zero_size"
    TRANSPARENT = "transparent"

    def __str__(self) -> str:
        return self.value


#: Registered technique classes, keyed by canonical name (insertion-ordered).
_REGISTRY: dict[str, type[Attack]] = {}

#: Deprecated technique aliases -> canonical name.
_ALIASES: dict[str, str] = {
    "zeroWidthCharacter": "zero_width",
}


def register(cls: type[Attack]) -> type[Attack]:
    """Register a technique class by its ``name``. Usable as a decorator.

    Raises ``ValueError`` if the class has no ``name`` or the name is already taken.
    """
    name = getattr(cls, "name", "")
    if not name:
        raise ValueError(f"{cls.__name__} has no 'name'; cannot register it.")
    if name in _REGISTRY and _REGISTRY[name] is not cls:
        raise ValueError(f"Technique name {name!r} is already registered.")
    _REGISTRY[name] = cls
    return cls


def resolve_name(technique: str) -> str:
    """Normalise a technique selector to its canonical name.

    Accepts a :class:`Technique`, a canonical name, or a deprecated alias
    (which emits a ``DeprecationWarning``). Raises ``ValueError`` if unknown.
    """
    name = technique.value if isinstance(technique, Technique) else str(technique)
    if name in _ALIASES:
        canonical = _ALIASES[name]
        warnings.warn(
            f"Technique name {name!r} is deprecated; use {canonical!r}.",
            DeprecationWarning,
            stacklevel=3,
        )
        name = canonical
    if name not in _REGISTRY:
        raise ValueError(f"Unknown technique: {technique!r}")
    return name


def get_technique(technique: str) -> type[Attack]:
    """Return the technique class for a name/alias/:class:`Technique`."""
    return _REGISTRY[resolve_name(technique)]


def obfuscation_techniques() -> dict[str, type[ObfuscationAttack]]:
    """All registered obfuscation techniques, keyed by canonical name."""
    return {
        name: cls
        for name, cls in _REGISTRY.items()
        if isinstance(cls, type) and issubclass(cls, ObfuscationAttack)
    }


def injection_techniques() -> dict[str, type[InjectionAttack]]:
    """All registered injection techniques, keyed by canonical name."""
    return {
        name: cls
        for name, cls in _REGISTRY.items()
        if isinstance(cls, type) and issubclass(cls, InjectionAttack)
    }


def _register_builtins() -> None:
    """Register the built-in techniques. Imports are local to avoid import cycles."""
    from ..injection.transparent_injection import TransparentInjection
    from ..injection.zerosize_injection import ZeroSizeInjection
    from ..obfuscation.diacritical_marks import DiacriticalMarks
    from ..obfuscation.homoglyph_text import HomoglyphText
    from ..obfuscation.reordering_char import BidiText
    from ..obfuscation.zero_width_text import ZeroWidthText

    for cls in (
        ZeroWidthText,
        HomoglyphText,
        DiacriticalMarks,
        BidiText,
        ZeroSizeInjection,
        TransparentInjection,
    ):
        register(cls)


_register_builtins()
