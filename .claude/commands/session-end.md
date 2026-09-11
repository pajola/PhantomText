---
description: Close a PhantomText session — update state, and guarantee the next session can start unblocked
allowed-tools: Bash(git*), Bash(gh*), Bash(uv*), Read, Edit, Write, Glob, Grep
---

Close this session properly. The single hard requirement: **the next session must be able to start without me
doing anything first.** A session that ends blocked is what stalled this project for five weeks (ADR-010).

## 1. Run the gates

```bash
uv run --no-sync pytest -q
uv run --no-sync ruff check . && uv run --no-sync ruff format --check .
uv run --no-sync mypy src/phantomtext
```

Report failures rather than papering over them. A red gate is a legitimate way to end a session — an
unrecorded red gate is not.

## 2. Update `docs/roadmap/HANDOFF.md`

- **Current position** — season, active arc, branch, review-queue depth
- **Git state**, marked *(verified <today>)* — from actual command output, not from memory
- **Done** — what this session actually landed, one line each, dated
- **>>> START HERE (next session)** — concrete, numbered, and startable with no maintainer action.
  If the only remaining work needs me, say so loudly and give the next session the fallback job:
  prepare the review.
- **Open questions** — Type-1 decisions awaiting my sign-off. Keep this list at four or fewer.

## 3. Update the arc file

Append to its **Session log**: what was decided, what was built, what was learned. Learnings matter most —
they are what a fresh session cannot re-derive.

## 4. Update `docs/roadmap/STATUS.md`

Only if capabilities actually changed. Do not inflate: 🟡 means works-but-unverified, and that is an honest
and useful state.

## 5. Log Type-2 decisions

Append to `docs/decisions/DECISION-LOG.md`:
`YYYY-MM-DD — [T2] <decision> — <one-line rationale>`

## 6. Check the review-queue cap

At most one arc awaiting review. If this session pushed a second, say so explicitly and recommend which one
I should look at first.

## 7. Report

Five lines maximum: what landed, what's next, what needs me (if anything), gate status, queue depth.
