"""Ground-truth corpus & generator (ARC-203, ADR-015).

Not part of the ``phantomtext`` package (deliberately outside ``src/``): this
is build-time tooling that produces static, committed corpus artifacts, not
runtime library code. See ADR-012 (clean-room core) for why the generator may
consult and call ``phantomtext.obfuscation.*`` for the families where that
code already produces correct output, without those techniques becoming part
of the shipped library's public surface.
"""
