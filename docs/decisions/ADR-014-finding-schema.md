# ADR-014 — Finding/Report schema, JSON wire shape, SARIF mapping, and severity/confidence model

- **Status:** Accepted (2026-09-11)
- **Deciders:** Luca (maintainer), assistant

## Context

ARC-202 needed to settle the `Finding`/`Report` data model before any detector, corpus manifest,
or evaluation baseline could be built against it. This absorbs **H2** from the superseded ARC-103
(ADR-009): a deliberately minimal `ScanReport` was rejected there specifically because it would be
outgrown within one season. Four decisions were gated as Type-1 per CLAUDE.md's explicit rule that
the `Finding`/report schema, and any serialized on-disk or on-wire format, are one-way doors —
ARC-203's corpus JSONL manifest and ARC-204's committed evaluation baseline both freeze against
whatever ships here.

## Decision (D1–D4)

- **D1 — Field set & offset-unit convention.** `Finding` carries: `id` (family ID, `PT.<CLASS>.
  <FAMILY>` per ADR-013), `severity`, `confidence`, `span` (`char_start`/`char_end` as the primary,
  authoritative offsets — Python codepoint indices, consistent with the string-first core, ADR-002
  — plus optional `utf16_start`/`utf16_end` for SARIF/editor-tooling interop, since JS string
  indices are UTF-16 code units and Python's are not), `message`, `provenance` (minimal and
  extensible: `source_kind: "string"|"html"|"docx"|"pdf"` plus optional `page`/`node`/`run`,
  richer population deferred to ARC-401's Loader protocol), and `remediation`. `Report` wraps an
  ordered list of `Finding`s plus `schema_version`.
- **D2 — JSON wire shape & versioning.** snake_case keys, 1:1 with the Python field names — no
  translation layer. `schema_version: "1.0"` at the `Report` top level; bump the minor version for
  additive (new optional field) changes, the major version for anything that could break an
  existing consumer (renamed/removed/retyped field). `None`-valued optional fields are omitted
  from serialized output, not emitted as explicit nulls.
- **D3 — SARIF 2.1.0 export mapping.** `ruleId` ← family `id` verbatim (e.g.
  `PT.INVIS.TAG_CHARS`). `level` ← severity, mapped onto SARIF's `error`/`warning`/`note`/`none`
  enum (Critical and High both map to `error`, since SARIF has no fourth slot), with the original
  4-level value preserved losslessly in `properties.phantomtext_severity` for tools that
  understand it. `locations[0].physicalLocation.region` ← `span` (`char_start`/`char_end` as
  `charOffset`/`charLength`).
- **D4 — Severity vs. confidence model.** Two independent fields, not one collapsed score.
  `severity` is the family's impact-if-true-positive (defaults from `docs/spec/TAXONOMY.md`,
  overridable per `Finding`). `confidence` is a continuous `float` in `[0.0, 1.0]` — this detector
  instance's certainty on this specific span. Continuous, not a small ordinal scale, so ARC-204
  can threshold-sweep for a real precision/recall curve.

Three Type-2 decisions were made alongside these and logged in `DECISION-LOG.md` rather than
gated here: the schema lives in `src/phantomtext/core/report.py`; it's implemented as a frozen,
slotted stdlib `dataclass` rather than adding a validation library (pydantic) as a new
dependency; and the family-`id` field is validated by a regex format check, not a generated
enum, since the taxonomy doc is hand-written Markdown, not a machine-readable source yet.

## Consequences

- ARC-203's corpus manifest and ARC-204's evaluation harness now have a fixed target to build
  against; both can proceed without guessing at structure.
- SARIF output is spec-conformant for any generic consumer (GitHub code scanning, IDEs) while
  staying full-fidelity for PhantomText-aware tooling via `properties.phantomtext_severity`.
- The confidence field makes ARC-204's precision/recall math and ARC-304's policy overrides
  (e.g. "suppress low-confidence findings" independent of "only escalate High+ severity")
  expressible as independent axes from day one, rather than needing a breaking split later.
- The `utf16_start`/`utf16_end` fields are dead weight until something actually consumes them
  (SARIF export, or an editor integration) — acceptable cost for avoiding a later breaking change
  to the span shape.
- `provenance`'s document-structure fields (page/node/run) stay unpopulated until ARC-401 exists;
  any Finding produced before then only fills `source_kind`.

## Alternatives considered

- **Codepoint offsets only, no UTF-16 companion (D1).** Rejected: SARIF and most editor tooling
  are UTF-16-indexed; adding the companion fields now is cheaper than a breaking span-shape change
  once SARIF export (D3) and an eventual editor integration (ARC-604) both depend on it.
- **camelCase JSON keys (D2).** Rejected: no external consumer exists yet that would benefit, and
  1:1 snake_case keeps serialization a straight `dataclasses.asdict()` with no translation layer
  to maintain or test.
- **A single collapsed `score` field instead of severity+confidence (D4).** Rejected: it cannot
  express "only alert on High+ severity regardless of confidence" or "surface low-confidence
  Criticals for manual review" as independent policy statements, which ARC-304 will need.
- **An ordinal confidence scale (low/medium/high) instead of continuous (D4).** Rejected: loses
  the ability to threshold-sweep for a precision/recall curve in ARC-204, which is the whole point
  of having a confidence field distinct from severity.
