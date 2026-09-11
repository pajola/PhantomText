# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.

⚠️ **Do not trust this file on sight.** It has drifted before. Run Step 0 of the session loop in `CLAUDE.md`
and reconcile against `git log`, `git status` and `gh pr list`. If this file disagrees with the repo, the repo
is right — correct this file first, say so, then continue.

---

## Current position
- **Season:** 2 — Ground Truth & the Detection Spec
- **Active arc:** ARC-201 — Threat taxonomy (**content drafted, PR not yet opened**)
- **Branch:** `arc/201-threat-taxonomy` (off `main`), not pushed
- **Next release target:** 0.2.0 (end of Season 3)
- **Review queue:** empty ✅ (cap is 1) — opening this arc's PR next session/turn will fill it to 1/1

## >>> START HERE (next session)
This task needs **no maintainer action to begin**. Start it unattended.

1. Run Step 0 verification (`CLAUDE.md`). Confirm `arc/201-threat-taxonomy` is checked out and the suite is
   green (no `src/` changes this arc, so it should be unchanged from `main`).
2. Read `docs/spec/TAXONOMY.md` (the drafted content) and the ARC-201 arc file's session log for what's
   already decided.
3. Run `/arc-ship`: quality gates, diff summary, risk notes, PR body, merge command. **Flag the
   `PT.DOC.*` 16-vs-8 family-ID expansion in the risk notes explicitly** — it's logged as Type-2
   (DECISION-LOG 2026-09-11) but is the one thing in this arc worth the maintainer's deliberate look, since
   the arc's own acceptance criteria call family-ID stability out as the point of the exercise.
4. Open the PR. That fills the review queue to its cap of 1 — the session after this one should not start a
   new arc; its job is to make this review cheap (see `CLAUDE.md`'s review-queue-cap rule).

Remaining open items are recorded in `docs/spec/TAXONOMY.md`'s own "Open items carried forward" section
(two candidate `PT.INVIS.*` ID splits deferred to the ARC-202 schema freeze, an OCR-engine
runtime-dependency flag for ARC-405, and two format details needing verification) — nothing here blocks
shipping this arc's PR.

## Git state *(verified 2026-09-11)*
- `main` @ `3da5bb2` — Season 0 (#1,#3,#4,#5) + ARC-101 (#6) + ARC-102 (#7) + the project re-cut, PR #9
  (#9, `docs: re-cut project governance and roadmap (ADR-009..012)`) merged. Working tree clean.
- `arc/103-string-first-api` (PR #8) was **closed, not merged** — superseded per ADR-009, as expected.
- Stale remote branch `origin/arc/200-project-recut` remains after PR #9 merged; safe to delete, not urgent.
- Library is fully offline (no runtime network anywhere).
- Suite: 21 passed, 2 xfailed. ruff/mypy not re-run this session. No open PRs — review queue is genuinely empty.

## Done
- 2026-08-03 — ARC-001 (governance) + ARC-002 (src layout / hygiene). *(#1, #3)*
- 2026-08-04 — ARC-003: Hatchling PEP 621 build, tooling, CI, pre-commit. ADR-006. *(#4)*
- 2026-08-04 — ARC-004: offline deterministic pytest baseline; Season 0 complete. *(#5)*
- 2026-08-04 — ARC-101: unified `core/base.py`; 8 techniques migrated. ADR-007. *(#6)*
- 2026-08-05 — ARC-102: vendored UTS#39 table; `requests` dropped; library fully offline. ADR-008. *(#7)*
- **2026-09-10 — Project re-cut.** Root cause of the five-week stall diagnosed and fixed in governance
  (ADR-010), roadmap re-cut detection-first (ADR-011), clean-room core adopted (ADR-012), ARC-103 superseded
  (ADR-009). Season 1 closed early: ARC-101/102 delivered, ARC-103–106 superseded.

## Next steps
1. **Ship ARC-201's PR** (`/arc-ship`) — content is drafted, this is the unblocked next action.
2. ARC-202 — Finding schema. Carries a Type-1 gate: the serialized schema. Do not start until ARC-201's PR
   is merged (review-queue cap).
3. ARC-203 — Ground-truth corpus, including the benign multilingual set.
4. ARC-204 — Evaluation harness + CI regression gate. Closes Season 2.

## Open questions / awaiting maintainer
- None. The queue is deliberately empty. **Keep it that way** — see the review-queue cap in `CLAUDE.md`.

## Post-mortem: why the project stalled 2026-08-05 → 2026-09-10
Recorded here so a future session does not recreate the conditions.

1. **An untiered sign-off rule.** Every decision, however reversible, needed the maintainer. ARC-103 accumulated
   eight of them into a single gate that required one contiguous block of attention. It never came. → ADR-010
   splits decisions into one-way and two-way doors and caps a gate at four.
2. **Sessions ended blocked.** Four arcs sat "done, awaiting review" simultaneously. Every possible next action
   required the maintainer, so a fresh session had nothing it could legally start. → ADR-010 requires every
   session to end on a task that needs no maintainer action, and caps the review queue at one.
3. **The state file drifted.** This file instructed a session to push and open a PR for `arc/102`, which was
   already merged into `main`. A state file that lies costs more than no state file. → Step 0 of the session
   loop now verifies HANDOFF against the repo before acting on it.

## Key findings from the 0.1.1 audit (now corpus test cases, not bugs to patch)
Under the clean-room decision (ADR-012) these are no longer fixes to make — they are regressions the new core
must never reintroduce, and each should become a test:
- Two duplicate `AttackBase` classes with incompatible signatures. *(fixed in ARC-101)*
- `ContentInjector.inject()` a stub; real injection elsewhere with a different API.
- `FileSanitizer.sanitize_file()` was `pass` — advertised but non-functional.
- `HomoglyphText` fetched unicode.org at runtime on every instantiation. *(fixed in ARC-102)*
- Off-by-one in zero-width RNG: `randint(0, n-1)` never picks the last symbol.
- Injection `check()` methods were `pass` → scanner blind to injection.
- `obfuscate()` accepted `"markdown"` with no obfuscator behind it → crash.
- `.txt` handler existed but was never wired up.
