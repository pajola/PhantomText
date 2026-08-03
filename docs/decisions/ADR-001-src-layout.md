# ADR-001 — `src/` repository layout

- **Status:** Accepted (2026-08-03)
- **Deciders:** Luca (maintainer), assistant

## Context
The 0.1.1 package uses a flat layout (`phantomtext/` at repo root) mixed with dead files (`test.py`,
`font-poisoning.py`), test artifacts (`output/`, stray PDFs/HTML), and build cruft. Flat layouts let tests
import the working tree instead of the installed package, hiding packaging bugs.

## Decision
Adopt the **`src/` layout**: the package lives at `src/phantomtext/`. The public import name stays `phantomtext`
(no breakage for users). Non-package material is relocated: tests → `tests/`, docs → `docs/`, datasets →
`datasets/`, examples → `examples/`. Dead/ambiguous files are quarantined out of the package in ARC-002.

## Consequences
- Tests run against the installed package → packaging bugs surface early.
- Every internal import path changes; done atomically in ARC-002.
- `pyproject.toml` uses `tool.setuptools.packages.find` with `where = ["src"]` (or hatchling).

## Alternatives considered
- Keep flat layout — rejected: perpetuates import-vs-install ambiguity and the current mess.
