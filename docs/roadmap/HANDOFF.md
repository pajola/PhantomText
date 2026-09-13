# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.

⚠️ **Do not trust this file on sight.** It has drifted before. Run Step 0 of the session loop in `CLAUDE.md`
and reconcile against `git log`, `git status` and `gh pr list`. If this file disagrees with the repo, the repo
is right — correct this file first, say so, then continue.

---

## Current position
- **Season:** 2 — Ground Truth & the Detection Spec
- **Active arc:** ARC-203 (ground-truth corpus & generator) — implemented on
  `arc/203-ground-truth-corpus`, **awaiting review** (PR not yet opened)
- **Branch:** `arc/203-ground-truth-corpus`
- **Next release target:** 0.2.0 (end of Season 3)
- **Review queue:** ARC-203 (1/1 — at cap; do not open a new arc until this is reviewed)

## >>> START HERE (next session)
**Review queue is at cap (1).** Per CLAUDE.md's review-queue rule, the next session's job is to
make ARC-203's review cheap, not to open ARC-204. This needs **no maintainer action to begin**.

1. Run Step 0 verification (`CLAUDE.md`) against branch `arc/203-ground-truth-corpus`.
2. If a PR for ARC-203 doesn't exist yet: run `/arc-ship` to produce the diff summary, risk notes,
   test evidence, and PR body/merge command, then open the PR.
3. If the PR already exists and the maintainer has acted (approved/requested changes): address
   feedback, or — once merged — draft ARC-204 (`/arc-plan`) as the next arc. ARC-204 (evaluation
   harness) directly consumes ARC-203's manifest (`corpus/manifests/corpus.jsonl`,
   `corpus.manifest.CorpusSample`), so re-read `corpus/manifest.py` first.
4. If the PR exists and is still unreviewed: do not open a new arc. There is nothing else this
   session should start.

## Git state *(verified 2026-09-13)*
- `main` @ `a92ae21` — Season 0 (#1,#3,#4,#5) + ARC-101 (#6) + ARC-102 (#7) + the project re-cut (#9)
  + ARC-201 threat taxonomy (#10) + ARC-202 Finding/Report schema (#11) merged. Working tree clean
  on `main`.
- `arc/203-ground-truth-corpus`, off `main` @ `a92ae21`: ARC-203 plan + ADR-015 (D1-D3) + full
  implementation (`corpus/manifest.py`, `corpus/generators/*`, `corpus/generate_corpus.py`,
  `corpus/benign/*`, `tests/test_corpus.py`) committed. Not yet pushed / PR not yet opened.
- `arc/202-finding-schema` remote branch was deleted on merge — no stale branches remain.
- `arc/103-string-first-api` (PR #8) was **closed, not merged** — superseded per ADR-009, as expected.
- Library is fully offline (no runtime network anywhere). Suite on `arc/203-ground-truth-corpus`:
  86 passed, 2 xfailed (55 on `main` + 31 new in `tests/test_corpus.py`); ruff/mypy clean on both
  `src/` and `corpus/`.

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
- **2026-09-11 — ARC-202: Finding/Report schema.** `src/phantomtext/core/report.py` — `Finding`,
  `Report`, `Span`, `Provenance`, `Severity`; JSON round-trip; SARIF 2.1.0 export. ADR-014 (D1–D4).
  Not re-exported from `phantomtext` (public API shape is ARC-301). Implementation dropped the
  planned `slots=True` after it hit a real CPython bug combined with `frozen=True` — logged as a
  Type-2 amendment, not re-gated. *(#11)*

## Next steps
1. **Review ARC-203** — implemented on `arc/203-ground-truth-corpus`, PR not yet opened. Run
   `/arc-ship` to prepare it.
2. ARC-204 — Evaluation harness + CI regression gate. Closes Season 2 (blocked on ARC-203 merging).

## Open questions / awaiting maintainer
- **ARC-203 awaiting review** (PR to be opened via `/arc-ship`). This is the one arc the review-queue
  cap allows — do not open ARC-204 or any other arc until this is reviewed and merged.

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
