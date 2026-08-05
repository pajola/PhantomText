"""Shared pytest fixtures.

Obfuscators use RNG to pick invisible/look-alike characters, so we seed both
``random`` and ``numpy`` before every test to keep runs reproducible. The whole
library is offline (the homoglyph table is vendored, see ARC-102), so nothing
needs patching to keep tests off the network.
"""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _deterministic():
    random.seed(0)
    np.random.seed(0)
    yield


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES
