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
| Threat taxonomy (`docs/spec/TAXONOMY.md`) | ✅ | ARC-201 (#10) — 8 `PT.INVIS.*` + 5 `PT.DECEIVE.*` + 8 `PT.DOC.*` families (21 total) with legitimate-use notes, severity/detectability, and citations. No detector code yet — ARC-202/203/204/301+ implement against this spec. |
| Finding schema & severity model | ✅ | ARC-202 (ADR-014) — `phantomtext.core.report`: `Finding`/`Report`/`Span`/`Provenance`, JSON round-trip, SARIF 2.1.0 export. Not re-exported from `phantomtext` (public API shape is ARC-301). No detector produces one yet. |
| Ground-truth corpus | ✅ | ARC-203 (ADR-015) — `corpus/manifests/corpus.jsonl`, 78 deterministic labelled samples (3 positive + 3 benign each) across all 13 text-level families (`PT.INVIS.*` ×8, `PT.DECEIVE.*` ×5); plus a UDHR-sourced benign multilingual corpus (`corpus/benign/`: fa/hi/ar/he/vi/zh + emoji). `PT.DOC.*` (8 document-level families) deferred to ARC-401/ARC-405 — no format writer exists yet. |
| Evaluation harness (precision/recall) | ☐ | ARC-204 |
| Core detection registry | ☐ | ARC-301 |
| String-first API | ⊘ | superseded (ADR-009); string-first-ness itself carried forward into ARC-301's core architecture |
| SecurityPolicy / profiles | ☐ | ARC-304 |
| Batch / parallel processing | ☐ | ARC-602 |
| CLI | ☐ | ARC-601 |
| Docs site | ☐ | ARC-603 |
| Build/packaging (Hatchling, PEP 621) | ✅ | ARC-003 |
| CI (ruff + build-import + pytest matrix + mypy) | ✅ | ARC-003/004 (mypy non-blocking) |
| Offline deterministic test suite | ✅ | 86 passed, 2 xfailed, no network *(as of ARC-203)* |
