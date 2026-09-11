"""The Finding/Report schema (ARC-202, ADR-014): a pure data model, no detectors.

Every Finding here is a hand-built fixture -- this arc doesn't produce any
detector, only the shape a future one will emit into.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from phantomtext.core.report import Finding, Provenance, Report, Severity, Span


def _finding(**overrides):
    defaults = {
        "id": "PT.INVIS.ZERO_WIDTH",
        "severity": Severity.HIGH,
        "confidence": 0.9,
        "span": Span(char_start=3, char_end=4),
        "message": "Zero-width space between visible characters",
        "provenance": Provenance(source_kind="string"),
        "remediation": "Remove the zero-width character.",
    }
    defaults.update(overrides)
    return Finding(**defaults)


def test_finding_is_frozen():
    f = _finding()
    with pytest.raises(FrozenInstanceError):
        f.confidence = 0.1
    with pytest.raises(FrozenInstanceError):
        f.made_up_attribute = 1


@pytest.mark.parametrize(
    "bad_id",
    ["zero_width", "pt.invis.zero_width", "PT.INVIS", "PT..ZERO_WIDTH", "PT.invis.ZERO_WIDTH"],
)
def test_finding_rejects_malformed_family_id(bad_id):
    with pytest.raises(ValueError, match="PT.<CLASS>.<FAMILY>"):
        _finding(id=bad_id)


@pytest.mark.parametrize(
    "family_id",
    ["PT.INVIS.ZERO_WIDTH", "PT.DECEIVE.CONFUSABLE", "PT.DOC.OFFPAGE_CLIP"],
)
def test_finding_accepts_real_taxonomy_ids(family_id):
    assert _finding(id=family_id).id == family_id


@pytest.mark.parametrize("bad_confidence", [-0.01, 1.01, 2.0, -1.0])
def test_finding_rejects_out_of_range_confidence(bad_confidence):
    with pytest.raises(ValueError, match="confidence"):
        _finding(confidence=bad_confidence)


@pytest.mark.parametrize("confidence", [0.0, 1.0, 0.5])
def test_finding_accepts_boundary_confidence(confidence):
    assert _finding(confidence=confidence).confidence == confidence


def test_span_rejects_negative_start():
    with pytest.raises(ValueError, match="char_start"):
        Span(char_start=-1, char_end=2)


def test_span_rejects_end_before_start():
    with pytest.raises(ValueError, match="char_end"):
        Span(char_start=5, char_end=2)


def test_span_rejects_partial_utf16_offsets():
    with pytest.raises(ValueError, match="utf16_start"):
        Span(char_start=0, char_end=1, utf16_start=0)


def test_span_accepts_full_utf16_offsets():
    s = Span(char_start=0, char_end=2, utf16_start=0, utf16_end=4)
    assert s.to_dict() == {"char_start": 0, "char_end": 2, "utf16_start": 0, "utf16_end": 4}


def test_span_to_dict_omits_utf16_when_absent():
    s = Span(char_start=0, char_end=2)
    assert s.to_dict() == {"char_start": 0, "char_end": 2}


def test_provenance_to_dict_omits_unset_optional_fields():
    p = Provenance(source_kind="html", page=3)
    assert p.to_dict() == {"source_kind": "html", "page": 3}


def test_finding_to_dict_omits_none_remediation():
    f = _finding(remediation=None)
    assert "remediation" not in f.to_dict()


def test_finding_to_dict_includes_remediation_when_set():
    f = _finding(remediation="Remove it.")
    assert f.to_dict()["remediation"] == "Remove it."


def test_finding_round_trips_through_dict():
    f = _finding()
    assert Finding.from_dict(f.to_dict()) == f


def test_report_round_trips_through_json():
    report = Report(findings=(_finding(), _finding(id="PT.DECEIVE.CONFUSABLE")))
    restored = Report.from_json(report.to_json())
    assert restored == report
    assert restored.schema_version == report.schema_version


def test_report_json_escapes_non_ascii():
    # Deliberate: a report format for invisible/deceiving characters should
    # make every non-ASCII codepoint a visible \uXXXX escape, not pass it
    # through raw where it would once again be invisible in the report itself.
    f = _finding(message="hidden ZWSP: ​ here")
    report = Report(findings=(f,))
    raw = report.to_json()
    assert "​" not in raw
    assert "\\u200b" in raw


def test_empty_report_round_trips():
    report = Report()
    assert Report.from_json(report.to_json()) == report
    assert report.to_dict()["findings"] == []


def test_sarif_export_shape():
    f = _finding()
    report = Report(findings=(f,))
    sarif = report.to_sarif()

    assert sarif["version"] == "2.1.0"
    run = sarif["runs"][0]
    assert run["tool"]["driver"]["name"] == "phantomtext"
    assert {"id": "PT.INVIS.ZERO_WIDTH"} in run["tool"]["driver"]["rules"]

    result = run["results"][0]
    assert result["ruleId"] == f.id
    assert result["level"] == "error"  # Severity.HIGH -> SARIF "error" (ADR-014, D3)
    assert result["message"]["text"] == f.message
    region = result["locations"][0]["physicalLocation"]["region"]
    assert region == {"charOffset": 3, "charLength": 1}
    assert result["properties"]["phantomtext_severity"] == "High"
    assert result["properties"]["confidence"] == f.confidence


@pytest.mark.parametrize(
    ("severity", "expected_level"),
    [
        (Severity.CRITICAL, "error"),
        (Severity.HIGH, "error"),
        (Severity.MEDIUM, "warning"),
        (Severity.LOW, "note"),
    ],
)
def test_sarif_severity_mapping(severity, expected_level):
    f = _finding(severity=severity)
    result = f.to_sarif_result()
    assert result["level"] == expected_level
    # The 4-level value survives losslessly in properties even where the
    # standard SARIF `level` enum collapses Critical and High together.
    assert result["properties"]["phantomtext_severity"] == severity.value


def test_sarif_rules_are_deduplicated_and_sorted():
    report = Report(
        findings=(
            _finding(id="PT.DOC.OFFPAGE_CLIP"),
            _finding(id="PT.INVIS.ZERO_WIDTH"),
            _finding(id="PT.INVIS.ZERO_WIDTH"),
        )
    )
    rule_ids = [r["id"] for r in report.to_sarif()["runs"][0]["tool"]["driver"]["rules"]]
    assert rule_ids == ["PT.DOC.OFFPAGE_CLIP", "PT.INVIS.ZERO_WIDTH"]
