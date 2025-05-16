import unittest
from phantomtext.file_scanning import FileScanner

class TestFileScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = FileScanner()

    # def test_scan_file_valid(self):
    #     # Test with a valid file path containing no malicious content
    #     result = self.scanner.scan_file("out/valid_file.txt")
    #     self.assertFalse(result['malicious_content_found'])

    # def test_scan_file_malicious(self):
    #     # Test with a file containing malicious content (e.g., zero-width characters)
    #     result = self.scanner.scan_file("tests/malicious_file.txt")
    #     self.assertTrue(result['malicious_content_found'])

    # def test_scan_file_non_existent(self):
    #     # Test with a non-existent file path
    #     result = self.scanner.scan_file("tests/non_existent_file.txt")
    #     self.assertIn("Error scanning file", result['vulnerabilities'][0])

    def test_scan_output_folder(self):
        # Test scanning the entire './output' folder
        reports = self.scanner.scan_dir("./output")
        self.assertIsInstance(reports, list)  # Ensure the result is a list
        for report in reports:
            self.assertIn("file_path", report)  # Ensure each report has a file path
            self.assertIn("malicious_content_found", report)  # Ensure the key exists
            self.assertIn("vulnerabilities", report)  # Ensure vulnerabilities are listed

if __name__ == "__main__":
    unittest.main()