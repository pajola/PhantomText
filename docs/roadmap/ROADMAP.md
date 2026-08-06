# PhantomText Roadmap — Seasons & Arcs

The project is delivered in **Seasons** (multi-week themed milestones) made of **Arcs** (single-session,
independently-reviewable units of work). Each arc is one branch and one PR. This file is the big picture;
`STATUS.md` tracks implemented-vs-not; `HANDOFF.md` tracks live state.

Positioning: **production security library**. Research/paper-reproduction artifacts will be split into a
separate repo in Season 4.

Legend: ☐ not started · ◐ in progress · ☑ done

---

## Season 0 — Foundation & Governance
**Goal:** a clean, trustworthy skeleton that preserves the working core with *no behavior changes*, plus the
handoff machinery. **Exit:** `uv sync` clean, CI green, docs skeleton live, everything that worked still works.

- ☑ **ARC-001 — Governance scaffold** — ROADMAP, STATUS, HANDOFF, CLAUDE.md, ADR-001…005. *(merged, #1)*
- ☑ **ARC-002 — Repo hygiene** — adopt `src/` layout; quarantine dead files; `.gitignore`. *(merged, #3)*
- ◐ **ARC-003 — Build & tooling** — Hatchling + single PEP 621 `pyproject.toml`; delete `setup.py`,
  `requirements.txt`, `build_package.sh`, `MANIFEST.in`; single-source version; metadata fixes; ruff + mypy +
  pytest; GitHub Actions CI (lint + build/import matrix); pre-commit. *(done, awaiting review)*
- ◐ **ARC-004 — Deterministic offline test baseline** — pin behavior of the working core with tests that never
  touch the network and are RNG-seeded; pytest + mypy CI jobs. *(done, awaiting review — closes Season 0)*

## Season 1 — Core API Consolidation (Attack Engine v1)
**Goal:** one coherent, typed, stable public API; kill the duplicate/stub façades. **Exit:** `0.2.0` + migration guide.

- ◐ **ARC-101 — Unify `AttackBase`** — `core/base.py`: `Attack` root + `ObfuscationAttack` + `InjectionAttack`;
  migrated all 8 techniques; `sanitized`→`sanitize` (aliased); honest injection `check()` stubs. *(done, awaiting review)*
- ◐ **ARC-102 — Vendor Unicode data offline** — homoglyph/confusables table shipped in-package (offline, cached);
  removed the runtime `requests.get`; **dropped `requests`**; added a refresh tool. *(done, awaiting review — library now fully offline)*
- ☐ **ARC-103 — String-first public API** — `scan / obfuscate / inject / sanitize` on `str`; file layer wraps it;
  deprecation shims for 0.1's `ContentObfuscator` / `ContentInjector` / `FileScanner`.
- ☐ **ARC-104 — Format layer (4 formats)** — first-class `txt` + `html` + `docx` + `pdf`; dedupe copy-paste;
  robust target-replacement semantics.
- ☐ **ARC-105 — Correctness fixes** — RNG off-by-one, replace-all vs first-match, coordinate/default handling.
- ☐ **ARC-106 — Batch API** — single-input and batch-over-files/dirs; parallel worker pool; aggregated report;
  deterministic (seeded) mode.

## Season 2 — Detection, Policy & Sanitization (the defensive half)
**Goal:** make scan + sanitize real, symmetric with the attacks, and policy-driven. **Exit:** verified
attack↔defense round-trip for every implemented family.

- ☐ **ARC-201 — SecurityPolicy / profiles** — one declarative policy (severity thresholds, e.g. font-size <4 =
  violation) consumed by *both* scanner and sanitizer; presets `strict / balanced / permissive`.
- ☐ **ARC-202 — Injection detection** — implement `check()` for injection families across formats.
- ☐ **ARC-203 — FileSanitizer** — real implementation; attack→scan→sanitize→verify-clean round-trip.
- ☐ **ARC-204 — Structured reports** — machine-readable (JSON) findings with severity; drop `print`.
- ☐ **ARC-205 — Attack-example dataset** — generator (`phantomtext dataset build`) emitting labeled clean+attacked
  samples across technique × modality × format, with a JSONL ground-truth manifest; ship generator + small sample.

## Season 3 — Productization & DX
**Goal:** usable by practitioners. **Exit:** `1.0-rc`.

- ☐ **ARC-301 — CLI** — `phantomtext scan|obfuscate|inject|sanitize|dataset`.
- ☐ **ARC-302 — Plugin API** — register third-party attack families via entry points.
- ☐ **ARC-303 — Docs site** — mkdocs-Material: guides, API reference, threat model, ethical-use policy.
- ☐ **ARC-304 — Performance & large files** — streaming/chunking, benchmarks.

## Season 4 — OSS Hardening & Release
**Goal:** sustainable open source. **Exit:** `1.0.0`.

- ☐ **ARC-401 — Community docs** — CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.md, issue/PR templates.
- ☐ **ARC-402 — Release automation** — PyPI trusted publishing, changelog, semver policy, tagged releases.
- ☐ **ARC-403 — Research-repo split** — move paper-reproduction artifacts to a separate repo; cross-link.
- ☐ **ARC-404 — 1.0.0** — final API review, docs freeze, release.

---

## New-attack backlog (to slot into S1/S2, adopt-all-relevant)
Headline: **Unicode Tags block (U+E0000–E007F)**, **variation selectors (U+FE00–FE0F / U+E0100+)**,
**font poisoning (cmap remap)**. Also: whitespace substitution, soft hyphen / conditional format chars,
full Unicode confusables, OCR-vs-text-layer mismatch, metadata & non-body channels (XMP, DOCX properties,
comments, tracked changes, headers/footers, alt-text, PDF annotations/OCG layers), HTML hidden channels
(`display:none`, `visibility:hidden`, `aria-hidden`, off-screen, comments, CSS `content:`).
