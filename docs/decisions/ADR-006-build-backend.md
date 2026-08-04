# ADR-006 — Build backend: Hatchling

- **Status:** Accepted (2026-08-04)
- **Deciders:** Luca (maintainer, deferred choice to assistant), assistant

## Context
ADR-003 committed to a single PEP 621 `pyproject.toml` managed with `uv`, but left the build backend
unspecified. The old setup used setuptools + `setup.py` + `setup_scm`.

## Decision
Use **Hatchling** as the build backend.

- Minimal, PEP 621-native, no `setup.py` needed.
- First-class `src/` layout support; automatically includes package data (the `fonts/*.ttf|*.pkl`) with no
  `MANIFEST.in` or `package-data` gymnastics — verified: fonts are present in the built wheel.
- Works cleanly with `uv`.
- Static version lives in `[project].version`; `__init__.__version__` reads it via `importlib.metadata` (ADR-003, D3).

## Consequences
- `[build-system]` requires `hatchling`; `[tool.hatch.build.targets.wheel] packages = ["src/phantomtext"]`.
- Contributors build/install via `uv` (no direct setuptools invocation).

## Alternatives considered
- **setuptools** (keep) — works, but heavier config and the legacy `setup.py`/`MANIFEST.in` we're removing.
- **PDM-backend / flit** — fine, but hatchling is the most common, best-documented uv-friendly choice.
