#!/usr/bin/env python3
"""Regenerate the ground-truth corpus manifest (ARC-203, ADR-015).

Usage: ``uv run --no-sync python corpus/generate_corpus.py``

Deterministic and offline: every sample's randomness is seeded from its own
``family:kind:index`` string (see ``corpus.generators.common``), so running
this twice produces byte-identical output.
"""

from __future__ import annotations

from pathlib import Path

from corpus.generators import deceive, invis
from corpus.manifest import dump_manifest

OUTPUT_PATH = Path(__file__).parent / "manifests" / "corpus.jsonl"


def main() -> None:
    samples = [*invis.all_samples(), *deceive.all_samples()]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dump_manifest(samples, OUTPUT_PATH)
    print(f"Wrote {len(samples)} samples to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
