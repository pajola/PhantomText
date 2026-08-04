"""Working injection techniques embed hidden content into real documents."""

from __future__ import annotations

from phantomtext.injection.zerosize_injection import ZeroSizeInjection


def test_zero_size_html_embeds_payload(fixtures_dir, tmp_path):
    out = tmp_path / "injected.html"
    ZeroSizeInjection(file_format="html").apply(
        input_document=str(fixtures_dir / "simple_webpage.html"),
        injection="INJECTED_SECRET",
        output_path=str(out),
    )
    assert out.exists()
    assert "INJECTED_SECRET" in out.read_text(encoding="utf-8")


def test_zero_size_pdf_produces_output(fixtures_dir, tmp_path):
    out = tmp_path / "injected.pdf"
    ZeroSizeInjection(file_format="pdf").apply(
        input_document=str(fixtures_dir / "custom_simple_pdf.pdf"),
        injection="SECRET",
        output_path=str(out),
    )
    assert out.exists()
    assert out.stat().st_size > 0


def test_zero_size_docx_produces_output(fixtures_dir, tmp_path):
    out = tmp_path / "injected.docx"
    ZeroSizeInjection(file_format="docx").apply(
        input_document=str(fixtures_dir / "simple_pdf.docx"),
        injection="SECRET",
        output_path=str(out),
    )
    assert out.exists()
    assert out.stat().st_size > 0
