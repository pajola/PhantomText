"""Tests for the ARC-203 ground-truth corpus manifest and generators.

Offline and deterministic (CLAUDE.md quality gates): every assertion here
runs against in-memory generator output or the committed manifest file, with
no network access and no reliance on wall-clock time.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from corpus.generate_corpus import OUTPUT_PATH
from corpus.generators import deceive, invis
from corpus.manifest import CorpusSample, CorpusSpan, dump_manifest, load_manifest

ALL_TEXT_LEVEL_FAMILIES = {
    "PT.INVIS.FORMAT_CHAR",
    "PT.INVIS.ZERO_WIDTH",
    "PT.INVIS.BIDI_CONTROL",
    "PT.INVIS.TAG_CHARS",
    "PT.INVIS.VARIATION_SELECTOR",
    "PT.INVIS.WHITESPACE",
    "PT.INVIS.SOFT_HYPHEN",
    "PT.INVIS.INTERLINEAR_SEPARATOR",
    "PT.DECEIVE.CONFUSABLE",
    "PT.DECEIVE.MIXED_SCRIPT",
    "PT.DECEIVE.HOMOGLYPH",
    "PT.DECEIVE.ZALGO",
    "PT.DECEIVE.STYLED_ALPHANUMERIC",
}


def _generate_all() -> list[CorpusSample]:
    return [*invis.all_samples(), *deceive.all_samples()]


class TestCorpusSpan:
    def test_valid_span(self):
        s = CorpusSpan(2, 5)
        assert s.to_dict() == {"char_start": 2, "char_end": 5}

    def test_negative_start_rejected(self):
        with pytest.raises(ValueError):
            CorpusSpan(-1, 2)

    def test_end_before_start_rejected(self):
        with pytest.raises(ValueError):
            CorpusSpan(5, 2)

    def test_round_trip(self):
        s = CorpusSpan(1, 4)
        assert CorpusSpan.from_dict(s.to_dict()) == s


class TestCorpusSample:
    def test_positive_requires_attacked_text(self):
        with pytest.raises(ValueError, match="attacked_text"):
            CorpusSample(
                id="x",
                family="PT.INVIS.ZERO_WIDTH",
                kind="positive",
                clean_text="a",
                attacked_text=None,
                spans=(CorpusSpan(0, 1),),
                source="generated",
                generator_seed="x",
            )

    def test_positive_requires_spans(self):
        with pytest.raises(ValueError, match="span"):
            CorpusSample(
                id="x",
                family="PT.INVIS.ZERO_WIDTH",
                kind="positive",
                clean_text="a",
                attacked_text="ab",
                spans=(),
                source="generated",
                generator_seed="x",
            )

    def test_span_out_of_bounds_rejected(self):
        with pytest.raises(ValueError, match="out of bounds"):
            CorpusSample(
                id="x",
                family="PT.INVIS.ZERO_WIDTH",
                kind="positive",
                clean_text="a",
                attacked_text="ab",
                spans=(CorpusSpan(0, 10),),
                source="generated",
                generator_seed="x",
            )

    def test_benign_rejects_attacked_text(self):
        with pytest.raises(ValueError, match="must not set attacked_text"):
            CorpusSample(
                id="x",
                family="PT.INVIS.ZERO_WIDTH",
                kind="benign",
                clean_text="a",
                attacked_text="a",
                spans=(),
                source="generated",
                generator_seed="x",
            )

    def test_benign_rejects_spans(self):
        with pytest.raises(ValueError, match="must not carry spans"):
            CorpusSample(
                id="x",
                family="PT.INVIS.ZERO_WIDTH",
                kind="benign",
                clean_text="a",
                attacked_text=None,
                spans=(CorpusSpan(0, 1),),
                source="generated",
                generator_seed="x",
            )

    def test_invalid_family_id_rejected(self):
        with pytest.raises(ValueError, match="PT.<CLASS>.<FAMILY>"):
            CorpusSample(
                id="x",
                family="not-a-family-id",
                kind="benign",
                clean_text="a",
                attacked_text=None,
                spans=(),
                source="generated",
                generator_seed="x",
            )

    def test_invalid_kind_rejected(self):
        with pytest.raises(ValueError, match="kind must be"):
            CorpusSample(
                id="x",
                family="PT.INVIS.ZERO_WIDTH",
                kind="malicious",  # type: ignore[arg-type]
                clean_text="a",
                attacked_text=None,
                spans=(),
                source="generated",
                generator_seed="x",
            )

    def test_round_trip(self):
        sample = CorpusSample(
            id="x",
            family="PT.INVIS.ZERO_WIDTH",
            kind="positive",
            clean_text="ab",
            attacked_text="axb",
            spans=(CorpusSpan(1, 2),),
            source="generated",
            generator_seed="seed",
            locale="fa",
            script="Arab",
        )
        assert CorpusSample.from_dict(sample.to_dict()) == sample


class TestManifestIO:
    def test_dump_and_load_round_trip(self, tmp_path: Path):
        samples = _generate_all()[:5]
        path = tmp_path / "manifest.jsonl"
        dump_manifest(samples, path)
        loaded = load_manifest(path)
        assert loaded == samples

    def test_dump_is_one_json_object_per_line(self, tmp_path: Path):
        samples = _generate_all()[:3]
        path = tmp_path / "manifest.jsonl"
        dump_manifest(samples, path)
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 3
        for line in lines:
            json.loads(line)  # must not raise


class TestGeneratorDeterminism:
    @pytest.mark.parametrize(
        "generate",
        [
            invis.zero_width_samples,
            invis.bidi_control_samples,
            invis.tag_chars_samples,
            invis.variation_selector_samples,
            invis.whitespace_samples,
            invis.soft_hyphen_samples,
            invis.interlinear_separator_samples,
            invis.format_char_samples,
            deceive.confusable_samples,
            deceive.mixed_script_samples,
            deceive.homoglyph_samples,
            deceive.zalgo_samples,
            deceive.styled_alphanumeric_samples,
        ],
    )
    def test_stable_across_runs(self, generate):
        assert generate() == generate()

    def test_no_network_imports(self):
        # ARC-203 in-scope: no network access anywhere in corpus/ (mirrors
        # ADR-004's runtime-offline guarantee for the library itself).
        import corpus.generate_corpus
        import corpus.generators.common
        import corpus.generators.deceive
        import corpus.generators.invis
        import corpus.manifest

        for module in (
            corpus.manifest,
            corpus.generators.common,
            corpus.generators.invis,
            corpus.generators.deceive,
            corpus.generate_corpus,
        ):
            src = Path(module.__file__).read_text(encoding="utf-8")
            for forbidden in ("requests", "urllib.request", "httpx", "socket."):
                assert forbidden not in src, f"{module.__name__} references {forbidden!r}"


class TestFamilyCoverage:
    """CLAUDE.md rule 7's own obligation, self-checked ahead of any detector."""

    def test_every_text_level_family_covered(self):
        samples = _generate_all()
        families = {s.family for s in samples}
        assert families == ALL_TEXT_LEVEL_FAMILIES

    def test_every_family_has_positive_and_benign(self):
        samples = _generate_all()
        by_family: dict[str, set[str]] = {}
        for s in samples:
            by_family.setdefault(s.family, set()).add(s.kind)
        for family, kinds in by_family.items():
            assert kinds == {"positive", "benign"}, f"{family} missing a kind: {kinds}"

    def test_committed_manifest_matches_generators(self):
        """Guards against a stale `corpus/manifests/corpus.jsonl` committed
        out of sync with the generator code that produces it."""
        assert OUTPUT_PATH.exists(), "run `python -m corpus.generate_corpus` first"
        committed = load_manifest(OUTPUT_PATH)
        assert committed == _generate_all()
