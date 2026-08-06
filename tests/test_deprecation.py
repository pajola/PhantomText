"""The 0.1 facades survive as DeprecationWarning shims over the new API (ADR-009 / H4).

These formerly-stub behaviours now actually work: ``FileSanitizer.sanitize_file`` (was a
no-op ``pass``) and ``ContentInjector`` (was a validate-only stub).
"""

from __future__ import annotations

import pytest

from phantomtext.content_injection import ContentInjector
from phantomtext.content_obfuscation import ContentObfuscator
from phantomtext.file_sanitization import FileSanitizer
from phantomtext.file_scanning import FileScanner
from phantomtext.obfuscation.zero_width_text import ZeroWidthText


def _zero_width_payload(text: str) -> str:
    """Zero-width-obfuscated text, built without a deprecated facade."""
    return ZeroWidthText(file_format="html").apply(text)


@pytest.mark.parametrize("facade", [ContentObfuscator, ContentInjector, FileScanner, FileSanitizer])
def test_facade_construction_warns(facade):
    with pytest.warns(DeprecationWarning):
        facade()


def test_file_sanitizer_removes_zero_width(tmp_path):
    p = tmp_path / "malicious.txt"
    p.write_text(_zero_width_payload("hidden"), encoding="utf-8")

    with pytest.warns(DeprecationWarning):
        result = FileSanitizer().sanitize_file(str(p))

    assert result is True
    assert "​" not in p.read_text(encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "hidden"


def test_content_injector_rejects_unsupported_document():
    with pytest.warns(DeprecationWarning):
        injector = ContentInjector()
    with pytest.warns(DeprecationWarning), pytest.raises(ValueError):
        injector.inject_content("file.xyz", "payload")
