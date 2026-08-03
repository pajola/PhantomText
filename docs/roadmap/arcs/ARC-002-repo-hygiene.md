# ARC-002 — Repo hygiene

- **Season:** 0
- **Branch:** `arc/002-repo-hygiene` (off `arc/001-governance`; rebase onto `main` after ARC-001 merges)
- **Status:** ◐ in progress (awaiting maintainer review)
- **Depends on:** ARC-001

## Goal
Adopt the `src/` layout (ADR-001) and quarantine dead files & build artifacts, with **no changes to package
source code**, keeping the package installable. Structural only.

## In scope
- Move `phantomtext/` → `src/phantomtext/` (git mv, history preserved).
- Move `test_package.py` → `tests/`; logos → `docs/assets/`; sample docs → `tests/fixtures/`.
- Remove: `test/` (dup), `test.py`, `font-poisoning.py`, `output/`, `dist/`, `*.egg-info/`, all tracked `__pycache__/`.
- Add `.gitignore`.
- Minimal `pyproject.toml` edit: `packages.find where = ["src"]` (stay installable).

## Out of scope (→ ARC-003)
- Deleting `setup.py` / `requirements.txt` / `build_package.sh` / `setup.cfg`.
- Metadata fixes (author email, repo URL), dependency trimming, tooling/CI, version single-sourcing.

## Acceptance criteria
- [x] `src/phantomtext/` holds the full working core (28 files); stubs removed.
- [x] Root free of artifacts; `.gitignore` in place.
- [x] `pyproject` discovers the package under `src/`.
- [ ] Package import/install verified in ARC-003/004 env (deps are broken pins until ARC-003).
- [ ] Maintainer approves PR; merged.

## Session log
- 2026-08-03 — Executed moves/removals on `arc/002-repo-hygiene`. 34 deletions, 54 renames, 1 add, 1 edit.
  Note: existing dep pins in `pyproject.toml` (e.g. `PyPDF2==1.26.0`, `Flask==2.0.1`) are stale/broken and are
  fixed in ARC-003 — a full `uv` install is therefore deferred to ARC-003.
