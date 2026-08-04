# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.
It is the handoff between sessions.

---

## Current position
- **Season:** 0 — Foundation & Governance
- **Active arc:** ARC-003 — Build & tooling (done, awaiting review)
- **Branch:** `arc/003-build-tooling` (off `main`)
- **Next release target:** 0.2.0 (end of Season 1)

## Git state
- `main` @ `cbeec23` — ARC-001 (#1) + ARC-002 (#3) merged. Auth works via gh (Luca's classic PAT).
- `arc/003-build-tooling` — Hatchling build + tooling + CI (about to commit & PR).
- Env: `uv` verified — `uv sync` + import OK on Python 3.9.25 and 3.14.

## Done
- 2026-08-03 — ARC-001 (governance) + ARC-002 (src layout/hygiene) written, merged to `main` (PRs #1, #3).
  (Note: original stacked PR #2 was auto-closed when its base branch was deleted during #1's merge; arc/002
  was rebased onto main and re-merged as #3.)
- 2026-08-04 — ARC-003: Hatchling PEP 621 build; deleted setup.py/requirements.txt/build_package.sh/MANIFEST.in;
  metadata fixed; deps corrected (drop Flask, PyPDF2>=3.0, pytest→dev); ruff/mypy/pytest config; pre-commit;
  CI workflow; ruff format+autofix baseline (+5 hand fixes); requires-python >=3.9. ADR-006 (Hatchling) accepted.

## Next steps
1. Push `arc/003-build-tooling`, open PR → `main`; maintainer reviews CI + merges.
2. Then **ARC-004** (deterministic offline test baseline): make the existing tests run without network and
   without writing to `./output`; add a pytest CI job + mypy (non-blocking) once green. Closes Season 0.

## Open questions / awaiting maintainer
- Review & merge ARC-003 PR (watch CI).

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
