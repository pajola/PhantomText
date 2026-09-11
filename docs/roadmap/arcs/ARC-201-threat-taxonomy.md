# ARC-201 — Threat taxonomy

- **Season:** 2 — Ground Truth & the Detection Spec
- **Branch:** `arc/201-threat-taxonomy` (off `main`)
- **Status:** ☐ not started
- **Depends on:** nothing — **this arc is unblocked and can start unattended**

## Goal

Produce `docs/spec/TAXONOMY.md`: the authoritative enumeration of everything PhantomText considers *invisible*
or *deceiving*, each entry with a stable ID, a precise definition, canonical examples, and — the part that
actually matters — a **legitimate-use note** describing where that character or construct appears innocently.

No code. No detectors. This arc produces the document every later arc is graded against.

## Why the legitimate-use note is the point

For a detector of this kind, false positives are fatal in a way misses are not. A miss is a gap; a false
positive is a reason to uninstall. Almost every character in the invisible set has a legitimate job:

- **U+200D ZWJ** — Devanagari and other Indic conjuncts; emoji sequences (👨‍👩‍👧, 🏳️‍🌈)
- **U+200C ZWNJ** — Persian/Farsi word-internal breaks; Indic scripts
- **U+200F RLM / U+200E LRM** — correct rendering of mixed Arabic/Hebrew and Latin
- **Combining marks (U+0300–U+036F)** — Vietnamese, transliteration, IPA, ordinary accented text in NFD
- **U+00AD SOFT HYPHEN** — legitimate hyphenation hints in justified text
- **U+FE0F VS16** — emoji presentation selector, on essentially every modern emoji
- **Mixed script** — a Chinese sentence containing a Latin brand name is not an attack

An entry without a defensible legitimate-use note is not finished.

## In scope

Each entry gets: `id`, `family`, `codepoints`/`construct`, `definition`, `why it hides`, `canonical example`,
`legitimate uses`, `default severity`, `detectability` (text-level vs requires format parsing), and
`related IDs`.

**Invisible — character level**
- `Cf` general-category format characters (the umbrella; enumerate, don't hand-wave)
- Zero-width: ZWSP U+200B, ZWNJ U+200C, ZWJ U+200D, WJ U+2060, ZWNBSP/BOM U+FEFF
- Bidi controls: LRM/RLM, LRE/RLE/LRO/RLO/PDF, the isolates LRI/RLI/FSI/PDI — including the Trojan Source
  reordering pattern (Boucher & Anderson, CVE-2021-42574)
- Tags block U+E0000–U+E007F — the deprecated language-tag block, invisible in every renderer, the current
  favourite for LLM prompt smuggling
- Variation selectors U+FE00–FE0F and U+E0100–U+E01EF — including the "hide arbitrary bytes in a selector
  chain" technique
- Whitespace substitution: NBSP U+00A0, the U+2000–U+200A quad/en/em family, U+202F, U+205F, U+3000, U+180E
- Soft hyphen U+00AD; other conditional-format characters
- Interlinear annotation U+FFF9–U+FFFB; U+2028/U+2029 line/paragraph separators

**Deceiving — character level**
- UTS #39 confusables: full table, skeleton mapping, single-script vs mixed-script confusables
- Mixed-script detection: script resolution, the Unicode "highly restrictive"/"moderately restrictive"
  restriction levels, and where each is the right default
- Cyrillic/Greek/Latin homoglyph sets specifically (the practical majority of real attacks)
- Combining-mark stacking / "Zalgo": density thresholds, and how they differ from legitimate stacking
- Fullwidth and mathematical alphanumeric substitutions (U+FF21…, U+1D400…)

**Document level** (detectable only after format parsing — flag as such, ARC-405 implements)
- Zero or near-zero font size; transparent fill; colour camouflage against background
- Out-of-bound / off-page positioning; clipped or masked content
- HTML: `display:none`, `visibility:hidden`, `aria-hidden`, `hidden`, off-screen positioning, zero-opacity,
  comments, CSS `content:`, `<meta>` and data attributes
- Metadata channels: XMP, DOCX core/custom properties, comments, tracked changes, headers/footers, alt-text,
  PDF annotations and OCG layers
- Font poisoning via cmap remapping — the glyph shown differs from the codepoint stored
- OCR-vs-text-layer mismatch (what a human reads vs what a parser extracts)

## Out of scope

- Any detector implementation (Season 3)
- The `Finding` schema itself (ARC-202) — this arc supplies the family IDs it will reference
- Corpus samples (ARC-203) — but note per entry what a good sample would look like

## Decisions needed

| # | Decision | Tier | Notes |
|---|----------|:----:|-------|
| **T1** | Family ID naming scheme | **Type-1** | IDs land in user config files, CI baselines and SARIF rule IDs — expensive to change. Proposal: `PT.<CLASS>.<FAMILY>` e.g. `PT.INVIS.ZERO_WIDTH`, `PT.DECEIVE.CONFUSABLE`, `PT.DOC.ZERO_SIZE_FONT` |
| T2 | Taxonomy file format (Markdown narrative vs YAML data + generated docs) | Type-2 | YAML is machine-readable and can drive the registry; decide and log |
| T3 | Default severity scale (3-level vs 4-level) | Type-2 | Reversible before ARC-202 freezes the schema |
| T4 | Whether restriction levels follow UTS #39 verbatim or a PhantomText subset | Type-2 | Behind the policy interface |

Only **T1** needs sign-off. Present it alone; do not bundle the others.

## Acceptance criteria

- [ ] `docs/spec/TAXONOMY.md` covers every family listed in scope
- [ ] Every entry has a legitimate-use note, or an explicit "no legitimate use" justification
- [ ] Every entry marked text-level or requires-format-parsing
- [ ] Family IDs follow the approved T1 scheme and are stable
- [ ] Cross-referenced against UTS #39, UAX #9, UAX #31 and the Trojan Source paper — citations included
- [ ] `ROADMAP.md` ARC-201 marked ☑; `STATUS.md` gains a taxonomy-coverage row
- [ ] `HANDOFF.md` updated, pointing at ARC-202 as an unblocked next task
- [ ] Type-2 decisions logged in `DECISION-LOG.md`

## Session log
- *(empty — arc not started)*
