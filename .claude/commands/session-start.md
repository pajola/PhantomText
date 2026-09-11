---
description: Open a PhantomText session — verify state against the repo, then report where we actually are
argument-hint: "[optional: ARC id to work on, e.g. ARC-201]"
allowed-tools: Bash(git*), Bash(gh*), Bash(uv*), Read, Glob, Grep
---

Open a work session on PhantomText. Do **Step 0 before anything else** — `HANDOFF.md` has drifted before and
must be verified, not believed.

## Step 0 — Verify

Run these and read the output:

```bash
git log --oneline -15
git status --short
git branch -a
gh pr list --state open --limit 10 2>/dev/null || echo "gh unavailable"
uv run --no-sync pytest -q 2>&1 | tail -5
```

## Step 1 — Read

- `CLAUDE.md` (working rules, decision tiers)
- `docs/roadmap/HANDOFF.md` (claimed state)
- `docs/roadmap/ROADMAP.md` (where this sits in the arc)
- the active arc file in `docs/roadmap/arcs/`
- any ADR in `docs/decisions/` whose status is **Proposed**

## Step 2 — Reconcile

Compare what HANDOFF claims against what the repo shows. **The repo wins.** If they disagree, fix HANDOFF
first, and say explicitly what was wrong. Do not skip this because it looks fine — say what you checked.

## Step 3 — Report back, then stop

Give me, in under 30 lines:

1. **Actual state** — branch, last merged arc, suite result, review-queue depth
2. **Any correction** you just made to HANDOFF
3. **The proposed target for this session** — which arc, and why that one (if I named one in
   `$ARGUMENTS`, use it and say whether it's genuinely unblocked)
4. **Type-1 decisions this arc will need** — listed, not yet argued. Max four. If it needs more, say the arc
   should be split and propose the split.
5. **What you'd do first**

Then stop and wait for me. Do not start implementing.

If the review queue already has an arc in it, do **not** propose opening a new one — propose making that
review cheap instead (see `/arc-ship`).
