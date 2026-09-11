---
description: Run the tiered decision protocol on the open decisions in the active arc
argument-hint: "[optional: decision id, e.g. T1]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

Work the open decisions in the active arc using the tiering rules in `CLAUDE.md` / ADR-010.

## For every open decision, first classify it

**Type-2 (two-way door)** — internal layout, private naming, test structure, wording, algorithm behind a
stable interface. → **Decide it yourself.** Do not ask me. Append one line to
`docs/decisions/DECISION-LOG.md`:
`YYYY-MM-DD — [T2] <decision> — <one-line rationale>` and carry on.

**Type-1 (one-way door)** — public API shape; `Finding`/report schema or any serialized format; a runtime
dependency added, removed or replaced; a user-visible capability dropped or broken; licensing, packaging
identity, versioning; taxonomy family IDs. → Prepare a Decision Proposal and **stop**.

Ambiguous → Type-1. But don't manufacture doubt to avoid deciding.

## Decision Proposal format (Type-1 only)

For each, no more than 200 words:

> **<ID> — <one-line question>**
>
> **Context.** Why this is being decided now, and what depends on it.
>
> **Options.** Two or three, each with its real consequence — not a strawman among them.
>
> **Recommendation.** One, with the reasoning that actually drives it.
>
> **Cost to reverse.** Concretely: what breaks, for whom, and at which release. This is the field that
> justifies the Type-1 label — if the honest answer is "nothing much", it was Type-2, so reclassify it.

## Rules

- **Maximum four Type-1 proposals in one gate.** If the arc needs more, stop and tell me the arc is too big,
  and propose how to split it. This limit is the fix for what stalled ARC-103 — do not exceed it.
- Present all of them at once, then stop. Do not implement anything that depends on an unapproved Type-1.
- On my approval: write the ADR (next free number in `docs/decisions/`), status **Accepted**, dated, with the
  rejected alternatives and *why* they were rejected. Then implement.

If `$ARGUMENTS` names a specific decision, work only that one.
