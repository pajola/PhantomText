# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.

⚠️ **Do not trust this file on sight.** It has drifted before. Run Step 0 of the session loop in `CLAUDE.md`
and reconcile against `git log`, `git status` and `gh pr list`. If this file disagrees with the repo, the repo
is right — correct this file first, say so, then continue.

---

## Current position
- **Season:** 2 — Ground Truth & the Detection Spec
- **Active arc:** ARC-202 — Finding schema & severity model (**implemented, PR not yet opened**)
- **Branch:** `arc/202-finding-schema` (off `main`), not pushed
- **Next release target:** 0.2.0 (end of Season 3)
- **Review queue:** empty ✅ (cap is 1) — opening this arc's PR fills it to 1/1

## >>> START HERE (next session)
This task needs **no maintainer action to begin**. Start it unattended.

1. Run Step 0 verification (`CLAUDE.md`). Confirm `arc/202-finding-schema` is checked out and the
   suite is green: 57 passed, 2 xfailed (up from 21 — `tests/test_report.py` adds 34).
2. Read `docs/roadmap/arcs/ARC-202-finding-schema.md`'s session log for what's already decided and
   implemented — all D1–D7 are settled ([ADR-014](../decisions/ADR-014-finding-schema.md)), all
   acceptance criteria but "HANDOFF.md updated" and the PR itself are checked off.
3. Run `/arc-ship`: quality gates, diff summary, risk notes, PR body, merge command. **Flag one
   thing in the risk notes**: implementation deviated from the approved D6 in one respect — the
   planned `slots=True` was dropped after it combined with `frozen=True` to hit a real CPython bug
   (confirmed on 3.12.13, reproducer in the session log). This is a Type-2 amendment already logged
   in `DECISION-LOG.md`, not a new Type-1 question, but it's a deviation from what was written down
   and worth a sentence in the PR body rather than only in the log.
4. Open the PR. That fills the review queue to cap — do not start ARC-203 until it merges.

## Git state *(verified 2026-09-11)*
- `main` @ `8ab7143` — Season 0 (#1,#3,#4,#5) + ARC-101 (#6) + ARC-102 (#7) + the project re-cut (#9)
  + ARC-201 threat taxonomy (#10) + ARC-202's plan and ADR-014 (direct commits, pre-implementation)
  merged. Working tree clean on `main`.
- `arc/202-finding-schema` created off `main`, not yet pushed. Adds
  `src/phantomtext/core/report.py` and `tests/test_report.py` — no other `src/` files touched.
- `arc/103-string-first-api` (PR #8) was **closed, not merged** — superseded per ADR-009, as expected.
- Library is fully offline (no runtime network anywhere). Suite on the branch: 57 passed, 2 xfailed;
  ruff/mypy clean.

## Done
- 2026-08-03 — ARC-001 (governance) + ARC-002 (src layout / hygiene). *(#1, #3)*
- 2026-08-04 — ARC-003: Hatchling PEP 621 build, tooling, CI, pre-commit. ADR-006. *(#4)*
- 2026-08-04 — ARC-004: offline deterministic pytest baseline; Season 0 complete. *(#5)*
- 2026-08-04 — ARC-101: unified `core/base.py`; 8 techniques migrated. ADR-007. *(#6)*
- 2026-08-05 — ARC-102: vendored UTS#39 table; `requests` dropped; library fully offline. ADR-008. *(#7)*
- **2026-09-10 — Project re-cut.** Root cause of the five-week stall diagnosed and fixed in governance
  (ADR-010), roadmap re-cut detection-first (ADR-011), clean-room core adopted (ADR-012), ARC-103 superseded
  (ADR-009). Season 1 closed early: ARC-101/102 delivered, ARC-103–106 superseded.
- **2026-09-11 — ARC-201: threat taxonomy.** `docs/spec/TAXONOMY.md` — 21 families (`PT.INVIS.*`
  ×8, `PT.DECEIVE.*` ×5, `PT.DOC.*` ×8), each with a legitimate-use note, severity, detectability,
  and citations. ADR-013 (family ID scheme). An initial `PT.DOC.*` draft of 16 IDs was reviewed and
  collapsed to 8 (DECISION-LOG). *(#10)*

## Next steps
1. **Ship ARC-202's PR** (`/arc-ship`) — implementation is done, this is the unblocked next action.
2. ARC-203 — Ground-truth corpus, including the benign multilingual set. Do not start until ARC-202's
   PR is merged (review-queue cap).
3. ARC-204 — Evaluation harness + CI regression gate. Closes Season 2.

## Open questions / awaiting maintainer
- None yet — ARC-202's PR is about to be opened, which will make this the one arc in the queue.

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
