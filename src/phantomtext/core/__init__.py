"""Core abstractions shared across PhantomText (attack base classes, and
later the security policy and registry)."""

from .base import Attack, InjectionAttack, ObfuscationAttack

__all__ = ["Attack", "ObfuscationAttack", "InjectionAttack"]
