# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.
It is the handoff between sessions.

---

## Current position
- **Season:** 1 — Core API Consolidation (**Season 0 complete**)
- **Active arc:** ARC-101 — Unify `AttackBase` (done, awaiting review)
- **Branch:** `arc/101-unify-attackbase` (off `main`)
- **Next release target:** 0.2.0 (end of Season 1)

## Git state
- `main` @ `5a29e71` — Season 0 fully merged (PRs #1, #3, #4, #5). Auth via gh (Luca's classic PAT).
- `arc/101-unify-attackbase` — `core/base.py` hierarchy + 8 techniques migrated (about to commit & PR).
- Env: `uv` only (`uv run --no-sync` avoids re-syncing away dev extras). Suite: 20 passed, 2 xfailed; ruff/mypy clean.

## Done
- 2026-08-03 — ARC-001 (governance) + ARC-002 (src layout/hygiene) written, merged to `main` (PRs #1, #3).
  (Note: original stacked PR #2 was auto-closed when its base branch was deleted during #1's merge; arc/002
  was rebased onto main and re-merged as #3.)
- 2026-08-04 — ARC-003: Hatchling PEP 621 build; deleted setup.py/requirements.txt/build_package.sh/MANIFEST.in;
  metadata fixed; deps corrected (drop Flask, PyPDF2>=3.0, pytest→dev); ruff/mypy/pytest config; pre-commit;
  CI workflow; ruff format+autofix baseline (+5 hand fixes); requires-python >=3.9. ADR-006 (Hatchling). Merged (#4).
- 2026-08-04 — ARC-004: rewrote tests as offline/deterministic pytest; 5 legacy test files removed; xfail for
  the two stubs; CI pytest matrix + non-blocking mypy. E1–E5 accepted. Merged (#5) → **Season 0 complete**.
- 2026-08-04 — ARC-101: new `core/base.py` (`Attack`/`ObfuscationAttack`/`InjectionAttack`); migrated all 8
  techniques; deleted both old `attack_base*.py`; `sanitized`→`sanitize` (aliased); `name`/`family` metadata;
  honest injection `check()` stubs. ADR-007 accepted. 20 passed, 2 xfailed.

## Next steps
1. Push `arc/101-unify-attackbase`, open PR → `main`; maintainer reviews CI + merges.
2. **ARC-102 — vendor homoglyph data offline**: ship the Unicode confusables table in-package, remove the
   runtime `requests.get` in `HomoglyphText._load_homoglyphs`, drop the `requests` dependency, add a refresh
   tool. (Then the conftest homoglyph patch can be simplified/removed.) After that: ARC-103 (string-first public
   API + deprecation shims for `ContentObfuscator`/`ContentInjector`/`FileScanner`), ARC-104 (formats incl. txt),
   ARC-105 (fix RNG off-by-one, drop numpy), ARC-106 (batch/parallel). Season 1 closes with the 0.2.0 release.

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
