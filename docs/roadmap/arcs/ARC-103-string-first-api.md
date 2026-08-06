# ARC-103 — String-first public API

- **Season:** 1 — Core API Consolidation
- **Branch:** `arc/103-string-first-api` (off `main`)
- **Status:** ☐ planned — **decisions H1–H8 awaiting maintainer sign-off** (do not implement yet)
- **Depends on:** ARC-101 (unified base), ARC-102 (offline data)

## Goal
Give PhantomText the clean, string-first public API promised by **ADR-002**: ergonomic top-level verbs that
operate on `str`, with the file layer wrapping them, replacing the inconsistent/half-stub 0.1 facades
(`ContentObfuscator`, `ContentInjector`, `FileScanner`, `FileSanitizer`) — kept as deprecation shims. This is
the centerpiece arc that turns the consolidated internals (ARC-101) into the API users actually touch.

## Proposed shape (illustrative — pending sign-off)
```python
import phantomtext as pt

pt.obfuscate(text, target, technique="zero_width")   # str -> str (a target substring)
pt.scan(text)                                         # str -> ScanReport (findings)
pt.sanitize(text)                                     # str -> str (remove all obfuscation)
pt.inject(document_path, payload, technique="zero_size", output_path=...)   # document-level
pt.scan_file(path); pt.sanitize_file(path, output_path=...)                 # file wrappers
```

## Decisions to confirm (H1–H8)
| # | Decision | Proposed |
|---|----------|----------|
| **H1** | API surface | Top-level **functions** (`pt.obfuscate/scan/sanitize/inject/scan_file/sanitize_file`) exposed from `phantomtext`, over the technique classes (which stay public) |
| **H2** | `scan` return type | A minimal **`ScanReport`/`Finding` dataclass** (`core/report.py`); full severity/policy model comes in ARC-201/204 (vs a bare dict) |
| **H3** | Technique selection | Canonical **`name` strings** (`"zero_width"`, `"homoglyph"`, `"diacritical"`, `"bidi"`); deprecate the old camelCase (`"zeroWidthCharacter"`). Optional `Technique` enum |
| **H4** | 0.1 facades | Keep `ContentObfuscator`/`ContentInjector`/`FileScanner`/`FileSanitizer` as **DeprecationWarning shims** delegating to the new API (removed at 1.0) |
| **H5** | `file_format` on string ops | **Drop it** from `obfuscate`/`sanitize` — it's irrelevant to a pure string transform; keep it only where a real document is involved |
| **H6** | Technique registry | Add `core/registry.py` keyed by `name`/`family` so the verbs iterate techniques generically (kills the if/elif ladders; sets up the ARC-302 plugin API + auto STATUS matrix) |
| **H7** | `sanitize(text)` scope | Remove **all** obfuscation families by default (iterate the registry); the policy-driven variant arrives with ARC-201 (SecurityPolicy) |
| **H8** | File layer | `scan_file`/`sanitize_file` wrap `load → string core → (write)`; `inject` stays document-level. `FileSanitizer` real behavior still lands here (was xfail in ARC-004) |

## Out of scope (later)
- `SecurityPolicy`/severity thresholds (ARC-201), structured JSON reports (ARC-204), first-class txt + format
  dedupe (ARC-104), RNG fix + drop numpy (ARC-105), batch/parallel (ARC-106).

## Acceptance criteria (once approved)
- [ ] Top-level string-first verbs implemented + typed; registry drives dispatch
- [ ] Deprecation shims keep 0.1 imports working (with warnings) — add tests
- [ ] `FileSanitizer`/`sanitize` actually removes obfuscation (flip the ARC-004 xfail)
- [ ] Suite green offline + ruff/mypy clean; ADR for the API shape (ADR-009)

## Session log
- 2026-08-05 — Plan drafted during ARC-102 handoff; awaiting sign-off on H1–H8 before implementation.
