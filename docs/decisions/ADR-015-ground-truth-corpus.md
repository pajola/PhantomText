# ADR-015 — Ground-truth corpus manifest, scope, and benign-corpus sourcing

- **Status:** Accepted (2026-09-13)
- **Deciders:** Luca (maintainer), assistant

## Context

ARC-203 needs to produce the labelled corpus that ARC-204's evaluation harness and every Season 3+
detector's CI regression gate will be built against (ADR-011: no detector without ground truth).
Three one-way doors had to be settled before implementation: the on-disk manifest shape, how much
of the 21-family taxonomy this arc covers, and where the benign multilingual corpus's real text
comes from.

## Decision

### D1 — Manifest shape

One JSON object per line (JSONL). Fields: `id`, `family` (`PT.<CLASS>.<FAMILY>`, same regex as
`phantomtext.core.report.Finding.id`), `kind` (`"positive"` | `"benign"`), `clean_text`,
`attacked_text` (null for benign entries), `spans` (list of `{char_start, char_end}`, mirroring
`Span`'s offset convention; empty for benign), `locale`/`script` where relevant, `source`
(`"generated"` or a citation for real-text benign samples), `generator_seed`.

A corpus entry is a *label*, not a detection result — it is deliberately **not** a serialized
`Finding`/`Report`, so the corpus's frozen baseline shape does not couple to `Finding`'s own future
evolution (detector-output concerns: new provenance fields, confidence-model changes, etc.).

### D2 — Scope: 13 text-level families now, `PT.DOC.*` deferred

This arc covers all of `PT.INVIS.*` (8) and `PT.DECEIVE.*` (5) — 13 families. The 8 `PT.DOC.*`
families are **out of scope**, picked up by ARC-401 (Loader/writer protocol) and ARC-405
(format-native detections) in Season 4, since a real attacked HTML/DOCX/PDF sample needs a format
writer that does not exist yet. This mirrors the taxonomy's own `text-level` vs
`requires-format-parsing` split and fully unblocks Season 3's text-level detector arcs (ARC-302,
ARC-303) under CLAUDE.md rule 7 without waiting on Season 4.

### D3 — Benign multilingual corpus: source & licensing

Official UDHR (Universal Declaration of Human Rights) translations — Persian, Hindi, Arabic,
Hebrew, Vietnamese, Chinese — plus hand-built emoji-ZWJ-sequence samples, vendored as static files
under `corpus/benign/`, fetched once by hand and committed. The generator never fetches anything at
runtime (consistent with ADR-004's offline spirit, even though ADR-004 itself scopes the runtime
library rather than tooling).

## Consequences

- ARC-204's harness and CI baseline read a manifest format that is stable independent of any future
  `Finding` schema change.
- `STATUS.md`'s "Ground-truth corpus" row will read as partial (text-level only) until ARC-401/
  ARC-405 backfill `PT.DOC.*` coverage — an explicit, tracked gap, not a silent one.
- Every Season 3+ detector's false-positive rate is measured against the UDHR-sourced benign corpus;
  changing that source later means re-running every family's false-positive numbers, though it does
  not touch the manifest schema itself.

## Alternatives considered

- **D1 — reuse `Finding`/`Report` as the corpus's on-disk shape.** Rejected: conflates a label with
  a detection result, coupling the frozen corpus baseline to future detector-output schema changes.
- **D2 — build minimal ad-hoc HTML/DOCX/PDF writers now to cover all 21 families in this arc.**
  Rejected: throwaway format-writing code in exactly the area ADR-012 is protecting from premature,
  soon-to-be-replaced implementation; would also push this arc past a single session.
- **D3 — a larger scraped multilingual dataset (e.g. OSCAR/CC-100 excerpts).** Rejected: licensing
  ambiguity and unnecessary size for what is meant to be a small, stable false-positive smoke
  corpus, not a representative sample of natural language at scale.
