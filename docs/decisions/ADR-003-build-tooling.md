# ADR-003 — uv + PEP 621 build & tooling

- **Status:** Accepted (2026-08-03)
- **Deciders:** Luca (maintainer), assistant

## Context
0.1.1 carries a redundant, drifting build setup: `setup.py` + `requirements.txt` + `pyproject.toml` +
`build_package.sh` + `setup.cfg`, with the version hard-coded in three places (0.1.0 vs 0.1.1 mismatch).

## Decision
- **`uv`** is the only supported local env/test tool (`uv venv`, `uv sync`, `uv run …`). No bare `pip` in docs/CI.
- A **single PEP 621 `pyproject.toml`** is the source of truth. **Delete `setup.py`, `requirements.txt`,
  `build_package.sh`, `setup.cfg`.**
- **Single-source the version** (dynamic from the package or a `[project] version`).
- Dev tooling: **ruff** (lint + format), **mypy** (typing), **pytest** (+ coverage), **pre-commit**.
- **CI:** GitHub Actions matrix over supported Python versions; runs ruff/mypy/pytest; tests must be offline.

## Consequences
- One place to edit deps/metadata; reproducible envs via `uv.lock`.
- Contributors need `uv` installed (documented in CONTRIBUTING, Season 4).

## Alternatives considered
- Keep setuptools + pip — rejected: the current duplication is a maintenance hazard.
- Poetry/Hatch — reasonable, but `uv` is the maintainer's chosen tool and is fastest for this workflow.
