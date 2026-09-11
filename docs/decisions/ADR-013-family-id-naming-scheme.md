# ADR-013 — Taxonomy family ID naming scheme

- **Status:** Accepted (2026-09-11)
- **Deciders:** Luca (maintainer), assistant

## Context

ARC-201 (threat taxonomy) needs a stable identifier for every entry in `docs/spec/TAXONOMY.md`. These IDs
are a one-way door: they will be written into user config files (per-family severity overrides, script/
language allowlists), committed into CI regression baselines (ARC-204), and emitted as SARIF `ruleId` values
(ARC-601). Once a user has one of these in a config file or a pinned baseline, renaming it silently breaks
their config (a dead override, not an error) and shifts their CI baseline, so the scheme had to be settled
before any entries were written rather than decided ad hoc mid-arc.

## Decision

**Family IDs use the dotted scheme `PT.<CLASS>.<FAMILY>`**, e.g. `PT.INVIS.ZERO_WIDTH`,
`PT.DECEIVE.CONFUSABLE`, `PT.DOC.ZERO_SIZE_FONT`.

- `<CLASS>` is one of the taxonomy's top-level classes from ARC-201's scope: `INVIS` (character-level
  invisible), `DECEIVE` (character-level deceiving), `DOC` (document-level, requires format parsing).
- `<FAMILY>` is a short, stable, upper-snake-case family name, assigned once per family and never reused for
  a different meaning even if the family is later split or deprecated.
- IDs are permanent once an entry ships in a tagged release: a family may be marked deprecated in the
  taxonomy doc, but its ID is never recycled.

## Consequences

- Config files and CI baselines read as `PT.INVIS.ZERO_WIDTH`, not an opaque numeric code — a user can tell
  what fired without a lookup table, and a CI diff is self-explanatory.
- The class prefix gives ARC-304's policy profiles (`strict` / `balanced` / `permissive`) a natural axis to
  set class-wide defaults over, then override per family.
- Document-level families (`PT.DOC.*`), which have no underlying codepoint, are represented as naturally as
  character-level ones — this is where the numeric and Unicode-block-mirroring alternatives were weaker.
- ARC-201 is responsible for assigning the initial ID to every entry in scope and keeping the list the single
  source of truth; ARC-202's `Finding` schema references these IDs rather than redefining them.

## Alternatives considered

- **Flat numeric codes** (`PT-014`, CWE/CVE-style). Maximally stable under renames — the ID never encodes a
  name that could change — but opaque: reading a CI baseline or a policy override requires a lookup table to
  know what actually fired. Rejected because the product's own goal (a security tool a practitioner keeps
  switched on) argues for self-explanatory output over ID immutability at the margin.
- **Dotted path mirroring Unicode block/construct names** (`PT.unicode.tags-block`). Reads well next to the
  UAX/UTS citations the taxonomy already needs, but has no natural home for document-level families that
  don't correspond to a codepoint or block (zero-size font, off-page placement, metadata channels). Rejected
  because roughly a third of ARC-201's scope is document-level.
