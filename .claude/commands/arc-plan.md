---
description: Draft or refresh an arc file from the roadmap, sized for a single session
argument-hint: "ARC-NNN [short description of what it should cover]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

Draft the arc file for **$ARGUMENTS** at `docs/roadmap/arcs/ARC-NNN-<slug>.md`, using
`docs/roadmap/arcs/_TEMPLATE.md`.

## Before writing

- Read the arc's entry in `docs/roadmap/ROADMAP.md` — that is the contract, don't drift from it
- Read every ADR it depends on
- Read `docs/spec/TAXONOMY.md` if it exists and the arc touches detection
- Check whether a superseded arc carried decisions forward into this one (see ADR-009) and pull them in

## Sizing — the important constraint

An arc is **one session's work**. If the draft cannot plausibly be finished, reviewed and merged in one
sitting, it is too big. Split it and say so rather than writing an arc nobody can close.

Concretely, an arc is too big if it has more than four Type-1 decisions, touches more than one season's
theme, or its acceptance criteria run past about ten items.

## Then write

Fill the template properly:

- **Goal** — one paragraph, what "done" looks like and why it matters
- **In / out of scope** — the out-of-scope list is what keeps the arc closable; be specific and name the arc
  that picks each item up
- **Decisions needed** — with the Tier column filled honestly. Type-2 rows do not need my attention; do not
  inflate them to Type-1 to be safe
- **Acceptance criteria** — checkable, not aspirational. Include the standing gates from the template
- **Depends on** — and state plainly whether this arc is startable unattended today

Write the file, then summarize in five lines: goal, the Type-1 decisions, whether it is unblocked, and your
estimate of whether it truly fits one session.
