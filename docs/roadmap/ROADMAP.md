# PhantomText Roadmap — Seasons & Arcs

The project is delivered in **Seasons** (multi-week themed milestones) made of **Arcs** (single-session,
independently-reviewable units of work). Each arc is one branch and one PR. This file is the big picture;
`STATUS.md` tracks implemented-vs-not; `HANDOFF.md` tracks live state.

**Positioning:** a production security library whose product is a **detector** — it tells a user, fast and
under their configuration, that a piece of text or a document contains invisible or deceiving characters.
The attack families are first-class peers, and they are also the ground truth the detector is graded on.

**Re-cut on 2026-09-10** (ADR-009 / ADR-011 / ADR-012). Seasons 0 and 1 are preserved as history; Season 1
was closed early with two arcs delivered and four superseded. Numbering continues rather than restarting, so
the ADR trail stays honest.

Legend: ☐ not started · ◐ in progress · ☑ done · ⊘ superseded

---

## Season 0 — Foundation & Governance ☑ *(complete, 2026-08-04)*
**Goal:** a clean, trustworthy skeleton preserving the working core with no behavior changes.

- ☑ **ARC-001 — Governance scaffold** — ROADMAP, STATUS, HANDOFF, CLAUDE.md, ADR-001…005. *(#1)*
- ☑ **ARC-002 — Repo hygiene** — `src/` layout; quarantine dead files; `.gitignore`. *(#3)*
- ☑ **ARC-003 — Build & tooling** — Hatchling + PEP 621; ruff/mypy/pytest; CI; pre-commit. *(#4)*
- ☑ **ARC-004 — Deterministic offline test baseline** — 21 passed, 2 xfailed, no network. *(#5)*

## Season 1 — Core API Consolidation ⊘ *(closed early, 2026-09-10)*
**Delivered:** the two arcs that turned out to be foundational regardless of what came next.
**Superseded:** everything that existed only to retrofit an API onto the 0.1 internals, now that the core is
being rewritten clean-room (ADR-012).

- ☑ **ARC-101 — Unify `AttackBase`** — `core/base.py`; all 8 techniques migrated. *(#6)*
- ☑ **ARC-102 — Vendor Unicode data offline** — UTS#39 table in-package; `requests` dropped. *(#7)*
- ⊘ **ARC-103 — String-first public API** — superseded by ADR-009. Decisions **H1** (functions vs classes),
  **H3** (canonical technique names) and **H6** (registry) carried forward to ARC-301. H2 and H7 absorbed into
  ARC-202/ARC-304; H4 and H5 dead; H8 already settled by ADR-002.
- ⊘ **ARC-104 — Format layer** — superseded; becomes Season 4.
- ⊘ **ARC-105 — Correctness fixes** — moot under a clean-room rewrite; the bugs are documented in the audit
  and become corpus test cases instead.
- ⊘ **ARC-106 — Batch API** — superseded; becomes ARC-602.

---

## Season 2 — Ground Truth & the Detection Spec
**Goal:** define exactly what counts as "invisible" or "deceiving", and build the labelled corpus that can
grade any detector — *before* a detector exists. This is the season that makes every later claim measurable.
**Exit:** a spec, a corpus, and a harness that emits precision/recall per family. Zero detectors written.

- ☑ **ARC-201 — Threat taxonomy** *(2026-09-11, #10)* — enumerate every family with a stable ID, a precise definition, canonical
  examples, and a **legitimate-use note**. The invisible half: `Cf` format characters, zero-width
  (ZWSP/ZWNJ/ZWJ), bidi controls (LRO/RLO/PDF/isolates), the Tags block (U+E0000–E007F), variation selectors
  (U+FE00–FE0F, U+E0100+), whitespace substitution, soft hyphen. The deceiving half: UTS#39 confusables,
  mixed-script strings, combining-mark stacking. Document-level: zero-size font, transparent text,
  out-of-bound placement, colour camouflage, CSS-hidden nodes, metadata channels.
  *The legitimate-use note is the point of this arc:* ZWJ in emoji sequences and Devanagari, ZWNJ in Persian,
  RTL marks in Arabic and Hebrew, combining marks in Vietnamese — a detector that flags these is not a
  security tool, it is a nuisance.
- ☐ **ARC-202 — Finding schema & severity model** *(absorbs H2)* — codepoint span, char/byte offsets, family
  ID, severity, confidence, provenance (page / node / run), suggested remediation. JSON and SARIF shapes.
  **Type-1** — this is a serialized format users will pin CI baselines to.
- ☐ **ARC-203 — Ground-truth corpus & generator** — clean/attacked pairs across family × format with a JSONL
  manifest. Must include a **benign corpus**: real multilingual text (Persian, Hindi, Arabic, Hebrew,
  Vietnamese, Chinese, emoji-heavy) that must yield zero findings. False positives are the failure mode that
  makes a tool like this get uninstalled.
- ☐ **ARC-204 — Evaluation harness** — `python -m phantomtext.eval`: precision / recall / F1 per family, per
  format; a committed baseline; a CI gate that fails on regression.

## Season 3 — The Detection Core (clean-room)
**Goal:** the detector itself, written against the Season 2 spec and graded by the Season 2 harness.
**Exit:** text-level detection meets an agreed precision/recall bar on the corpus. `0.2.0`.

- ☐ **ARC-301 — Core architecture & registry** *(absorbs H1, H3, H6)* — public verbs, technique registry keyed
  by family ID, and the `Backend` protocol that isolates the scanning kernel. **Type-1** (public API shape).
- ☐ **ARC-302 — Invisible-character detectors** — the `Cf` / zero-width / bidi / Tags / variation-selector /
  whitespace families.
- ☐ **ARC-303 — Confusable & mixed-script detection** — the genuinely hard half: UTS#39 skeleton mapping,
  script resolution, and a scoring model that survives the benign corpus.
- ☐ **ARC-304 — Configuration & policy** *(absorbs H7)* — profiles (`strict` / `balanced` / `permissive`),
  per-family severity overrides, script and language allowlists, config-file discovery and precedence.
  This is the "configuration" half of the product goal.
- ☐ **ARC-305 — Benchmark harness & the backend decision** — measure the kernel against realistic inputs,
  then decide Python-only vs a Rust (PyO3) backend **on the numbers**, recorded as an ADR. The `Backend`
  protocol from ARC-301 is what makes this a swap rather than a rewrite.

## Season 4 — Formats
**Goal:** a finding must point at a place a human can act on, in every supported format.
**Exit:** provenance-accurate detection across txt / html / docx / pdf.

- ☐ **ARC-401 — Loader protocol & provenance** — text extraction that carries an offset → (page, node, run)
  mapping, so a finding round-trips to a location.
- ☐ **ARC-402 — HTML** · ☐ **ARC-403 — DOCX** · ☐ **ARC-404 — PDF**
- ☐ **ARC-405 — Format-native detections** — zero-size font, transparency, off-page placement, colour
  camouflage, `display:none` / `visibility:hidden` / `aria-hidden` / off-screen, HTML comments, CSS
  `content:`, and the metadata channels (XMP, DOCX core properties, comments, tracked changes,
  headers/footers, alt-text, PDF annotations and OCG layers).

## Season 5 — Sanitization & Round-Trip Parity
**Goal:** close the loop. Every attack the library can perform, it can detect and undo.
**Exit:** verified attack ↔ defense round-trip for every implemented family.

- ☐ **ARC-501 — Sanitizer** — driven by the same policy object as the scanner; never two sources of truth.
- ☐ **ARC-502 — Attack engine, clean-room** — obfuscation and injection rebuilt on the shared taxonomy,
  first-class and public, plus the families the 0.1 code never had (Tags block, variation selectors,
  font poisoning via cmap remap, whitespace substitution).
- ☐ **ARC-503 — Property-based round-trip tests** — inject → scan must detect; sanitize → scan must be clean;
  sanitize must be idempotent; sanitize must not alter the benign corpus. Hypothesis-driven.

## Season 6 — Product Surfaces
**Goal:** reachable by practitioners, and fast enough that they leave it switched on. **Exit:** `1.0-rc`.

- ☐ **ARC-601 — CLI** — `phantomtext scan|sanitize|inject|obfuscate|corpus`; exit codes for CI; JSON and SARIF
  output; a terminal renderer that makes invisible characters visible.
- ☐ **ARC-602 — Throughput & daemon mode** *(absorbs ARC-106)* — parallel file dispatch, streaming/chunking
  for large inputs, and a persistent process so the editor extension never pays Python start-up.
- ☐ **ARC-603 — Stable typed Python API & docs site** — mkdocs-Material: guides, API reference, threat model,
  ethical-use policy.
- ☐ **ARC-604 — VS Code extension** — live highlighting over the ARC-602 daemon.
- ☐ **ARC-605 — Browser extension** — stretch; same daemon contract, different host.

## Season 7 — Release & Research Artifact
**Goal:** sustainable open source and a defensible paper artifact. **Exit:** `1.0.0`.

- ☐ **ARC-701 — Community docs** — CONTRIBUTING, CODE_OF_CONDUCT, SECURITY.md, issue/PR templates.
- ☐ **ARC-702 — Release automation** — PyPI trusted publishing, changelog, semver policy, tagged releases.
- ☐ **ARC-703 — Research-repo split** — paper-reproduction artifacts to a separate repo; cross-link; `v0.1.1`
  stays tagged here as the AISec'25 artifact.
- ☐ **ARC-704 — 1.0.0** — final API review, docs freeze, release.

---

## Why detection moved ahead of the attack engine

The original roadmap put the attack engine in Season 1 and detection in Season 2, which mirrors how the paper
was written. The product is the other way round: the reason someone installs this library is to find hidden
characters, not to plant them. Attacks stay first-class — they are how the detector is graded, and Season 5
rebuilds them in full — but the corpus and the spec have to exist before either half can be trusted, and a
corpus is useful to the detector immediately and to the attack engine only later.
