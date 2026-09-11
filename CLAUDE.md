# CLAUDE.md — Working conventions & session onboarding

This file is the entry point for any AI/coding session on PhantomText. Read it first, every time.

## What this project is

PhantomText is being rebuilt from a scientific-paper alpha (`phantomtext` 0.1.1 on PyPI) into a
**maintained, production-grade open-source security library**.

**The product is a detector.** The thing a user installs PhantomText to do is *spot invisible or deceiving
characters in text and documents, quickly, under a configuration they control.* Everything else in the
repo exists to make that detector trustworthy or to make it reachable.

Four capabilities, over plain Unicode text and the PDF / DOCX / HTML formats:

- **Scanning / detection** — find hidden or deceptive content. *The product.*
- **Sanitization** — remove it, driven by a configurable security policy. *The product's other half.*
- **Obfuscation** — hide/alter text with invisible or look-alike Unicode. *First-class, and the ground truth the detector is measured against.*
- **Injection** — embed hidden content into documents. *First-class, same role.*

Attacks are not demoted — they are peers of the detector, and they are how we prove the detector works.
But when scope must be cut, detection is what ships.

It accompanies Castagnaro et al., *"The Hidden Threat in Plain Text: Attacking RAG Data Loaders"* (2025, arXiv:2507.05093).

## Non-negotiable working rules

1. **Human-in-the-middle, tiered.** The maintainer (Luca) reviews every *consequential* decision. Not every
   decision. See "The decision tiers" below — this rule was changed in ADR-010 because the untiered version
   stalled the project for five weeks.
2. **Decisions are recorded.** Type-1 decisions become ADRs in `docs/decisions/`. Type-2 decisions become one
   line in `docs/decisions/DECISION-LOG.md`. If a Type-1 decision isn't in an accepted ADR, it isn't settled.
3. **One arc = one branch = one PR.** Branch name `arc/<NNN>-<slug>`. Keep `main` releasable. (ADR-005)
4. **`uv` only** for local envs and tests. No bare `pip`. (`uv venv`, `uv sync`, `uv run pytest`.)
5. **String-first.** The core operates on in-memory `str`; file handlers are a thin layer on top. (ADR-002)
6. **No network at runtime.** Unicode data is vendored offline. (ADR-004)
7. **No detector without ground truth.** A detection family may not be merged before the corpus contains both
   positive samples it must catch and benign samples it must not flag. (ADR-011)
8. **Clean-room core.** The v2 core is written against the spec, not ported from 0.1. `v0.1.1` is tagged and
   stays as the paper artifact. Old code may be *consulted*; it may not be *copied*. (ADR-012)

## The decision tiers

The original rule — "propose → discuss → sign-off → implement, for everything" — produced a queue of eight
batched decisions that needed one contiguous block of maintainer attention, and the project stopped for five
weeks waiting for it. Decisions are now sorted by whether they are reversible.

**Type-1 — one-way doors. Require explicit maintainer sign-off before implementation.**
Anything expensive or embarrassing to undo once released:
- the public API shape (names, signatures, return types of anything exported from `phantomtext`)
- the `Finding` / report schema and any serialized on-disk or on-wire format
- adding, removing or replacing a runtime dependency
- dropping, renaming or breaking a user-visible capability
- licensing, packaging identity, versioning policy
- the detection taxonomy's family IDs (they end up in user config files and CI baselines)

**Type-2 — two-way doors. The assistant decides, logs one line, and proceeds.**
Anything a later arc can change without anyone outside the repo noticing:
- internal module layout, private helper names, file splits
- test structure, fixture organisation, lint rule tweaks
- docstrings, comments, error-message wording
- algorithm choice *behind* a stable interface
- anything explicitly listed as reversible in the arc file

Log Type-2 decisions to `DECISION-LOG.md` as `YYYY-MM-DD — [T2] <decision> — <one-line rationale>`. The
maintainer may veto any of them at PR review; that is the safety net, and it is cheap.

**When in doubt, it is Type-1.** But do not manufacture doubt to avoid deciding.

**Batching limit.** Never present more than **four** Type-1 decisions in one gate. If an arc needs more, it
is too big — split it. A gate that needs an hour of attention will not get it.

## The session must not end blocked

An arc may not be left in a state where the *only* way for the next session to make progress is a maintainer
action. Before ending a session, there must be a next task that a fresh session can start unattended.

**Review-queue cap: at most one arc awaiting review at a time.** If an arc is awaiting review and the maintainer
has not acted, the next session does not open a new arc. Its job is to make the review cheap: produce a diff
summary, the risk notes, the test evidence, and the exact merge command. Piling up four unreviewed arcs is what
happened in Season 1, and it is what killed momentum.

## The season / arc model

- **Season** — a multi-week milestone with a theme and exit criteria (≈ a minor-version goal). See `docs/roadmap/ROADMAP.md`.
- **Arc** — a single-session-sized unit of work with explicit acceptance criteria. See `docs/roadmap/arcs/`.
- **STATUS** — `docs/roadmap/STATUS.md` is the always-current "what's implemented vs not" matrix.
- **HANDOFF** — `docs/roadmap/HANDOFF.md` is live state, and it is **not trusted on sight** (see below).

## Session loop (follow this exactly)

**Step 0 — Verify state before believing it.** `HANDOFF.md` has drifted from reality before (it once told a
session to push a branch that was already merged). Before acting on it, reconcile it against the repo:

```bash
git log --oneline -15 && git status --short && git branch -a
gh pr list --state all --limit 10 2>/dev/null || true
uv run --no-sync pytest -q 2>&1 | tail -5
```

If HANDOFF disagrees with the repo, **the repo is right**. Correct HANDOFF first, say so, then continue.

**Start:** read `HANDOFF.md`, the active arc file, and any ADR with status Proposed. Summarize actual current
state back to the maintainer — including any correction you just made — before touching anything.

**During:** classify each decision as Type-1 or Type-2. Type-2: decide, log, move on. Type-1: write a short
Decision Proposal (options + recommendation + what it costs to reverse), stop, and wait. Do not write code
that depends on an un-accepted Type-1 decision. Do not batch more than four.

**End:** update `HANDOFF.md` (verified state, done-this-session, next-unblocked-task, open questions), append
to the active arc's session log, update `STATUS.md` if capabilities changed, and confirm the review queue is
within cap.

## Repo layout (target — see ADR-001)

```
src/phantomtext/        # the package (src layout)
tests/                  # pytest, offline & deterministic
corpus/                 # ground-truth corpus + generator + JSONL manifests (Season 2)
docs/                   # mkdocs site + roadmap + decisions
  roadmap/              # ROADMAP, STATUS, HANDOFF, arcs/
  decisions/            # ADRs + DECISION-LOG
```

## Commands (uv)

```bash
uv venv && uv sync --extra dev      # create env + install (incl. dev extras)
uv run --no-sync pytest             # run tests (must be offline & deterministic)
uv run --no-sync ruff check . && uv run --no-sync ruff format --check .
uv run --no-sync mypy src/phantomtext
uv run --no-sync python -m phantomtext.eval    # corpus precision/recall (Season 2+)
```

`--no-sync` matters: a bare `uv run` re-syncs and drops the dev extras.

## Quality gates (an arc is not done until all pass)

- [ ] `pytest` green, offline, deterministic (seeded RNG, no network, no clock dependence)
- [ ] `ruff check` and `ruff format --check` clean
- [ ] `mypy src/phantomtext` clean for new code
- [ ] every new detection family has positive **and** benign corpus samples (rule 7)
- [ ] no precision/recall regression against the corpus baseline (Season 2+)
- [ ] `STATUS.md` reflects reality
- [ ] `HANDOFF.md` names a next task that needs no maintainer action
