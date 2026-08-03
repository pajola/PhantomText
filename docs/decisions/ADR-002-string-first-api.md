# ADR-002 — String-first core API

- **Status:** Accepted (2026-08-03)
- **Deciders:** Luca (maintainer), assistant

## Context
Two use cases must be first-class: (a) users pass **raw Unicode strings** to be checked/transformed inside
normal pipelines (no file on disk); (b) users pass **PDF/DOCX/HTML files**. The 0.1.x API is inconsistent:
`ContentObfuscator.obfuscate(x, y, …)` on strings, `ZeroSizeInjection.apply(input_document, …)` on file paths,
`FileScanner.scan_file(path)` on files — three different shapes, some stubbed.

## Decision
The **core operates on `str`**. Primitive verbs: `scan(text) → Report`, `obfuscate(text, target, …) → str`,
`inject(...)`, `sanitize(text, policy) → str`. **File handling is a thin convenience layer** that reads a
PDF/DOCX/HTML into text (or applies a document-level attack) and delegates to the string core. Both are
first-class and fully supported (file formats are batteries-included per ADR-004).

Document-structure attacks that have no string equivalent (e.g. zero-size injection, metadata, font poisoning)
live in the file layer by nature, but share the same verb names and the same `SecurityPolicy`.

## Consequences
- Clean, testable core (string in / string or Report out); no I/O in the hot path.
- 0.1's `ContentObfuscator` / `ContentInjector` / `FileScanner` get deprecation shims (removed by 1.0).
- Enables trivial batch/parallel wrapping (ARC-106).

## Alternatives considered
- File-path-first API — rejected: forces temp files for pipeline/string use, the primary production case.
