# ADR-009 — Supersede ARC-103 (string-first public API)

- **Status:** Accepted (2026-09-10)
- **Deciders:** Luca (maintainer), assistant
- **Supersedes:** ARC-103 plan of 2026-08-05

## Context

ARC-103 was drafted to retrofit a clean string-first public API onto the 0.1 internals, keeping the 0.1 facade
classes (`ContentObfuscator`, `ContentInjector`, `FileScanner`, `FileSanitizer`) alive as deprecation shims.
It carried eight decisions, H1–H8, awaiting maintainer sign-off. None were signed off, and the project stopped
for five weeks (see ADR-010 for the process cause).

ADR-012 now adopts a clean-room rewrite of the core. That invalidates ARC-103's premise: there are no 0.1
internals to retrofit, and no reason to preserve 0.1 class names through a break the tagged `v0.1.1` release
already covers.

## Decision

**ARC-103 is closed as superseded.** Its decisions are dispositioned individually rather than discarded:

| # | Decision | Disposition |
|---|----------|-------------|
| H1 | Top-level functions vs technique classes | **Carried forward** to ARC-301 — still a real Type-1 choice |
| H2 | Minimal `ScanReport` / `Finding` dataclass | **Absorbed** into ARC-202 — the schema is a core deliverable of the detection spec; a deliberately minimal version would be outgrown within one season |
| H3 | Canonical technique name strings | **Carried forward** to ARC-301, informed by the ARC-201 taxonomy |
| H4 | Deprecation shims for the 0.1 facades | **Rejected** — a clean-room core plus a tagged `v0.1.1` makes 0.2.0 a documented break with a migration guide, not a shim layer |
| H5 | Drop `file_format` from string operations | **Moot** — true by construction in a string-first clean design |
| H6 | Technique registry | **Carried forward, promoted** to ARC-301 — foundational, not a de-laddering trick |
| H7 | `sanitize()` removes all families by default | **Absorbed** into ARC-304 — it is a policy question and belongs with the policy model |
| H8 | File layer wraps the string core | **Already settled** by ADR-002 |

ARC-104, ARC-105 and ARC-106 are superseded in the same movement: ARC-104 becomes Season 4, ARC-106 becomes
ARC-602, and ARC-105's bug list becomes corpus test cases rather than patches (the code being patched no
longer exists).

## Consequences

- Season 1 closes early, having delivered ARC-101 and ARC-102 — both foundational regardless of the rewrite.
- The repo is unblocked without ratifying four decisions the rewrite makes meaningless.
- Season numbering continues from 2 rather than restarting, so the ADR trail and PR history stay legible.
- `0.2.0` will be a breaking release. That cost is accepted and must be documented in a migration guide (ARC-603).

## Alternatives considered

- **Sign off all eight and proceed.** Rejected: four of the eight are invalidated by ADR-012, and H2 would lock
  in a `Finding` schema before the taxonomy that defines its contents exists.
- **Close ARC-103 with no carry-forward.** Rejected: H1, H3 and H6 are genuine design questions whose framing
  cost real thought; discarding them would mean re-deriving them from scratch in ARC-301.
