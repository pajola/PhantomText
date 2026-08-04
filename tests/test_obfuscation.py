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
    obfuscated = atk.apply("cameo")  # a, e, o are in the fake map
    assert obfuscated != "cameo"
    assert atk.check(obfuscated) is True
    assert atk.sanitize(obfuscated) == "cameo"


def test_content_obfuscator_removes_target():
    obfuscator = ContentObfuscator()
    content = "Contact me at secret@example.com now."
    target = "secret@example.com"
    for technique in ["zeroWidthCharacter", "diacritical", "bidi", "homoglyph"]:
        out = obfuscator.obfuscate(
            content, target, obfuscation_technique=technique, file_format="html"
        )
        assert target not in out


def test_content_obfuscator_validation():
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
