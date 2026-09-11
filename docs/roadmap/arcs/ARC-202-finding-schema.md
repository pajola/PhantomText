# ARC-202 — Finding schema & severity model

- **Season:** 2 — Ground Truth & the Detection Spec
- **Branch:** `arc/202-finding-schema` (off `main`)
- **Status:** ☐ not started — D1–D4 approved as recommended ([ADR-014](../../decisions/ADR-014-finding-schema.md)); implementation not yet started
- **Depends on:** ARC-201 (merged, #10 — supplies the family IDs this schema references). Fully
  unblocked — branch and implement.

## Goal

Define, and implement as a pure data model (no detector logic), the `Finding`/`Report` schema:
the structure every future detector (Season 3+) will emit, every corpus manifest (ARC-203) and
evaluation baseline (ARC-204) will be built against, and every export format (JSON, SARIF —
ARC-601's CLI output) will serialize. This is the arc that turns "we have a taxonomy" into
"we have something a detector can return and a CI pipeline can consume." Nothing here scans
anything; `Finding` instances in tests are hand-built fixtures, not detector output.

This absorbs **H2** from the superseded ARC-103 (ADR-009): a *deliberately minimal* `ScanReport`
was rejected there specifically because it would be outgrown within one season — ARC-202 is where
it becomes a first-class, durable deliverable instead.

## In scope

- `Finding` fields: family `id` (references the `PT.<CLASS>.<FAMILY>` IDs fixed by ADR-013 and
  enumerated in `docs/spec/TAXONOMY.md`), `severity`, `confidence`, a `span` (character-offset
  start/end at minimum), a human-readable `message`, a minimal/extensible `provenance` slot, and
  `remediation` guidance text.
- `Report` container: an ordered collection of `Finding`s plus a `schema_version` and whatever
  top-level metadata the JSON shape decision (D2) requires.
- JSON serialization (round-trippable) and a SARIF 2.1.0 export mapping.
- The severity scale is **already fixed** (4-level Critical/High/Medium/Low, DECISION-LOG
  2026-09-11) — this arc wires it into the schema, it does not re-derive it.
- Basic structural validation of the family-`id` field's shape (it looks like a
  `PT.<CLASS>.<FAMILY>` string) — not a full lookup against the taxonomy doc, which would need a
  generated data file this arc doesn't build.

## Out of scope

- **Any detector that produces a real `Finding`** — Season 3 (ARC-301+). This arc's tests use
  hand-built fixtures.
- **Populating `provenance`'s document-structure fields** (page/node/run) for real files — needs
  the Loader protocol (ARC-401, Season 4). ARC-202 defines the *shape* (a `source_kind` string
  plus optional structured fields) as an extension point, not the extraction logic.
- **Severity *overrides* / per-family policy thresholds** — ARC-304 (this is where the superseded
  ARC-103's **H7** actually landed, per ADR-009; ARC-202 defines what severity *is* as a field,
  not how a `strict`/`balanced`/`permissive` profile changes it).
- **CLI wiring that prints JSON/SARIF** — ARC-601. This arc defines the serialization functions;
  a command-line surface for them is later.
- **The ground-truth corpus's own JSONL manifest shape** — ARC-203. That format will *contain*
  `Finding`-shaped data but is a distinct deliverable with its own clean/attacked-pair structure.
- **Any change to the taxonomy itself** — ARC-201 is merged and closed; this arc references family
  IDs, it does not redefine them.

## Decisions needed

| # | Decision | Tier | Notes |
|---|----------|:----:|-------|
| **D1** | `Finding` field set & offset-unit convention | **Type-1** | Fields: `id` (family ID), `severity`, `confidence`, `span` (Python codepoint-index start/end; optional `utf16_offset` for JS/SARIF-tooling interop, since JS string indices are UTF-16 code units and Python's are not), `message`, `provenance` (minimal — `source_kind: "string"\|"html"\|"docx"\|"pdf"` plus optional page/node/run, richer shape deferred to ARC-401), `remediation`. This is *the* schema CLAUDE.md names explicitly as Type-1. |
| **D2** | JSON wire shape & versioning | **Type-1** | Key casing (snake_case, matching the Python field names), a `schema_version` field and what bumping it means, null-omission rule for optional fields. ARC-203's corpus manifest and ARC-204's committed baseline both freeze against whatever this arc ships — changing it later means rewriting both. |
| **D3** | SARIF 2.1.0 export mapping | **Type-1** | `ruleId` ← family `id`; `level` ← severity, mapped onto SARIF's `error`/`warning`/`note`/`none` (lossy from 4 levels to effectively 3+1 — needs an explicit, documented mapping table, not an implicit one); `locations[].physicalLocation.region` ← `span`. SARIF is an external standard consumed directly by GitHub code scanning and other CI tooling (ARC-601) — a wrong mapping surfaces as broken CI integrations, not a local bug. |
| **D4** | Severity vs. confidence model | **Type-1** | Two independent axes — severity = impact if this is a true positive (a property of the *family*, TAXONOMY.md already sets defaults per family), confidence = this detector instance's certainty on this specific span (continuous `[0,1]` or a small ordinal scale) — versus one collapsed score. Drives ARC-204's precision/recall math (do we threshold on confidence before computing precision/recall, or not?) and ARC-304's override semantics (does a policy override severity, confidence, or both?). Expensive to un-collapse later once a baseline and policy model exist on top of it. |
| D5 | Module location (e.g. `core/report.py`) | Type-2 | Internal layout, freely revisable. |
| D6 | Implementation: stdlib `@dataclass` vs. a validation library (e.g. pydantic) | Type-2 | Default to a frozen, slotted stdlib `dataclass` — adding pydantic would itself be a new runtime dependency, which is Type-1 under CLAUDE.md's dependency rule; sidestep that gate by not adding one unless dataclasses genuinely can't do the job. |
| D7 | Family-`id` validation mechanism (regex vs. a generated literal/enum from `TAXONOMY.md`) | Type-2 | Behind the stable field from D1; swappable later without touching the wire format. A regex format check (`PT\.[A-Z]+\.[A-Z_]+`) is enough for this arc — a generated enum is a nice-to-have for a later arc once the taxonomy has a machine-readable form (T2 from ARC-201 flagged Markdown-vs-YAML for exactly this reason). |

**Four Type-1 rows — at the batching cap (ADR-010).** If review surfaces a fifth one-way door
(e.g. someone argues `remediation` text needs its own versioned template system), split it into a
follow-up arc rather than adding a fifth row here.

## Acceptance criteria

- [ ] `Finding` and `Report` implemented per the approved D1/D5/D6 shape
- [ ] Family `id` field validated per the approved D7 mechanism
- [ ] JSON serialization round-trips (`Finding`/`Report` → JSON → back), matching the approved D2 shape, including `schema_version`
- [ ] SARIF export produces valid SARIF 2.1.0 output for at least one hand-built `Finding`, per the approved D3 mapping
- [ ] Severity and confidence are modeled as two fields per the approved D4 shape, not collapsed
- [ ] Unit tests cover: field validation (good and malformed family IDs), JSON round-trip, SARIF shape, at least one hand-built benign-context and one hand-built positive-context `Finding` fixture
- [ ] `pytest` green offline & deterministic; `ruff check`/`ruff format --check`/`mypy src/phantomtext` clean
- [ ] `STATUS.md` updated — "Finding schema" row flips from ☐ to ✅
- [ ] `HANDOFF.md` updated, pointing at ARC-203 as the next unblocked task
- [x] Type-2 decisions D5–D7 logged in `DECISION-LOG.md`; any made during implementation to be added

## Session log
- **2026-09-11** — Arc file drafted via `/arc-plan`. D5–D7 (Type-2) decided and logged. D1–D4
  (Type-1) proposed via `/decide` and approved as recommended — see
  [ADR-014](../../decisions/ADR-014-finding-schema.md). Implementation not yet started.
