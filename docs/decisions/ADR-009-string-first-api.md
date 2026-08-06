# ADR-009 — String-first public API

- **Status:** Accepted (2026-08-06)
- **Deciders:** Luca (maintainer), assistant
- **Arc:** ARC-103
- **Supersedes/realises:** ADR-002 (string-first principle) for the obfuscation/scan/sanitize surface.

## Context
0.1.x exposed four inconsistent, partly-stubbed facade classes (`ContentObfuscator`,
`ContentInjector`, `FileScanner`, `FileSanitizer`) with camelCase technique strings, a
`file_format` argument bolted onto pure string transforms, if/elif dispatch ladders, and a
`FileSanitizer.sanitize_file` that was `pass`. ADR-002 committed the library to a **string-first**
core; ARC-101 unified the attack base classes and ARC-102 made the data offline. ARC-103 turns those
consolidated internals into the ergonomic top-level API users actually touch.

## Decision (H1–H8)

- **H1 — Top-level function verbs.** `phantomtext` exposes module-level functions
  `obfuscate / scan / sanitize / inject / scan_file / sanitize_file` (in `phantomtext/api.py`).
  The concrete technique classes stay public and importable; the verbs are the recommended surface.
- **H2 — Minimal report model.** `scan`/`scan_file` return a `ScanReport` holding `Finding`
  dataclasses (`core/report.py`), not a bare dict. Severity/policy and JSON serialisation are
  deliberately out of scope here — they arrive with ARC-201 (SecurityPolicy) / ARC-204 (JSON reports).
- **H3 — Canonical `name` strings + `Technique` enum.** Techniques are selected by canonical snake_case
  names (`"zero_width"`, `"homoglyph"`, `"diacritical"`, `"bidi"`; injection `"zero_size"`, …). A
  `Technique` string-enum (`core/registry.py`) ships **now** for typed autocomplete; verbs accept
  `str | Technique`. The single legacy camelCase alias `"zeroWidthCharacter"` is still accepted but
  emits `DeprecationWarning`.
- **H4 — Facades become deprecation shims.** `ContentObfuscator`, `ContentInjector`, `FileScanner`,
  `FileSanitizer` keep working, emit `DeprecationWarning`, and delegate to the new API. Removed at 1.0.
- **H5 — Drop `file_format` from string ops.** `obfuscate`/`scan`/`sanitize` are pure `str -> …`
  transforms with no `file_format` parameter. `file_format` survives only where a real document is
  involved (the injection techniques / `inject`).
- **H6 — Technique registry.** `core/registry.py` maps `name -> class` (with `family`), so the verbs
  iterate techniques generically instead of hard-coded if/elif ladders. A public `register()` hook is
  exposed to seed the ARC-302 plugin API and a future auto-generated STATUS matrix.
- **H7 — `sanitize(text)` removes all obfuscation.** By default `sanitize` iterates every registered
  obfuscation technique and strips each. The policy-driven, selective variant lands with ARC-201.
- **H8 — File layer wraps the string core.** `scan_file` / `sanitize_file` do `load → string core →
  (write)`; `inject` stays document-level. `sanitize_file` gives `FileSanitizer` its first real
  behaviour (flipping the ARC-004 xfail). `.txt` is wired through the load/save helpers so the plain-text
  path works now; full multi-format dedupe remains ARC-104.

## Consequences
- New public surface: `pt.obfuscate/scan/sanitize/inject/scan_file/sanitize_file`, plus `Technique`,
  `ScanReport`, `Finding`, and the technique classes.
- The four 0.1 facades still import and run, now with `DeprecationWarning`s; their old return shapes are
  preserved so existing callers keep working until 1.0.
- Dispatch is registry-driven, killing the if/elif ladders and preparing the plugin API (ARC-302).
- `scan`/`sanitize` no longer take `file_format`; the injection API keeps it.
- Not yet done (by design): SecurityPolicy/severity (ARC-201), JSON reports (ARC-204), format dedupe /
  first-class txt across every op (ARC-104), RNG off-by-one fix + numpy drop (ARC-105), batch (ARC-106).
