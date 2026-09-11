# ARC-NNN — <title>

- **Season:** <n>
- **Branch:** `arc/NNN-<slug>`
- **Status:** ☐ not started | ◐ in progress | ☑ done | ⊘ superseded
- **Depends on:** ARC-xxx | nothing — **unblocked, can start unattended**

## Goal
One paragraph: what "done" looks like and why it matters.

## In scope
- ...

## Out of scope
- ...

## Decisions needed

| # | Decision | Tier | Notes |
|---|----------|:----:|-------|
| **D1** | ... | **Type-1** | one-way door — needs sign-off |
| D2 | ... | Type-2 | assistant decides, logs to DECISION-LOG.md |

**At most four Type-1 rows.** More than four means the arc is too big — split it. (ADR-010)

## Acceptance criteria
- [ ] ...
- [ ] Tests pass offline & deterministically (`uv run --no-sync pytest`)
- [ ] `ruff check` / `ruff format --check` / `mypy src/phantomtext` clean
- [ ] New detection families have positive **and** benign corpus samples (CLAUDE.md rule 7)
- [ ] No precision/recall regression against the corpus baseline
- [ ] `STATUS.md` updated if capabilities changed
- [ ] `HANDOFF.md` updated with a next task that needs **no maintainer action**
- [ ] Type-2 decisions logged in `DECISION-LOG.md`

## Session log
- YYYY-MM-DD — ...
