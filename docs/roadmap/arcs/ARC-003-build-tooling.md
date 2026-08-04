# ARC-003 — Build & tooling

- **Season:** 0
- **Branch:** `arc/003-build-tooling` (off `main`)
- **Status:** ◐ in progress (awaiting maintainer review)
- **Depends on:** ARC-002

## Goal
One clean PEP 621 build (Hatchling), correct metadata, trimmed/corrected deps, dev tooling, and CI — with the
`uv` env actually building/installing/importing. Near-zero logic changes.

## Done
- **Build:** rewrote `pyproject.toml` to Hatchling + PEP 621; deleted `setup.py`, `requirements.txt`,
  `build_package.sh`, `MANIFEST.in`; moved `PUBLISHING.md` → `docs/`.
- **Metadata:** author email `example.com` → `lucapajola94@gmail.com`; URLs `lucapajola` → `pajola`;
  version single-sourced (`[project].version = "0.2.0.dev0"`, `__init__.__version__` via `importlib.metadata`).
- **Deps (D4):** dropped **Flask**; unpinned **PyPDF2 → >=3.0** (the `==1.26.0` pin was incompatible with the
  3.x API the code uses); moved **pytest** to a `dev` extra. Kept `requests`/`numpy` (removed in Season 1).
- **Python floor (D2):** `requires-python = ">=3.9"` — verified `uv sync` + import on **3.9.25** and 3.14.
- **Tooling:** `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`; `dev` extra; `.pre-commit-config.yaml`.
- **CI:** `.github/workflows/ci.yml` — ruff lint/format gate + build+import smoke matrix (3.9–3.13).
- **Lint baseline (D6):** ran `ruff format` + safe `--fix` (262 → clean). Fixed 5 real items by hand
  (2× `raise … from e`, 1× `dict()`→`{}`, 2× unused vars). Deferred **E501** (line reflow) to Season-1 rewrites.
- **Fonts:** confirmed packaged in the built wheel by Hatchling.

## Out of scope (later)
- Offline test suite (ARC-004), removing requests/numpy (S1), pypdf migration (S1), typing (mypy stays lenient).

## Acceptance criteria
- [x] `uv sync` + `uv run python -c "import phantomtext"` works (3.9 and 3.14)
- [x] `uv run ruff check .` and `ruff format --check .` pass
- [x] Wheel builds with fonts included
- [x] Metadata corrected; legacy build files removed
- [ ] CI green on GitHub; maintainer approves PR

## Session log
- 2026-08-04 — Executed ARC-003 on `arc/003-build-tooling`.
