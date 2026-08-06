"""Deprecated 0.1 facade — kept as a shim over the string-first API (ADR-009 / H4).

Prefer :func:`phantomtext.scan_file`, which returns a structured ``ScanReport``. This
class preserves the old dict-shaped report for backwards compatibility and is removed at 1.0.
"""

from __future__ import annotations

import os
import warnings
from typing import Any

from tqdm import tqdm

from .api import scan_file as _scan_file

#: Canonical technique name -> the human label used in the legacy dict report.
_LABELS = {
    "diacritical": "Diacritical marks detected.",
    "homoglyph": "Homoglyph characters detected.",
    "bidi": "Bidi characters detected.",
    "zero_width": "Zero-width characters detected.",
}


class FileScanner:
    """Deprecated. Use :func:`phantomtext.scan_file`."""

    def __init__(self) -> None:
        warnings.warn(
            "FileScanner is deprecated and will be removed in 1.0; use phantomtext.scan_file().",
            DeprecationWarning,
            stacklevel=2,
        )

    def scan_file(self, file_path: str) -> dict[str, Any]:
        """Scan a file, returning the legacy dict report (delegates to the new API)."""
        report: dict[str, Any] = {
            "file_path": file_path,
            "malicious_content_found": False,
            "vulnerabilities": [],
        }
        try:
            result = _scan_file(file_path)
            for finding in result.findings:
                report["malicious_content_found"] = True
                report["vulnerabilities"].append(
                    _LABELS.get(finding.technique, f"{finding.technique} detected.")
                )
        except Exception as e:  # noqa: BLE001 (legacy behaviour: report errors, don't raise)
            report["vulnerabilities"].append(f"Error scanning file: {str(e)}")
        return report

    def scan_dir(self, dir_path: str) -> list[dict[str, Any]]:
        """Scan every file under ``dir_path`` and print a summary."""
        reports = []
        for root, _, files in os.walk(dir_path):
            for file_name in tqdm(files, desc="Scanning files", unit="file"):
                reports.append(self.scan_file(os.path.join(root, file_name)))
        self._generate_summary_report(reports)
        return reports

    def _generate_summary_report(self, reports: list[dict[str, Any]]) -> None:
        print("\n📄 Scan Summary Report")
        print("=" * 50)
        for report in reports:
            print(f"📂 File: {report['file_path']}")
            if report["malicious_content_found"]:
                print("  ⚠️ Status: Malicious content found!")
                print("  🛑 Vulnerabilities:")
                for vulnerability in report["vulnerabilities"]:
                    print(f"    - {vulnerability}")
            else:
                print("  ✅ Status: No malicious content detected.")
            print("-" * 50)
