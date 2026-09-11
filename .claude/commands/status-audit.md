---
description: Reconcile STATUS.md against what the code and tests actually do
allowed-tools: Bash(uv*), Bash(git*), Read, Edit, Glob, Grep
---

`docs/roadmap/STATUS.md` claims what PhantomText can do. Verify each claim against reality and correct it.

For every non-☐ cell in the matrix, establish which is true:

- **✅ implemented & tested** — there is code *and* a test that would fail if the code broke. Name the test.
- **🟡 works but unverified/partial** — code exists, no test pins it, or it only handles some inputs.
- **🚧 stub/placeholder** — the function exists and does nothing meaningful. Check for bodies that are
  `pass`, bare `return None`, or `NotImplementedError`. The 0.1 audit found several of these behind
  advertised capabilities; that must never recur silently.
- **☐ planned** — no implementation.

Method:

```bash
uv run --no-sync pytest -q --collect-only 2>/dev/null | tail -30
grep -rn "pass$\|NotImplementedError\|TODO\|FIXME" src/phantomtext/ || true
```

Then read the actual implementations. Do not infer a capability from a file name — the 0.1 package had a
`.txt` handler that was never wired to anything and a `font-poisoning.py` that could not even be imported.

Once the corpus and eval harness exist (Season 2), a ✅ additionally requires corpus coverage on **both**
sides — positive samples caught, benign samples not flagged. Cite the precision/recall figure.

Report every discrepancy you find before editing, then update `STATUS.md`. Bias toward the *lower* claim
when uncertain: an honest 🟡 is more useful than an optimistic ✅.
