# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.

⚠️ **Do not trust this file on sight.** It has drifted before. Run Step 0 of the session loop in `CLAUDE.md`
and reconcile against `git log`, `git status` and `gh pr list`. If this file disagrees with the repo, the repo
is right — correct this file first, say so, then continue.

---

## Current position
- **Season:** 2 — Ground Truth & the Detection Spec
- **Active arc:** ARC-201 — Threat taxonomy (**PR #10 open, awaiting merge**)
- **Branch:** `arc/201-threat-taxonomy` (pushed to `origin`)
- **Next release target:** 0.2.0 (end of Season 3)
- **Review queue:** 1/1 — PR #10, at cap

## >>> START HERE (next session)
The review queue is at cap. **Do not open a new arc.** The only unblocked task is making PR #10's
review/merge cheap.

1. Run Step 0 verification (`CLAUDE.md`). Confirm `main` is unchanged and `arc/201-threat-taxonomy`
   still applies cleanly on top of it.
2. Check `gh pr view 10` for maintainer comments since the last update. All acceptance criteria are
   now met (see the ARC-201 arc file) — the one open question (`PT.DOC.*` family-ID granularity) was
   reviewed and resolved: collapsed from 16 to 8 IDs, 1:1 with the arc's scope bullets.
3. If the maintainer has approved, merge with `gh pr merge 10 --squash --delete-branch`, then update
   `ROADMAP.md` (☑), `STATUS.md`, and this file to point at ARC-202 as the next unblocked task.
4. If there are new comments, address them the same way the `PT.DOC.*` collapse was handled: edit,
   commit, push to the same branch (PR updates in place) — do not open a second PR.

Remaining open items, none blocking, are recorded in `docs/spec/TAXONOMY.md`'s own "Open items
carried forward" section: two candidate `PT.INVIS.*` ID splits deferred to the ARC-202 schema
freeze (now leaning toward *not* splitting, given the `PT.DOC.*` precedent), an OCR-engine
runtime-dependency flag for ARC-405, and two format details needing verification.

## Git state *(verified 2026-09-11)*
- `main` @ `3da5bb2` — Season 0 (#1,#3,#4,#5) + ARC-101 (#6) + ARC-102 (#7) + the project re-cut, PR #9
  (#9, `docs: re-cut project governance and roadmap (ADR-009..012)`) merged. Working tree clean.
- `arc/201-threat-taxonomy` pushed to origin, PR #10 open (`docs: threat taxonomy spec (ARC-201)`).
  Docs-only arc — no `src/` changes, so gates are unchanged from `main`: 21 passed, 2 xfailed;
  ruff/mypy clean.
- `arc/103-string-first-api` (PR #8) was **closed, not merged** — superseded per ADR-009, as expected.
- Stale remote branch `origin/arc/200-project-recut` remains after PR #9 merged; safe to delete, not urgent.
- Library is fully offline (no runtime network anywhere).

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
1. **Merge PR #10** (ARC-201) once satisfied — merge command is in the PR / arc-ship output:
   `gh pr merge 10 --squash --delete-branch`.
2. ARC-202 — Finding schema. Carries a Type-1 gate: the serialized schema. Do not start until PR #10
   is merged (review-queue cap).
3. ARC-203 — Ground-truth corpus, including the benign multilingual set.
4. ARC-204 — Evaluation harness + CI regression gate. Closes Season 2.

## Open questions / awaiting maintainer
- **PR #10 (ARC-201) awaiting merge decision.** The one substantive review point
  (`PT.DOC.*` family-ID granularity) has already been resolved in-thread — collapsed 16→8. Merge
  when satisfied.

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
