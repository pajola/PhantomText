# ARC-101 — Unify `AttackBase`

- **Season:** 1 — Core API Consolidation
- **Branch:** `arc/101-unify-attackbase` (off `main`)
- **Status:** ◐ in progress (awaiting maintainer review)
- **Depends on:** Season 0

## Goal
Replace the two duplicate, incompatible `AttackBase` classes with one honest hierarchy, and migrate all 8
techniques to it. Internal refactor — the working transforms are untouched. (ADR-007)

## Done
- New **`phantomtext/core/`** package with `base.py`: `Attack` root + `ObfuscationAttack` (`apply/check/sanitize`)
  + `InjectionAttack` (`apply/check`), all typed.
- Migrated 4 obfuscation + 4 injection techniques to the new bases; deleted `attack_base.py` +
  `attack_base_injection.py`.
- `sanitized` → **`sanitize`** on obfuscators; `sanitized()` kept as a DeprecationWarning alias.
- Added `name` to each technique (`family` comes from the base).
- Fixed dishonest injection `check()` stubs (`return True`/`pass` → `return False  # TODO(ARC-202)`).

## Out of scope (later arcs)
- String-first public facade (ARC-103), offline homoglyph (ARC-102), RNG off-by-one (ARC-105),
  real injection detection (ARC-202), pypdf migration.

## Acceptance criteria
- [x] One base hierarchy; both old files removed; no lingering `attack_base` refs
- [x] `sanitize` + deprecation-aliased `sanitized`; `name`/`family` on every technique
- [x] Suite green (20 passed, 2 xfailed) + ruff/mypy clean; import unchanged
- [ ] CI green; maintainer approves PR

## Session log
- 2026-08-04 — Created `core/base.py`; migrated 8 subclasses via sed + targeted edits; updated tests
  (sanitize + alias-deprecation + metadata tests). ADR-007 accepted.
