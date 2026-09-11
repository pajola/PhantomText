---
description: Prepare the current arc for review — gates, diff summary, risk notes, PR body, merge command
allowed-tools: Bash(git*), Bash(gh*), Bash(uv*), Read, Write, Edit, Glob, Grep
---

Make reviewing this arc as cheap as possible for me. Reviewing is the bottleneck that stalled this project
(ADR-010), so the goal here is that I can act in a few minutes, not that the PR merely exists.

## 1. Gates — run them, report honestly

```bash
uv run --no-sync pytest -q
uv run --no-sync ruff check . && uv run --no-sync ruff format --check .
uv run --no-sync mypy src/phantomtext
uv run --no-sync python -m phantomtext.eval 2>/dev/null || echo "eval harness not yet available"
```

If anything is red, stop here and tell me. Do not open a PR on red gates.

## 2. Check the arc's own acceptance criteria

Go through the arc file's checklist item by item and mark each honestly. An unmet criterion is a reason to
either finish it or explicitly descope it in the PR body — never to quietly tick it.

## 3. Diff summary — the part that actually saves me time

```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
```

Then write, in prose:

- **What changed and why**, grouped by intent rather than by file
- **The two or three places I should actually look**, with file and line, and what to look *for*
- **What I should be sceptical of** — the weakest part of this change. If you can't name one, look harder
- **Behaviour changes visible to a user**, if any
- **New dependencies** — if there are any, they were Type-1 and must already have an ADR; link it

## 4. PR body

Write it to a file and open the PR:

```bash
gh pr create --base main --title "<conventional commit title>" --body-file <path>
```

Body must link the arc file and every ADR the arc accepted, and must contain the diff summary from step 3.

## 5. Give me the merge command

The literal command to run once I'm satisfied, so I don't have to look it up.

## 6. Queue check

State the review-queue depth. If this makes two arcs awaiting review, say so — the cap is one, and the next
session must not open a third.
