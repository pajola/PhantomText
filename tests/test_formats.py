"""Format loaders read the fixture documents; the txt handler round-trips Unicode."""

from __future__ import annotations

import pytest

from phantomtext.formats.txt import TXTHandler
from phantomtext.text_loader import TextLoader


@pytest.mark.parametrize(
    "filename",
    ["simple_webpage.html", "simple_pdf.docx", "custom_simple_pdf.pdf"],
)
def test_load_text_from_fixtures(fixtures_dir, filename):
    text = TextLoader().load_text(str(fixtures_dir / filename))
    assert isinstance(text, str)
    assert "drugs" in text.lower()


def test_load_text_unsupported_format(tmp_path):
    p = tmp_path / "note.rtf"
    p.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError):
        TextLoader().load_text(str(p))


def test_txt_handler_unicode_roundtrip(tmp_path):
    handler = TXTHandler()
    content = "héllo​world"  # accented + zero-width space preserved
    p = tmp_path / "sample.txt"
    handler.write_txt(str(p), content)
    assert handler.read_txt(str(p)) == content
