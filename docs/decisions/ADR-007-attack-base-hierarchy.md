# ADR-007 — Attack base-class hierarchy

- **Status:** Accepted (2026-08-04)
- **Deciders:** Luca (maintainer), assistant

## Context
0.1.x had **two different classes both named `AttackBase`** in `attack_base.py` and
`attack_base_injection.py`, with incompatible signatures:

- obfuscation: `apply(text) / check(text) / sanitized(text)` — a reversible string transform;
- injection: `apply(input_document, injection, …, output_path) / check(document)` — a file-level embed.

The duplication was confusing and the two operations are genuinely different, so a single forced base is wrong.

## Decision (F1–F7)
- **F1 — One root + two specialised ABCs.** `Attack` (root: `name`/`family` metadata + constructor) →
  `ObfuscationAttack` (string-first: `apply/check/sanitize`) and `InjectionAttack` (document-level:
  `apply/check`). Not a single forced base, not Protocols (revisit Protocols for the plugin API in ARC-302).
- **F2 — Home & names.** New `phantomtext/core/` subpackage; `core/base.py`. The two old `attack_base*.py`
  files are deleted.
- **F3 — `sanitized` → `sanitize`.** Renamed to `sanitize`; `sanitized()` kept as a **DeprecationWarning alias**
  on `ObfuscationAttack` (removed at 1.0).
- **F4 — `name`/`family` metadata** added to every technique (powers the STATUS matrix, future plugin
  registry, and report model).
- **F5 — Injection `apply` signature kept compatible** for now (typed; `output_path` keyword-only in the base
  contract). Subclass geometry kwargs unchanged. The real API cleanup is ARC-103.
- **F6 — Honest `check()` stubs.** Injection `check()` returned `True`/`pass` (falsely claiming detection) →
  now `return False  # TODO(ARC-202)` until real detection lands.
- **F7 — Type hints** added to the base ABCs; full subclass typing comes with each module's later rewrite.

## Consequences
- Public import paths of the concrete techniques are unchanged; only `sanitized()` is affected (aliased).
- `core/` becomes the home for cross-cutting abstractions (SecurityPolicy in ARC-201, registry in ARC-302).
- All 8 techniques now share one honest taxonomy; 20 tests pass, mypy/ruff clean.
