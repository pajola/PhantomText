"""Shared pytest fixtures: determinism + offline operation.

Two cross-cutting concerns for the whole suite:

* **Determinism** — obfuscators use RNG to pick invisible characters. We seed
  both ``random`` and ``numpy`` before every test so runs are reproducible.
* **Offline** — ``HomoglyphText`` normally fetches its confusables table from
  unicode.org at construction time. We patch that fetch with a small fixed map
  so no test touches the network. ARC-102 will replace the fetch with vendored
  data, at which point this patch becomes unnecessary.
"""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pytest

from phantomtext.obfuscation.homoglyph_text import HomoglyphText

FIXTURES = Path(__file__).parent / "fixtures"

# Latin -> Cyrillic look-alikes, standing in for the unicode.org table.
_FAKE_HOMOGLYPHS: dict[str, list[str]] = {
    "a": ["а"],  # CYRILLIC SMALL LETTER A
    "e": ["е"],  # CYRILLIC SMALL LETTER IE
    "o": ["о"],  # CYRILLIC SMALL LETTER O
}


@pytest.fixture(autouse=True)
def _deterministic_and_offline(monkeypatch: pytest.MonkeyPatch):
    random.seed(0)
    np.random.seed(0)
    monkeypatch.setattr(HomoglyphText, "_load_homoglyphs", lambda self: dict(_FAKE_HOMOGLYPHS))
    yield


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES
