# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.
It is the handoff between sessions.

---

## Current position
- **Season:** 1 — Core API Consolidation
- **Active arc:** ARC-103 — String-first public API (**planned; decisions H1–H8 awaiting sign-off**)
- **Branch:** none yet (create `arc/103-string-first-api` off `main` after H1–H8 are approved)
- **Next release target:** 0.2.0 (end of Season 1)

## >>> START HERE (next session)
1. Read `docs/roadmap/arcs/ARC-103-string-first-api.md` — the ARC-103 plan with decision table **H1–H8**.
2. Present H1–H8 to Luca, get sign-off (human-in-the-middle), write **ADR-009** for the API shape.
3. Then branch `arc/103-string-first-api` off `main` and implement. `uv sync --extra dev`;
   verify with `uv run --no-sync pytest` / `ruff check .` / `mypy src/phantomtext`.

## Git state
- `main` @ `a6efa20` — Season 0 (#1,#3,#4,#5) + ARC-101 (#6) + ARC-102 (#7) merged. Auth via gh (classic PAT).
- Working tree clean; **library is fully offline** (no runtime network anywhere).
- Env: `uv` only (`uv run --no-sync` avoids re-syncing away dev extras). Suite: 21 passed, 2 xfailed; ruff/mypy clean.
- CI = 12 jobs (ruff, build/import ×5, pytest ×5, mypy non-blocking). Repo also runs a Sourcery bot on PRs (not a gate).

## Done
- 2026-08-03 — ARC-001 (governance) + ARC-002 (src layout/hygiene) written, merged to `main` (PRs #1, #3).
  (Note: original stacked PR #2 was auto-closed when its base branch was deleted during #1's merge; arc/002
  was rebased onto main and re-merged as #3.)
- 2026-08-04 — ARC-003: Hatchling PEP 621 build; deleted setup.py/requirements.txt/build_package.sh/MANIFEST.in;
  metadata fixed; deps corrected (drop Flask, PyPDF2>=3.0, pytest→dev); ruff/mypy/pytest config; pre-commit;
  CI workflow; ruff format+autofix baseline (+5 hand fixes); requires-python >=3.9. ADR-006 (Hatchling). Merged (#4).
- 2026-08-04 — ARC-004: rewrote tests as offline/deterministic pytest; 5 legacy test files removed; xfail for
  the two stubs; CI pytest matrix + non-blocking mypy. E1–E5 accepted. Merged (#5) → **Season 0 complete**.
- 2026-08-04 — ARC-101: new `core/base.py`; migrated all 8 techniques; `sanitized`→`sanitize` (aliased);
  `name`/`family` metadata; honest injection `check()` stubs. ADR-007. Merged (#6).
- 2026-08-05 — ARC-102: vendored `intentional.txt` in `phantomtext/data/` (offline, cached parser); removed the
  runtime `requests.get`; **dropped `requests`**; added `python -m phantomtext.data.refresh_homoglyphs`;
  simplified tests (no more network patch). ADR-008. 21 passed, 2 xfailed. Library now fully offline.

## Next steps
1. Push `arc/102-vendor-homoglyphs`, open PR → `main`; maintainer reviews CI + merges.
2. **ARC-103 — string-first public API**: the central ADR-002 deliverable. Design `scan / obfuscate / inject /
   sanitize` operating on `str`, with the file layer wrapping them; add deprecation shims for the 0.1 facades
   (`ContentObfuscator`, `ContentInjector`, `FileScanner`). Then ARC-104 (formats incl. txt), ARC-105 (fix RNG
   off-by-one + drop numpy), ARC-106 (batch/parallel). Season 1 closes with the 0.2.0 release.

## Open questions / awaiting maintainer
- Review & merge ARC-004 PR (watch CI) → closes Season 0.

## Key findings from the 0.1.1 audit (context for upcoming arcs)
- Two duplicate `AttackBase` classes with incompatible signatures.
- `ContentInjector.inject()` is a stub; real injection lives in `injection/*` with a different API.
- `FileSanitizer.sanitize_file()` is `pass` (advertised but non-functional).
- `HomoglyphText` fetches unicode.org at runtime on every instantiation (no cache/timeout/offline path);
  `FileScanner.__init__` triggers it → every scan hits the network.
- Off-by-one in zero-width RNG (`randint(0, n-1)` never picks the last symbol).
- Injection `check()` methods are `pass` → scanner blind to injection.
- `obfuscate()` accepts `"markdown"` but no obfuscator supports it → crash. `.txt` handler exists but isn't wired.
- Packaging smells: `font-poisoning.py` (unimportable), `test.py` in package, Flask/requests as core deps,
  placeholder `example.com` author email, wrong repo URL in metadata, dead artifacts in the tarball.

## Working-core inventory (preserve through the refactor)
`obfuscation/{zero_width_text, homoglyph_text, diacritical_marks, reordering_char}`,
`injection/{zerosize_injection, transparent_injection}`, `file_scanning.FileScanner`,
`formats/{pdf, docx, html, txt}`, `text_loader`, `text_saver`, `fonts/DejaVuSans.*`.
