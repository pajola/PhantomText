# ADR-012 — Clean-room rewrite of the core

- **Status:** Accepted (2026-09-10)
- **Deciders:** Luca (maintainer), assistant

## Context

The 0.1.1 audit found the defensive half of the library to be largely non-functional: `FileSanitizer.sanitize_file()`
was `pass`, injection `check()` methods were `pass`, `ContentInjector.inject()` was a stub while real injection
lived elsewhere under a different API, and the scanner had no notion of severity, confidence or provenance.
The whole package is roughly 2,100 lines of Python.

Two arcs of consolidation (ARC-101, ARC-102) improved the attack half materially. The remaining plan (ARC-103–106)
was a sequence of retrofits onto a structure whose defensive half does not exist and whose public API was
described by the maintainer as broken.

## Decision

**The v2 core is written clean-room against the Season 2 spec. Nothing is ported.**

- `v0.1.1` is tagged and stays as the AISec'25 paper artifact. It is not maintained.
- The 0.1 code may be **consulted** as a reference — for technique semantics, for the format handling that
  worked, for what the paper actually did. It may not be **copied** into the v2 core.
- The working-core inventory (`obfuscation/*`, `injection/{zerosize,transparent}`, `formats/*`, `text_loader`,
  `text_saver`, the DejaVu font assets) is a *behavioural* specification for Season 5, not a codebase to
  refactor. Where a 0.1 technique produced correct output, the v2 implementation must reproduce that output
  and a corpus sample must pin it.
- The bugs in the audit list become corpus test cases — regressions the new core must never reintroduce —
  rather than patches to apply.
- `0.2.0` is therefore a breaking release, with a migration guide (ARC-603).

The one structural element that survives is `core/base.py` from ARC-101, as *design input* to ARC-301's
registry and attack hierarchy — its shape was derived from the taxonomy the v2 spec will formalise anyway.

## Consequences

- No inherited structural debt, and no half-migrated intermediate states where some techniques use the new
  base and some the old.
- The 21 passing tests from ARC-004 stop being a ratchet on the new core. They remain valid against `v0.1.1`
  and their *intent* must be re-expressed as corpus samples — an explicit ARC-203 obligation, and the main
  risk this decision carries.
- Contributors reading the paper will find code that no longer matches it; ARC-703's research-repo split and
  clear cross-linking are how that is addressed.
- Realistically slower to first working detector than incremental refactoring, and faster to a trustworthy one.

## Alternatives considered

- **Module-by-module rewrite behind the arc process**, keeping the existing tests green as a ratchet. A
  legitimate option, rejected because the tests pin 0.1 behaviour including behaviour the spec will change,
  and because the defensive half — the part that matters most — has essentially nothing to keep.
- **Continue the incremental consolidation (ARC-103–106).** Rejected: it ends at a tidier version of a
  structure the maintainer does not want.
