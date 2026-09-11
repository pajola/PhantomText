# Decision Log

## Part 1 — ADR index (Type-1 decisions)

One-way doors. Every one is an Architecture Decision Record requiring maintainer sign-off. Status values:
**Proposed** (awaiting maintainer) · **Accepted** · **Rejected** · **Superseded by ADR-xxx**.

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [001](ADR-001-src-layout.md) | `src/` repository layout | Accepted | 2026-08-03 |
| [002](ADR-002-string-first-api.md) | String-first core API | Accepted | 2026-08-03 |
| [003](ADR-003-build-tooling.md) | uv + PEP 621 build & tooling | Accepted | 2026-08-03 |
| [004](ADR-004-dependencies.md) | Batteries-included dependencies | Accepted | 2026-08-03 |
| [005](ADR-005-arc-workflow.md) | Per-arc branches & PRs | Accepted (amended by 010) | 2026-08-03 |
| [006](ADR-006-build-backend.md) | Build backend: Hatchling | Accepted | 2026-08-04 |
| [007](ADR-007-attack-base-hierarchy.md) | Attack base-class hierarchy | Accepted | 2026-08-04 |
| [008](ADR-008-offline-homoglyph-data.md) | Offline homoglyph data | Accepted | 2026-08-05 |
| [009](ADR-009-supersede-arc-103.md) | Supersede ARC-103 (string-first public API) | Accepted | 2026-09-10 |
| [010](ADR-010-tiered-decisions.md) | Tiered decisions, unblocked handoffs, review-queue cap | Accepted | 2026-09-10 |
| [011](ADR-011-detection-first-ground-truth.md) | Detection-first roadmap; no detector without ground truth | Accepted | 2026-09-10 |
| [012](ADR-012-clean-room-core.md) | Clean-room rewrite of the core | Accepted | 2026-09-10 |
| [013](ADR-013-family-id-naming-scheme.md) | Taxonomy family ID naming scheme (`PT.<CLASS>.<FAMILY>`) | Accepted | 2026-09-11 |

## Part 2 — Type-2 log (two-way doors)

Reversible decisions the assistant made without a sign-off gate, per ADR-010. One line each, newest last.
The maintainer may veto any of these at PR review — that is the intended safety net.

Format: `YYYY-MM-DD — [T2] <decision> — <one-line rationale>`

- 2026-09-10 — [T2] Season numbering continues from 2 rather than restarting after the re-cut — keeps the ADR trail and PR history legible against the roadmap.
- 2026-09-10 — [T2] The 0.1 audit bug list is carried in HANDOFF as prospective corpus samples rather than as an open bug list — under ADR-012 the code they describe will not exist.
- 2026-09-11 — [T2] ARC-201 taxonomy is a hand-written Markdown doc (`docs/spec/TAXONOMY.md`) with a fixed per-entry field structure, not YAML + generated docs — the arc is explicitly no-code/no-detectors, and a consistently-structured Markdown entry converts trivially to YAML later if ARC-301's registry needs it.
- 2026-09-11 — [T2] Default severity scale is 4-level (Critical/High/Medium/Low) — maps cleanly onto SARIF's error/warning/note bucketing (plus none for suppressed) and gives ARC-304's per-family policy overrides enough granularity across dozens of families without overloading a 3-level scale.
- 2026-09-11 — [T2] Mixed-script restriction levels follow UTS #39 verbatim (ASCII-Only … Unrestricted) rather than a PhantomText subset — keeps the taxonomy citation-grounded; any user-facing simplification belongs in ARC-304's policy layer, not in the taxonomy definitions.
- 2026-09-11 — [T2] `PT.DOC.*` is enumerated as 16 family IDs against the arc's 8 scope bullets (vs. the ~1:1 mapping used for `PT.INVIS.*`/`PT.DECEIVE.*`) — several bullets (HTML hidden-node techniques, metadata channels) bundle mechanisms with materially different legitimacy and severity profiles that a single family would flatten. Flagged prominently in `TAXONOMY.md`'s scope note for maintainer veto at PR review, per ADR-010's safety net.
