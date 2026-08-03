# ADR-004 — Batteries-included dependencies

- **Status:** Accepted (2026-08-03)
- **Deciders:** Luca (maintainer), assistant

## Context
Sending PDF/DOCX/HTML files is a **first-class, expected capability**, not an add-on. Separately, the raw-string
pipeline use case is served by the API design (ADR-002), not by the install shape. 0.1.1 also lists deps it
doesn't need for the core (`Flask`, `requests`).

## Decision
- **Batteries-included default install.** `pip install phantomtext` (or `uv add phantomtext`) pulls the file-format
  stack so all four formats work immediately: `PyPDF2`/pypdf, `python-docx`, `beautifulsoup4`, `lxml`, `reportlab`.
- **Drop `Flask` entirely** (unused).
- **Drop `requests`** — the only use is the runtime homoglyph fetch, which is replaced by **vendored offline
  Unicode data** (ARC-102). No network at runtime.
- **Drop `numpy`** as a hard dep if the only use is trivial random choice (use stdlib `random`); re-add only if a
  real numerical need appears.

## Consequences
- Simple, obvious UX; heavier install for string-only users (acceptable; revisitable).
- A future slim `[core]`/extras split remains possible — this ADR can be superseded if pipeline users ask.

## Alternatives considered
- Optional extras (`phantomtext[pdf]` …) — rejected for now: makes the expected file-format capability a
  second step and a source of `ImportError` confusion.
