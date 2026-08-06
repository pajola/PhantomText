"""Deprecated FileScanner facade still detects obfuscation via the string-first core."""

from __future__ import annotations

import pytest

from phantomtext.file_scanning import FileScanner
from phantomtext.obfuscation.zero_width_text import ZeroWidthText


def _scanner() -> FileScanner:
    with pytest.warns(DeprecationWarning):
        return FileScanner()


def test_scan_detects_zero_width(tmp_path):
    scanner = _scanner()
    payload = ZeroWidthText(file_format="html").apply("hidden")
    f = tmp_path / "malicious.html"
    f.write_text(f"<html><body><p>{payload}</p></body></html>", encoding="utf-8")

    report = scanner.scan_file(str(f))

    assert report["malicious_content_found"] is True
    assert any("Zero-width" in v for v in report["vulnerabilities"])


def test_scan_clean_file(tmp_path):
    scanner = _scanner()
    f = tmp_path / "clean.html"
    f.write_text("<html><body><p>totally clean text</p></body></html>", encoding="utf-8")

    report = scanner.scan_file(str(f))

    assert report["malicious_content_found"] is False
    assert report["vulnerabilities"] == []


def test_scan_dir_aggregates(tmp_path):
    scanner = _scanner()
    (tmp_path / "a.html").write_text("<p>clean</p>", encoding="utf-8")
    payload = ZeroWidthText(file_format="html").apply("secret")
    (tmp_path / "b.html").write_text(f"<p>{payload}</p>", encoding="utf-8")

    reports = scanner.scan_dir(str(tmp_path))

    assert isinstance(reports, list)
    assert len(reports) == 2
    assert any(r["malicious_content_found"] for r in reports)
