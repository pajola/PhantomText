# ADR-011 — Detection-first roadmap; no detector without ground truth

- **Status:** Accepted (2026-09-10)
- **Deciders:** Luca (maintainer), assistant

## Context

The original roadmap sequenced the attack engine first (Season 1) and detection second (Season 2), mirroring
the structure of the AISec'25 paper. But the reason a practitioner installs PhantomText is to *find* invisible
or deceiving characters in text they did not write — not to plant them. The product is the detector.

Separately, the 0.1 detector had no way to know whether it worked. `FileScanner` printed findings; nothing
measured whether those findings were correct, complete, or spurious. For a detector, the failure mode that
matters most is not a miss — it is a **false positive**. A tool that flags the zero-width joiner in a
Devanagari conjunct, the ZWNJ in Persian, the RTL mark in Hebrew, or a Vietnamese combining mark will be
switched off within a day, and everything else it could have caught goes with it.

## Decision

**1. The roadmap is re-cut detection-first.** Season 2 is ground truth and spec; Season 3 is the detection
core; formats follow in Season 4; sanitization and the rebuilt attack engine in Season 5. The attack families
remain first-class and public — they are peers of the detector and the mechanism by which it is graded — but
when scope must be cut, detection ships.

**2. Ground truth precedes implementation.** Season 2 produces a taxonomy, a `Finding` schema, a labelled
corpus and an evaluation harness *before* any detector is written. Season 2 contains zero detectors by design.

**3. No detection family may be merged without corpus coverage on both sides.** A family needs positive
samples it must catch **and** benign samples it must not flag. This is now rule 7 in CLAUDE.md and a quality
gate on every arc.

**4. The benign corpus is a first-class deliverable.** It must contain real multilingual text — Persian,
Hindi, Arabic, Hebrew, Vietnamese, Chinese, emoji sequences — where the characters the detector hunts appear
legitimately. Every taxonomy entry carries a legitimate-use note, and that note is what the benign corpus
must exercise.

**5. Precision/recall are gated in CI.** A committed baseline; a regression fails the build.

## Consequences

- Nothing user-visible ships until Season 3. Season 2 produces a spec, data and a measuring instrument, which
  can feel like no progress and is not.
- Every subsequent claim about the detector is defensible with a number, which also serves the paper artifact.
- Corpus maintenance becomes an ongoing cost; new families mean new samples on both sides.
- The corpus is a genuine research asset in its own right and may be publishable separately.

## Alternatives considered

- **Write detectors first, add tests later.** Rejected: this is how the 0.1 scanner reached a state where
  nobody could say whether it worked.
- **Grade only on recall.** Rejected: precision is the survival metric for this class of tool.
- **Reuse the paper's evaluation set.** Rejected as the sole source: it was built to demonstrate attacks, so
  it is dense in positives and near-empty in the benign multilingual text where false positives live.
