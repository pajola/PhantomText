# ADR-005 — Per-arc branches & PRs

- **Status:** Accepted (2026-08-03)
- **Deciders:** Luca (maintainer), assistant

## Context
The maintainer reviews every meaningful decision (human-in-the-middle) and wants small, focused reviews rather
than large batched changes.

## Decision
- **One arc = one branch = one PR.** Branch name `arc/<NNN>-<slug>` (e.g. `arc/002-repo-hygiene`).
- PRs target `main`; `main` stays releasable at all times.
- **Conventional Commits** for messages; **semver** for releases.
- No decision is implemented before its ADR is Accepted. The PR description links the arc file and any ADRs.
- The assistant shows the diff and waits for explicit approval before committing/pushing.

## Consequences
- More branches/PRs (higher process overhead) in exchange for tight, reviewable increments and a clean history.

## Alternatives considered
- One long-lived Season branch — rejected: reviews get large and coupled.
