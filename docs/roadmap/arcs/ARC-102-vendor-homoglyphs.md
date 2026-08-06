# ARC-102 — Vendor homoglyph data offline

- **Season:** 1 — Core API Consolidation
- **Branch:** `arc/102-vendor-homoglyphs` (off `main`)
- **Status:** ◐ in progress (awaiting maintainer review)
- **Depends on:** ARC-101

## Goal
Ship the Unicode confusables table in-package, remove the last runtime network call in the library, and drop
`requests`. Obfuscation behavior unchanged. (ADR-008)

## Done
- Vendored `intentional.txt` (byte-for-byte upstream, ~6.5 KB) in `src/phantomtext/data/`; packaged in the wheel.
- Rewrote `HomoglyphText._load_homoglyphs` → module-level `@lru_cache` `_load_homoglyph_table()` that parses
  the vendored file by hex codepoints (robust). Removed `import requests`.
- **Dropped `requests`** (and `types-requests`) from `pyproject`.
- Added `python -m phantomtext.data.refresh_homoglyphs` (stdlib `urllib`, dev-only).
- Removed the conftest network patch; tests use the real vendored data. New tests assert `A→Α`, ASCII-not-flagged,
  and that the table is cached.

## Result
**The library is now fully offline** — no runtime network anywhere. 21 passed, 2 xfailed; ruff/mypy clean;
`requests` uninstalled from the resolved env.

## Out of scope (later)
- Drop `numpy` / fix RNG off-by-one (ARC-105); string-first public API (ARC-103); real injection detection (ARC-202).

## Acceptance criteria
- [x] Homoglyph data vendored + packaged in wheel; parsed offline & cached
- [x] `requests` removed from deps and code; no runtime network
- [x] Refresh tool works (stdlib only); suite green; ruff/mypy clean
- [ ] CI green; maintainer approves PR

## Session log
- 2026-08-05 — Vendored data + refresh tool; rewrote loader; dropped requests; simplified tests. ADR-008.
