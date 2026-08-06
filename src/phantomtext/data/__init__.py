"""Vendored data shipped with PhantomText.

`intentional.txt` is the Unicode UTS#39 "intentional confusables" table, kept
byte-for-byte as published so it can be audited against upstream:

    https://www.unicode.org/Public/security/latest/intentional.txt

Retrieved 2026-08-05 (file header: Unicode Security Mechanisms, Version 17.0.0,
dated 2025-07-22). Refresh it with:

    python -m phantomtext.data.refresh_homoglyphs
"""
