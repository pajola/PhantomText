# STATUS — Implemented vs Not

The single source of truth for what PhantomText can actually do. Update this whenever a capability lands.
Ideally this table becomes auto-generated from a capability registry (Season 1).

**Cell legend:** ✅ implemented & tested · 🟡 works but unverified/partial · 🚧 stub/placeholder · ☐ planned · — N/A

_Last updated: 2026-08-03 (baseline from `phantomtext` 0.1.1 — pre-rebuild)._

## Attacks × formats

Columns: **str** = raw Unicode string · then file formats · **Detect** = scanner finds it · **Sanitize** = remover fixes it.

### Obfuscation
| Technique | str | txt | html | docx | pdf | Detect | Sanitize |
|-----------|:---:|:---:|:----:|:----:|:---:|:------:|:--------:|
| zero-width characters | 🟡 | ☐ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| homoglyph characters  | 🟡 | ☐ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| diacritical marks     | 🟡 | ☐ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| bidi / reordering     | 🟡 | ☐ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| unicode tags block    | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| variation selectors   | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| whitespace substitution | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| full confusables      | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

### Injection
| Technique | str | txt | html | docx | pdf | Detect | Sanitize |
|-----------|:---:|:---:|:----:|:----:|:---:|:------:|:--------:|
| zero-size      | — | — | 🟡 | 🟡 | 🟡 | ☐ | ☐ |
| transparent    | — | — | 🟡 | 🟡 | 🟡 | ☐ | ☐ |
| out-of-bound   | — | — | 🚧 | 🚧 | 🚧 | ☐ | ☐ |
| camouflage     | — | — | 🚧 | 🚧 | 🚧 | ☐ | ☐ |
| metadata       | — | — | ☐ | ☐ | ☐ | ☐ | ☐ |
| font poisoning | — | — | ☐ | ☐ | ☐ | ☐ | ☐ |

_(ARC-102) The homoglyph table is vendored offline — the library makes no runtime network calls anywhere._

## Cross-cutting capabilities
| Capability | Status | Notes |
|-----------|:------:|-------|
| Unified attack base (`core/base.py`) | ✅ | ARC-101 — Attack/ObfuscationAttack/InjectionAttack + `name`/`family` |
| Fully offline (no runtime network) | ✅ | ARC-102 — vendored UTS#39 table; `requests` dropped |
| Threat taxonomy (`docs/spec/TAXONOMY.md`) | 🟡 | ARC-201 — 8 `PT.INVIS.*` + 5 `PT.DECEIVE.*` + 8 `PT.DOC.*` families (21 total) with legitimate-use notes and citations; not yet accepted (PR #10 open, updated per maintainer review) |
| Finding schema & severity model | ☐ | ARC-202 (Type-1: serialized format) |
| Ground-truth corpus | ☐ | ARC-203 |
| Evaluation harness (precision/recall) | ☐ | ARC-204 |
| Core detection registry | ☐ | ARC-301 |
| String-first API | ⊘ | superseded (ADR-009); string-first-ness itself carried forward into ARC-301's core architecture |
| SecurityPolicy / profiles | ☐ | ARC-304 |
| Batch / parallel processing | ☐ | ARC-602 |
| CLI | ☐ | ARC-601 |
| Docs site | ☐ | ARC-603 |
| Build/packaging (Hatchling, PEP 621) | ✅ | ARC-003 |
| CI (ruff + build-import + pytest matrix + mypy) | ✅ | ARC-003/004 (mypy non-blocking) |
| Offline deterministic test suite | ✅ | ARC-004 — 21 passed, 2 xfailed, no network |
