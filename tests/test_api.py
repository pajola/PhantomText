"""The string-first public API (ADR-009): verbs, registry, report model, file layer."""

from __future__ import annotations

import pytest

import phantomtext as pt
from phantomtext import Finding, ScanReport, Technique
from phantomtext.core import registry

TEXT = "attack at dawn"


# --------------------------------------------------------------------------- obfuscate


def test_obfuscate_replaces_only_the_target():
    out = pt.obfuscate(TEXT, "dawn", technique="zero_width")
    assert out != TEXT
    assert out.startswith("attack at ")  # prefix untouched
    assert "dawn" not in out  # the target substring is obfuscated


def test_obfuscate_accepts_technique_enum():
    assert pt.obfuscate(TEXT, "dawn", technique=Technique.BIDI) != TEXT


def test_obfuscate_missing_target_raises():
    with pytest.raises(ValueError):
        pt.obfuscate(TEXT, "midnight")


def test_obfuscate_rejects_injection_technique():
    with pytest.raises(ValueError):
        pt.obfuscate(TEXT, "dawn", technique="zero_size")


def test_obfuscate_no_file_format_kwarg():
    # H5: string ops take no file_format; passing it is a TypeError.
    with pytest.raises(TypeError):
        pt.obfuscate(TEXT, "dawn", file_format="pdf")  # type: ignore[call-arg]


def test_deprecated_camelcase_alias_warns():
    with pytest.warns(DeprecationWarning):
        out = pt.obfuscate(TEXT, "dawn", technique="zeroWidthCharacter")
    assert out != TEXT


# --------------------------------------------------------------------------- scan / sanitize


def test_scan_reports_detected_techniques():
    obfuscated = pt.obfuscate(TEXT, "dawn", technique="bidi")
    report = pt.scan(obfuscated)
    assert isinstance(report, ScanReport)
    assert report.clean is False
    assert bool(report) is True
    assert "bidi" in report.techniques
    assert all(isinstance(f, Finding) for f in report.findings)
    assert report.findings[0].family == "obfuscation"


def test_scan_clean_text():
    report = pt.scan("perfectly ordinary text")
    assert report.clean is True
    assert report.techniques == []
    assert not report


def test_sanitize_removes_all_obfuscation():
    obfuscated = pt.obfuscate(TEXT, "dawn", technique="zero_width")
    assert pt.sanitize(obfuscated) == TEXT
    assert pt.scan(pt.sanitize(obfuscated)).clean


# --------------------------------------------------------------------------- registry / enum


def test_registry_lists_families():
    assert set(registry.obfuscation_techniques()) == {
        "zero_width",
        "homoglyph",
        "diacritical",
        "bidi",
    }
    assert "zero_size" in registry.injection_techniques()


def test_registry_resolves_alias_and_enum():
    assert registry.resolve_name(Technique.ZERO_WIDTH) == "zero_width"
    with pytest.warns(DeprecationWarning):
        assert registry.resolve_name("zeroWidthCharacter") == "zero_width"
    with pytest.raises(ValueError):
        registry.resolve_name("nonexistent")


# --------------------------------------------------------------------------- file layer


def test_scan_file_and_sanitize_file_on_txt(tmp_path):
    payload = pt.obfuscate("hidden message", "hidden", technique="zero_width")
    p = tmp_path / "note.txt"
    p.write_text(payload, encoding="utf-8")

    report = pt.scan_file(str(p))
    assert report.source == str(p)
    assert "zero_width" in report.techniques

    # sanitize in place
    returned = pt.sanitize_file(str(p))
    assert returned == "hidden message"
    assert p.read_text(encoding="utf-8") == "hidden message"
    assert pt.scan_file(str(p)).clean


def test_sanitize_file_writes_to_output_path(tmp_path):
    payload = pt.obfuscate("secret data", "secret", technique="bidi")
    src = tmp_path / "in.txt"
    dst = tmp_path / "out.txt"
    src.write_text(payload, encoding="utf-8")

    pt.sanitize_file(str(src), output_path=str(dst))

    assert src.read_text(encoding="utf-8") == payload  # source untouched
    assert dst.read_text(encoding="utf-8") == "secret data"


def test_inject_writes_document(fixtures_dir, tmp_path):
    out = tmp_path / "injected.html"
    result = pt.inject(
        str(fixtures_dir / "simple_webpage.html"),
        "INJECTED_SECRET",
        technique="zero_size",
        output_path=str(out),
    )
    assert result == str(out)
    assert out.exists()
    assert "INJECTED_SECRET" in out.read_text(encoding="utf-8")


def test_inject_unsupported_format_raises(tmp_path):
    bad = tmp_path / "note.txt"
    bad.write_text("hi", encoding="utf-8")
    with pytest.raises(ValueError):
        pt.inject(str(bad), "payload")
