# ADR-010 — Tiered decisions, unblocked handoffs, and a review-queue cap

- **Status:** Accepted (2026-09-10)
- **Deciders:** Luca (maintainer), assistant
- **Amends:** ADR-005 (per-arc branches & PRs), CLAUDE.md rule 1

## Context

Between 2026-08-05 and 2026-09-10 the project made no progress. The cause was not technical — `main` was
clean, CI green, the suite passing. It was the governance model.

Three compounding faults:

1. **Untiered sign-off.** CLAUDE.md rule 1 required maintainer approval for every meaningful decision, with
   "meaningful" defined broadly enough to include reversible internal choices. ARC-103 accumulated eight
   decisions into one gate needing a single contiguous block of maintainer attention. It never arrived.
2. **Sessions ending blocked.** Four arcs stood "done, awaiting review" at once. Every available next action
   required the maintainer, so a session that followed the rules correctly had nothing it could legally start.
3. **A state file that drifted.** `HANDOFF.md` instructed sessions to push and open a PR for `arc/102`, a
   branch already merged into `main`. Sessions that trusted it began from a false premise.

Human-in-the-middle is the right instinct for a security library. Applied without tiering, it became a
single point of failure with a five-week latency.

## Decision

**1. Decisions are tiered by reversibility.**

- **Type-1 (one-way doors)** require explicit maintainer sign-off before implementation: public API shape;
  the `Finding`/report schema and any serialized format; adding, removing or replacing a runtime dependency;
  dropping or breaking a user-visible capability; licensing, packaging identity, versioning policy; and the
  taxonomy's family IDs, which end up in user config files and CI baselines.
- **Type-2 (two-way doors)** are decided by the assistant, logged as one line in `DECISION-LOG.md`, and
  implemented: internal module layout, private naming, test structure, lint tweaks, wording, and algorithm
  choice behind a stable interface.
- Ambiguity resolves to Type-1, but doubt must not be manufactured to avoid deciding.
- The maintainer may veto any Type-2 decision at PR review. That is the safety net, and it is cheap.

**2. A gate carries at most four Type-1 decisions.** An arc needing more is too large and must be split.

**3. A session may not end blocked.** `HANDOFF.md` must always name a next task a fresh session can start
with no maintainer action.

**4. The review queue is capped at one arc.** If an arc awaits review, the next session does not open another.
Its job is to make that review cheap: diff summary, risk notes, test evidence, exact merge command.

**5. `HANDOFF.md` is not trusted on sight.** Step 0 of every session reconciles it against `git log`,
`git status` and `gh pr list`. Where they disagree, the repo wins and HANDOFF is corrected first.

## Consequences

- The maintainer reviews strictly less, and what remains is the set of things genuinely worth his attention.
- Some reversible decisions will be made in a direction he would not have chosen. The PR-review veto and the
  low cost of reversal are the accepted price; the alternative cost five weeks.
- `DECISION-LOG.md` becomes load-bearing and must be kept readable, not a dumping ground.
- Slightly more work at session end (verification, review preparation) in exchange for sessions that can
  always start.

## Alternatives considered

- **Keep the untiered rule but respond faster.** Rejected: it relies on maintainer availability, which is the
  exact variable that failed. A process should not require its scarcest input to be abundant.
- **Remove human-in-the-middle entirely.** Rejected: for a security library, API and schema decisions genuinely
  need the maintainer. The problem was the absence of tiering, not the presence of review.
- **Auto-merge on green CI.** Rejected: CI cannot evaluate whether an API is the right API.
