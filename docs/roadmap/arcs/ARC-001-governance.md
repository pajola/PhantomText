# ARC-001 — Governance scaffold

- **Season:** 0
- **Branch:** `arc/001-governance`
- **Status:** ◐ in progress (awaiting maintainer review)
- **Depends on:** —

## Goal
Stand up the session-handoff machinery and record the foundational decisions, so every subsequent arc has a
clear, self-onboarding structure and a decision trail. No product code changes.

## In scope
- `CLAUDE.md` (session onboarding + working rules)
- `docs/roadmap/{ROADMAP,STATUS,HANDOFF}.md` + arc template
- `docs/decisions/{DECISION-LOG.md, ADR-001…005}`

## Out of scope
- Any change to `phantomtext/` source (that starts in ARC-002)

## Acceptance criteria
- [x] Governance docs written
- [x] ADR-001…005 recorded as Accepted
- [ ] Maintainer reviews & approves the PR
- [ ] Merged to `main`

## Decisions needed
- Resolved: ADR-001 (src layout), ADR-002 (string-first API), ADR-003 (build/tooling), ADR-004 (batteries-included
  deps), ADR-005 (per-arc PR workflow).

## Session log
- 2026-08-03 — Audited 0.1.1, agreed direction, cloned repo, wrote scaffold + ADRs on `arc/001-governance`.
