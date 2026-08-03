# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.
It is the handoff between sessions.

---

## Current position
- **Season:** 0 — Foundation & Governance
- **Active arc:** ARC-002 — Repo hygiene (committed locally, awaiting review)
- **Branch:** `arc/002-repo-hygiene` (off `arc/001-governance`)
- **Next release target:** 0.2.0 (end of Season 1)

## Git state (nothing pushed yet — no credentials on this machine)
- `arc/001-governance` @ `ac97ab1` — governance scaffold (committed, not pushed).
- `arc/002-repo-hygiene` — src-layout + hygiene (about to commit).
- **Push is blocked** pending maintainer setting up `gh auth` / SSH. Once available: push both, open PRs.

## Done (2026-08-03)
- Analyzed `phantomtext` 0.1.1; agreed positioning/repo/cadence; cloned repo; accepted ADR-001…005.
- ARC-001: wrote governance scaffold (CLAUDE.md, ROADMAP, STATUS, HANDOFF, ADR-001…005). Committed.
- ARC-002: `src/` layout move + dead-file/artifact quarantine + `.gitignore` + minimal `pyproject` fix.
  28 core files now under `src/phantomtext/`; root cleaned; history preserved.

## Next steps
1. Maintainer sets up push credentials → push `arc/001` and `arc/002`, open the two PRs.
2. Start ARC-003 (build & tooling: PEP 621 rewrite, delete setup.py/requirements.txt/build_package.sh,
   fix metadata author-email + repo-URL, trim deps Flask/requests/numpy, add ruff/mypy/pytest + CI).

## Open questions / awaiting maintainer
- Push credentials (gh auth or SSH key) — blocks all pushes/PRs.

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
