# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.

⚠️ **Do not trust this file on sight.** It has drifted before. Run Step 0 of the session loop in `CLAUDE.md`
and reconcile against `git log`, `git status` and `gh pr list`. If this file disagrees with the repo, the repo
is right — correct this file first, say so, then continue.

---

## Current position
- **Season:** 2 — Ground Truth & the Detection Spec
- **Active arc:** ARC-201 — Threat taxonomy (**not started**)
- **Branch:** none yet — create `arc/201-threat-taxonomy` off `main`
- **Next release target:** 0.2.0 (end of Season 3)
- **Review queue:** empty ✅ (cap is 1)

## >>> START HERE (next session)
This task needs **no maintainer action to begin**. Start it unattended.

1. Run Step 0 verification (`CLAUDE.md`). Confirm `main` is clean and the suite is green.
2. Read `docs/roadmap/arcs/ARC-201-threat-taxonomy.md`.
3. Branch `arc/201-threat-taxonomy` off `main`.
4. Draft `docs/spec/TAXONOMY.md`. Research is the bulk of this arc — use the `unicode-analyst` subagent for
   the Unicode semantics and, above all, for the legitimate-use notes.
5. The only Type-1 gate in this arc is the **family ID naming scheme** (IDs land in user config files and CI
   baselines, so they are expensive to change). Everything else here is Type-2 — decide and log it.

## Git state *(verified 2026-09-10)*
- `main` @ `ce46a1a` — Season 0 (#1,#3,#4,#5) + ARC-101 (#6) + ARC-102 (#7) merged. No other remote branches.
- Working tree clean. Library is fully offline (no runtime network anywhere).
- Suite: 21 passed, 2 xfailed. ruff/mypy clean. CI = 12 jobs (ruff, build/import ×5, pytest ×5, mypy non-blocking).
- Tag `v0.1.1` is the AISec'25 paper artifact and stays put.

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
1. **ARC-201 — Threat taxonomy** (this session's target; unblocked).
2. ARC-202 — Finding schema. Carries a Type-1 gate: the serialized schema.
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
