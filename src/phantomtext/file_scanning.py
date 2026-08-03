from phantomtext.text_loader import TextLoader
from phantomtext.obfuscation.zero_width_text import ZeroWidthText
from phantomtext.obfuscation.homoglyph_text import HomoglyphText
from phantomtext.obfuscation.diacritical_marks import DiacriticalMarks
from phantomtext.obfuscation.reordering_char import BidiText

from tqdm import tqdm
import os

class FileScanner:
    def __init__(self):
        self.text_loader = TextLoader()
        self.bidi_checker = BidiText()
        self.diacritical_checker = DiacriticalMarks()
        self.zero_width_checker = ZeroWidthText()
        self.homoglyph_checker = HomoglyphText()

    def scan_file(self, file_path):
        """
        Scans the specified file for malicious content or vulnerabilities.

        Args:
            file_path (str): Path to the file to be scanned.

        Returns:
            dict: A report indicating the presence of any malicious content or vulnerabilities.
        """
        report = {
            "file_path": file_path,
            "malicious_content_found": False,
            "vulnerabilities": []
        }

        try:
            # Load the text from the file
            text = self.text_loader.load_text(file_path)

            # Check for diacritics
            if self.diacritical_checker.check(text):
                report["malicious_content_found"] = True
                report["vulnerabilities"].append("Diacritical marks detected.")

            # Check for homoglyphs characters
            if self.homoglyph_checker.check(text):
                report["malicious_content_found"] = True
                report["vulnerabilities"].append("Homoglyph characters detected.")

            # Check for Bidi characters
            if self.bidi_checker.check(text):
                report["malicious_content_found"] = True
                report["vulnerabilities"].append("Bidi characters detected.")


            # Check for zero-width characters
            if self.zero_width_checker.check(text):
                report["malicious_content_found"] = True
                report["vulnerabilities"].append("Zero-width characters detected.")

        except Exception as e:
            report["vulnerabilities"].append(f"Error scanning file: {str(e)}")

        return report

    def scan_dir(self, dir_path):
        """
        Scans all files in the specified directory for malicious content or vulnerabilities.

        Args:
            dir_path (str): Path to the directory to be scanned.

        Returns:
            list: A list of reports for each file scanned.
        """
        reports = []

        # Iterate over all files in the directory using tqdm for a progress bar
        for root, _, files in os.walk(dir_path):
            for file_name in tqdm(files, desc="Scanning files", unit="file"):
                file_path = os.path.join(root, file_name)
                report = self.scan_file(file_path)
                reports.append(report)

        # Generate a visually appealing summary report
        self._generate_summary_report(reports)
        return reports

    def _generate_summary_report(self, reports):
        """
        Generates a visually appealing summary report with emojis.

        Args:
            reports (list): List of individual file scan reports.
        """
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