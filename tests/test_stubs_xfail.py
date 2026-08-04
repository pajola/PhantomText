"""Behaviors advertised but not yet implemented.

These are marked ``xfail`` (non-strict) so they document the intended contract
and auto-flip to passing once the feature lands in its Season-1/2 arc.
"""

from __future__ import annotations

import pytest

from phantomtext.content_injection import ContentInjector
from phantomtext.file_sanitization import FileSanitizer
from phantomtext.obfuscation.zero_width_text import ZeroWidthText


@pytest.mark.xfail(
    reason="ContentInjector is a stub; the real string-first injection API lands in ARC-103",
    strict=False,
)
def test_content_injector_rejects_unsupported_document():
    with pytest.raises(ValueError):
        ContentInjector().inject_content("file.xyz", "payload")


@pytest.mark.xfail(
    reason="FileSanitizer.sanitize_file is unimplemented; it lands in ARC-203",
    strict=False,
)
def test_file_sanitizer_removes_zero_width(tmp_path):
    payload = ZeroWidthText(file_format="html").apply("hidden")
    p = tmp_path / "malicious.txt"
    p.write_text(payload, encoding="utf-8")

    FileSanitizer().sanitize_file(str(p))

    assert "​" not in p.read_text(encoding="utf-8")
