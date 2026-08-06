# ADR-008 — Offline homoglyph data

- **Status:** Accepted (2026-08-05)
- **Deciders:** Luca (maintainer), assistant

## Context
`HomoglyphText` fetched the Unicode UTS#39 confusables table (`intentional.txt`) from unicode.org **at every
instantiation**, with a fragile positional parser and no caching, timeout, or offline path. `FileScanner`
constructs a `HomoglyphText`, so every scan hit the network. This was the last runtime network call in the
library.

## Decision (G1–G6)
- **G1 — Vendor the raw file.** Ship Unicode's `intentional.txt` byte-for-byte in `src/phantomtext/data/`
  (~6.5 KB) and parse it at runtime, rather than shipping a pre-digested JSON. It is the most auditable,
  single-source-of-truth option; the file is tiny.
- **G2 — Refresh tool.** `python -m phantomtext.data.refresh_homoglyphs` re-downloads the table using stdlib
  `urllib` (dev-only).
- **G3 — Drop `requests`** entirely (runtime and dev). The refresh tool uses `urllib`.
- **G4 — Cache once.** `_load_homoglyph_table()` is module-level `@lru_cache(maxsize=1)` — parsed once per
  process, not per `HomoglyphText()`.
- **G5 — Tests use real data.** The old conftest network-patch is removed; tests exercise the vendored table.
  (Verified: no ASCII characters appear as confusable glyphs, so `check()` does not false-positive on clean
  ASCII text.)
- **G6 — Robust parser.** Parse by hex codepoints; skip multi-codepoint sequences; keep `base → [glyphs]`.

## Consequences
- **The library is now fully offline** — no runtime network anywhere. Smaller install (no `requests`).
- Data provenance is recorded in `data/__init__.py`; updating it is a deliberate, reviewable step (run the
  refresh tool, commit the diff).
- Obfuscation behavior is unchanged.
