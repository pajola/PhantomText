# CLAUDE.md — Working conventions & session onboarding

This file is the entry point for any AI/coding session on PhantomText. Read it first, every time.

## What this project is

PhantomText is being rebuilt from a scientific-paper alpha (`phantomtext` 0.1.1 on PyPI) into a
**maintained, production-grade open-source security library**. It handles four capabilities across
plain Unicode text and the PDF / DOCX / HTML file formats:

- **Obfuscation** — hide/alter text with invisible or look-alike Unicode (zero-width, homoglyph, diacritical, bidi, …).
- **Injection** — embed hidden content into documents (zero-size, transparent, out-of-bound, metadata, font poisoning, …).
- **Scanning / detection** — find the above in text or files.
- **Sanitization** — remove it, driven by a configurable security policy.

It accompanies Castagnaro et al., *"The Hidden Threat in Plain Text: Attacking RAG Data Loaders"* (2025, arXiv:2507.05093).

## Non-negotiable working rules

1. **Human-in-the-middle.** The maintainer (Luca) reviews every meaningful decision. Propose → discuss →
   get sign-off → implement. Never implement an unapproved decision. Meaningful = API shape, dependencies,
   layout, naming, dropping a feature, anything a user would notice.
2. **Decisions are recorded as ADRs** in `docs/decisions/`. If a decision isn't in an accepted ADR, it isn't settled.
3. **One arc = one branch = one PR.** Branch name `arc/<NNN>-<slug>`. Keep `main` releasable.
4. **`uv` only** for local envs and tests. No bare `pip`. (`uv venv`, `uv sync`, `uv run pytest`.)
5. **String-first.** The core operates on in-memory `str`; file handlers are a thin layer on top. (ADR-002)
6. **No network at runtime.** Unicode data is vendored offline. (ADR-004)

## The season / arc model

- **Season** — a multi-week milestone with a theme and exit criteria (≈ a minor-version goal). See `docs/roadmap/ROADMAP.md`.
- **Arc** — a single-session-sized unit of work with explicit acceptance criteria. See `docs/roadmap/arcs/`.
- **STATUS** — `docs/roadmap/STATUS.md` is the always-current "what's implemented vs not" matrix.

## Session loop (follow this exactly)

**Start:** read `docs/roadmap/HANDOFF.md`, the active arc file, and any open ADRs. Summarize current state
back to the maintainer before touching anything.

**During:** turn each decision into a short Decision Proposal (options + recommendation). On approval, write/append
an ADR and set its status to Accepted. Do not write code that depends on an un-accepted ADR.

**End:** update `HANDOFF.md` (state, done-this-session, next, open questions), append to the active arc's session log,
update `STATUS.md` if capabilities changed, and update the assistant's persistent memory.

## Repo layout (target — see ADR-001)

```
src/phantomtext/        # the package (src layout)
tests/                  # pytest, offline & deterministic
docs/                   # mkdocs site + roadmap + decisions
  roadmap/              # ROADMAP, STATUS, HANDOFF, arcs/
  decisions/            # ADRs + DECISION-LOG
datasets/               # attack-example corpus generator + sample (see Season 2)
```

## Commands (uv)

```bash
uv venv && uv sync                 # create env + install (incl. dev extras)
uv run pytest                      # run tests (must be offline & deterministic)
uv run ruff check . && uv run ruff format --check .
uv run mypy src/phantomtext
```
