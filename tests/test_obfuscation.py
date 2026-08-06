"""Obfuscation transforms operate on plain strings, offline and deterministically."""

from __future__ import annotations

import pytest

from phantomtext.content_obfuscation import ContentObfuscator
from phantomtext.obfuscation.diacritical_marks import DiacriticalMarks
from phantomtext.obfuscation.homoglyph_text import HomoglyphText
from phantomtext.obfuscation.reordering_char import BidiText
from phantomtext.obfuscation.zero_width_text import ZeroWidthText

TEXT = "attack at dawn"


@pytest.mark.parametrize("cls", [ZeroWidthText, DiacriticalMarks, BidiText])
def test_apply_check_sanitize_roundtrip(cls):
    atk = cls(modality="default", file_format="html")
    obfuscated = atk.apply(TEXT)

    assert obfuscated != TEXT
    assert atk.check(obfuscated) is True
    assert atk.check(TEXT) is False
    # Sanitizing removes the injected characters and restores the original.
    assert atk.sanitize(obfuscated) == TEXT


def test_zero_width_heavy_modality():
    atk = ZeroWidthText(modality="heavy", file_format="html")
    obfuscated = atk.apply(TEXT)
    assert atk.check(obfuscated)
    assert atk.sanitize(obfuscated) == TEXT


def test_homoglyph_offline_roundtrip():
    atk = HomoglyphText(file_format="html")
    original = "ACEHI"  # all present in the vendored UTS#39 table
    obfuscated = atk.apply(original)
    assert obfuscated != original
    assert all(ord(c) > 127 for c in obfuscated)  # replaced with non-ASCII look-alikes
    assert atk.check(obfuscated) is True
    assert atk.check(original) is False  # plain ASCII is not flagged
    assert atk.sanitize(obfuscated) == original


def test_homoglyph_table_is_offline_and_cached():
    from phantomtext.obfuscation.homoglyph_text import _load_homoglyph_table

    table = _load_homoglyph_table()
    assert table["A"] == ["Α"]  # Greek capital alpha
    assert _load_homoglyph_table() is table  # cached (same object)


def test_content_obfuscator_removes_target():
    # Deprecated 0.1 facade — still works, now over the string-first API.
    with pytest.warns(DeprecationWarning):
        obfuscator = ContentObfuscator()
    content = "Contact me at secret@example.com now."
    target = "secret@example.com"
    # Old camelCase name is accepted but deprecated; canonical names are not.
    with pytest.warns(DeprecationWarning):
        assert target not in obfuscator.obfuscate(
            content, target, obfuscation_technique="zeroWidthCharacter", file_format="html"
        )
    for technique in ["diacritical", "bidi", "homoglyph"]:
        out = obfuscator.obfuscate(
            content, target, obfuscation_technique=technique, file_format="html"
        )
        assert target not in out


def test_content_obfuscator_validation():
    with pytest.warns(DeprecationWarning):
        obfuscator = ContentObfuscator()
    with pytest.raises(ValueError):  # target not contained in source
        obfuscator.obfuscate("abc", "xyz", obfuscation_technique="bidi", file_format="html")
    with pytest.raises(ValueError):  # unsupported file format
        obfuscator.obfuscate("abc", "a", obfuscation_technique="bidi", file_format="rtf")
    with pytest.raises(ValueError):  # unknown technique
        obfuscator.obfuscate("abc", "a", obfuscation_technique="nope", file_format="html")


def test_sanitized_alias_is_deprecated():
    atk = ZeroWidthText(file_format="html")
    obfuscated = atk.apply(TEXT)
    with pytest.warns(DeprecationWarning):
        restored = atk.sanitized(obfuscated)
    assert restored == TEXT


def test_attack_metadata():
    from phantomtext.core.base import InjectionAttack, ObfuscationAttack
    from phantomtext.injection.zerosize_injection import ZeroSizeInjection

    assert issubclass(ZeroWidthText, ObfuscationAttack)
    assert ZeroWidthText.family == "obfuscation"
    assert ZeroWidthText.name == "zero_width"

    assert issubclass(ZeroSizeInjection, InjectionAttack)
    assert ZeroSizeInjection.family == "injection"
    assert ZeroSizeInjection.name == "zero_size"
