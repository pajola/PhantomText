"""Shared helpers for the per-family corpus generators (ARC-203).

Determinism (DECISION-LOG 2026-09-13): every sample's randomness is seeded
from its own ``f"{family}:{kind}:{index}"`` string, never from global
``random``/``numpy`` state left over from a previous family. The legacy
``phantomtext.obfuscation.*`` techniques this module's callers reuse for five
families use ``np.random`` internally with no way to inject a ``Random``
instance, so :func:`seeded_numpy` seeds the *global* numpy RNG immediately
before each call -- safe here only because generation is strictly sequential
and single-threaded.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from contextlib import contextmanager

import numpy as np

#: Three short, plain-ASCII base sentences reused across character-level
#: families for positive-sample generation, so each family's 3 positive
#: samples vary the surrounding text rather than repeating one fixture.
BASE_SENTENCES = [
    "Please review the attached quarterly report.",
    "The meeting has been rescheduled to next Monday.",
    "Our team completed the migration successfully.",
]

SAMPLES_PER_KIND = 3  # DECISION-LOG 2026-09-13: 3 positive + 3 benign per family.


def seed_for(family: str, kind: str, index: int) -> str:
    """The stable seed string for one sample -- also stored as ``generator_seed``."""
    return f"{family}:{kind}:{index}"


def _seed_int(seed: str) -> int:
    # Stable across runs/machines (unlike Python's salted hash()); truncated
    # to fit numpy's/random's 32-bit seed range.
    return int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16)


def make_rng(seed: str) -> np.random.Generator:
    """A fresh, independently-seeded RNG for hand-written (non-legacy) generators."""
    return np.random.default_rng(_seed_int(seed))


@contextmanager
def seeded_numpy(seed: str) -> Iterator[None]:
    """Seed the global ``numpy`` RNG for the duration of a legacy-technique call.

    The legacy ``phantomtext.obfuscation.*`` classes call ``np.random.*``
    directly (global state, no injectable ``Random``/``Generator``) -- see the
    module docstring.
    """
    state = np.random.get_state()
    try:
        np.random.seed(_seed_int(seed) % (2**32 - 1))
        yield
    finally:
        np.random.set_state(state)


def sample_id(family: str, kind: str, index: int) -> str:
    short = family.split(".", 1)[1].lower().replace(".", "_")
    return f"{short}-{kind}-{index}"
