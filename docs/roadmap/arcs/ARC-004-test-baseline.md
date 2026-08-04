# ARC-004 — Deterministic offline test baseline

- **Season:** 0
- **Branch:** `arc/004-test-baseline` (off `main`)
- **Status:** ◐ in progress (awaiting maintainer review)
- **Depends on:** ARC-003

## Goal
A green, **offline, deterministic** pytest suite that pins the *actual* behavior of the working core, plus
pytest + mypy jobs in CI. Closes Season 0. Tests + CI only — no package source changes.

## Done
- **`tests/conftest.py`** — autouse fixture seeds `random`/`numpy` and patches `HomoglyphText._load_homoglyphs`
  with a small fixed Latin→Cyrillic map, so no test touches the network (E3). `fixtures_dir` helper.
- **Rewrote the suite as pytest functions** (E1), replacing the old unittest files that wrote to a missing
  `./output`, hit the network, and asserted on stubs:
  - `test_obfuscation.py` — zero-width / diacritical / bidi / homoglyph: `apply`→`check`→`sanitized` round-trip;
    `ContentObfuscator` target removal + validation errors.
  - `test_scanning.py` — `FileScanner` detects zero-width in `tmp_path` files; clean files pass; dir aggregation.
  - `test_formats.py` — loaders read the fixture pdf/docx/html; txt Unicode round-trip; unsupported-format error.
  - `test_injection.py` — zero-size injection round-trips (html payload embedded; pdf/docx output produced).
  - `test_stubs_xfail.py` — `xfail(strict=False)` for `ContentInjector` validation (→ARC-103) and
    `FileSanitizer` removal (→ARC-203) (E2).
- **CI:** added a **pytest** matrix job (3.9–3.13, with coverage report) and a **mypy** job
  (`continue-on-error`, non-blocking) (E4, E5).

## Result
`uv run pytest` → **18 passed, 2 xfailed** in <0.5s, offline and reproducible. ruff + mypy clean.

## Out of scope (later)
- Implementing sanitizer/injector features (S1/S2); vendoring homoglyph data (ARC-102); pypdf migration;
  typing the code / making mypy blocking.

## Acceptance criteria
- [x] Suite passes offline & deterministically; no writes outside `tmp_path`
- [x] ruff + mypy clean; CI pytest + mypy jobs added
- [ ] CI green on GitHub; maintainer approves PR → **Season 0 complete**

## Session log
- 2026-08-04 — Wrote conftest + 5 test modules; removed 5 legacy test files; added CI test/type jobs.
