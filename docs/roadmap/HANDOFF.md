# HANDOFF — Live project state

The living state file. **Read this first** at the start of every session; **update it** at the end of every session.
It is the handoff between sessions.

---

## Current position
- **Season:** 0 — Foundation & Governance
- **Active arc:** ARC-001 — Governance scaffold
- **Branch:** `arc/001-governance`
- **Next release target:** 0.2.0 (end of Season 1)

## Done this session (2026-08-03)
- Analyzed `phantomtext` 0.1.1 (from PyPI sdist) — see findings summary below.
- Agreed positioning (production library), repo (rewrite in place on `github.com/pajola/PhantomText`), and
  human-in-the-middle cadence with per-arc PRs.
- Cloned the real repo; confirmed `main` ≈ 0.1.1.
- Accepted foundational decisions ADR-001…005.
- Wrote the governance scaffold (this arc): CLAUDE.md, ROADMAP, STATUS, HANDOFF, ADR-001…005.

## Next steps
1. Commit & open PR for ARC-001 (governance scaffold) — **awaiting maintainer review**.
2. Start ARC-002 (repo hygiene: `src/` layout + dead-file quarantine + metadata fixes).

## Open questions / awaiting maintainer
- (none currently — ADR-001…005 accepted)

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
