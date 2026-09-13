# ARC-203 — Ground-truth corpus & generator

- **Season:** 2 — Ground Truth & the Detection Spec
- **Branch:** `arc/203-ground-truth-corpus` (off `main`)
- **Status:** ☐ not started
- **Depends on:** ARC-201 (merged, #10 — family IDs), ARC-202 (merged, #11 — `Finding`/`Span` shape
  this arc's manifest entries mirror). Nothing outstanding — **unblocked, can start unattended**
  for the planning/decision step below. Implementation itself must wait on D1–D3 sign-off
  (CLAUDE.md: "do not write code that depends on an un-accepted Type-1 decision").

## Goal

Build the labelled corpus that will grade every future detector, and the generator that produces
it — *before* any detector exists (ADR-011). "Done" means: a versioned JSONL manifest format that
ARC-204's evaluation harness and CI baseline can freeze against; a generator that deterministically
produces clean/attacked sample pairs for every text-level taxonomy family; and a benign corpus of
real multilingual and emoji-heavy text that a future detector must score zero findings against.
This is the arc that makes every later precision/recall claim (Season 3+) measurable instead of
anecdotal, and it is the literal gate CLAUDE.md rule 7 enforces before any detection family may
merge.

## In scope

- A JSONL manifest schema (D1) and a Python module that (de)serializes it, mirroring
  `phantomtext.core.report.Span`'s offset convention so a future detector's `Finding.span` can be
  diffed directly against a manifest entry's labelled span.
- A generator (`corpus/generate_corpus.py` + supporting modules under `corpus/`, **not** under
  `src/phantomtext/`) that deterministically produces, for **every family in `PT.INVIS.*` (8) and
  `PT.DECEIVE.*` (5)** — 13 families total:
  - one or more **positive** samples: a clean baseline string plus an attacked variant, with the
    injected span(s) labelled.
  - one or more **benign** samples per family: text that superficially resembles the attack surface
    (e.g. real ZWJ emoji sequences for `PT.INVIS.ZERO_WIDTH`, real Persian ZWNJ prose) but must not
    be flagged — the false-positive half CLAUDE.md rule 7 requires.
- A **benign multilingual corpus**, independent of any single family: real-text excerpts in
  Persian, Hindi, Arabic, Hebrew, Vietnamese, Chinese, and an emoji-heavy sample set, sourced and
  licensed per D3, that a future detector must score zero findings against as a standing smoke test.
- Determinism: fixed seeding, no network access anywhere in the generator (consistent with ADR-004's
  spirit even though ADR-004 itself scopes the *runtime library*, not tooling).
- Tests: manifest round-trip, generator output stability under a fixed seed, and a structural check
  that every in-scope family has at least one positive and one benign sample (this arc's own
  self-check of rule 7, ahead of any detector needing it).

## Out of scope

- **`PT.DOC.*` (8 families, document-level).** Generating "attacked" DOC samples means writing real
  HTML/DOCX/PDF files with format-specific hiding constructs (zero-size runs, `Tr 3`, OOXML
  `w:vanish`, XMP metadata, cmap remaps) — that needs the Loader/writer protocol ARC-401 builds
  (Season 4) and is naturally sequenced with ARC-405's format-native detectors, which will need
  fresh format-level corpus samples anyway. Picked up by **ARC-401/ARC-405**. This mirrors the
  taxonomy's own `text-level` vs `requires-format-parsing` split (`docs/spec/TAXONOMY.md`), so
  Season 3's text-level detector arcs (ARC-302, ARC-303) are fully unblocked by this arc without it.
- **The evaluation harness** (precision/recall/F1 computation, CI regression gate) — ARC-204,
  the very next arc, consumes this arc's manifest but is a distinct deliverable.
- **Any detector** — this arc produces labelled data only; nothing here scans anything (Season 3).
- **A public, first-class attack API** for the 8 families with no existing generator code (see
  DECISION-LOG) — the minimal generator functions this arc writes for them are private corpus-tooling, not
  the "first-class, public" obfuscation/injection surface ADR (ARC-502, Season 5) will ship. No
  behavioral promise is made to library users by this arc.
- **Growing the corpus's sample volume** beyond what makes the manifest schema and generator
  demonstrably correct — a modest fixed count per family (Type-2, logged), not an exhaustive fuzz
  corpus. Expanding it is cheap later and doesn't touch the schema.

## Decisions needed

| # | Decision | Tier | Notes |
|---|----------|:----:|-------|
| **D1** | JSONL manifest schema | **Type-1** | One JSON object per line: sample `id`, `family` (`PT.<CLASS>.<FAMILY>`, validated with the same regex `Finding.id` uses), `kind` (`"positive"` \| `"benign"`), `clean_text`, `attacked_text` (null for benign-only entries), `spans` (list of `{char_start, char_end}` in the injected/flagged region, empty for benign), `locale`/`script` tag where relevant, `source` (`"generated"` \| a citation for real-text benign samples), `generator_seed`. This is *the* format ARC-204's harness and CI baseline freeze against — flagged explicitly in `ROADMAP.md`'s ARC-203 entry as easy to mistake for Type-2. |
| **D2** | Corpus scope for this arc: 13 text-level families now, all 8 `PT.DOC.*` deferred to ARC-401/ARC-405 | **Type-1** | Changes what "the ground-truth corpus" delivers at Season 2's close and when Season 3's detector arcs can rely on rule 7's gate (immediately, for text-level) versus Season 4 (for document-level). Reversing this later means either backfilling DOC samples into this arc's manifest shape retroactively or accepting a second corpus-arc — cheap to defer now, more coordination to undo later. |
| **D3** | Benign multilingual corpus: source & license | **Type-1** | Universal Declaration of Human Rights official translations (Persian, Hindi, Arabic, Hebrew, Vietnamese, Chinese) plus hand-built emoji-ZWJ-sequence samples — short, stable, unambiguously reproducible text, vendored as static files under `corpus/`, fetched once by hand (not by the generator at any point) rather than pulled from a larger web-scraped multilingual dataset. Licensing is a Type-1 category per CLAUDE.md; a wrong call here means re-sourcing the one corpus every later detector's false-positive rate is measured against. |

**Three Type-1 rows — under the batching cap (ADR-010).** No fourth is needed; if review surfaces
one (e.g. disagreement with the D2 scope cut), it can be added without exceeding the cap of four.

## Acceptance criteria

- [ ] Manifest schema implemented per approved D1, with a loader/writer (round-trips JSONL → objects → JSONL)
- [ ] Generator produces, deterministically (fixed seed), at least one positive and one benign sample for
      all 13 in-scope families (`PT.INVIS.*` ×8, `PT.DECEIVE.*` ×5)
- [ ] Benign multilingual corpus present per approved D3 sourcing: Persian, Hindi, Arabic, Hebrew,
      Vietnamese, Chinese, plus an emoji-heavy sample set
- [ ] Every new family generator has both a positive and a benign sample (CLAUDE.md rule 7's own
      corpus obligation, self-checked by a test — no detector consumes this yet, but the corpus
      itself must not violate the rule it exists to satisfy)
- [ ] No network access anywhere in `corpus/` code (generator or tests)
- [ ] Tests pass offline & deterministically (`uv run --no-sync pytest`)
- [ ] `ruff check` / `ruff format --check` / `mypy src/phantomtext` clean (and `corpus/` if it's
      brought under the same lint/type config — Type-2, log the choice)
- [ ] `STATUS.md` — "Ground-truth corpus" row flips from ☐ to ✅, scoped explicitly to text-level
      families with a note pointing DOC-level coverage at ARC-401/ARC-405
- [ ] `HANDOFF.md` updated with a next task (ARC-204) that needs no maintainer action
- [ ] Type-2 decisions (module layout, legacy-code reuse per family, seeding scheme, sample volume)
      logged in `DECISION-LOG.md`

## Session log
- **2026-09-13** — Arc file drafted via `/arc-plan`. D1–D3 (Type-1) identified and proposed, not yet
  decided — next step is `/decide`.
- **2026-09-13** — D1–D3 approved as recommended via `/decide` — see
  [ADR-015](../../decisions/ADR-015-ground-truth-corpus.md). Implementation starting.
