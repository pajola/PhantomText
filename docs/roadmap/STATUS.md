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
| homoglyph characters  | 🟡 | ☐ | 🟡 | 🟡 | 🟡 | 🟡¹ | 🟡 |
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

¹ homoglyph detection currently requires a **runtime network fetch** to unicode.org — to be removed (ARC-102).

## Cross-cutting capabilities
| Capability | Status | Notes |
|-----------|:------:|-------|
| String-first API | ☐ | ARC-103 |
| Batch / parallel processing | ☐ | ARC-106 |
| SecurityPolicy / profiles | ☐ | ARC-201 |
| Structured (JSON) reports | ☐ | ARC-204 |
| Attack-example dataset | ☐ | ARC-205 |
| CLI | ☐ | ARC-301 |
| Plugin API | ☐ | ARC-302 |
| Docs site | ☐ | ARC-303 |
| Build/packaging (Hatchling, PEP 621) | ✅ | ARC-003 |
| CI (ruff + build-import + pytest matrix + mypy) | ✅ | ARC-003/004 (mypy non-blocking) |
| Offline deterministic test suite | ✅ | ARC-004 — 18 passed, 2 xfailed, no network |
