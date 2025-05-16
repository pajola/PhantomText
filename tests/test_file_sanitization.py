import unittest
from phantomtext.file_sanitization import FileSanitizer

class TestFileSanitizer(unittest.TestCase):

    def setUp(self):
        self.sanitizer = FileSanitizer()

    def test_sanitize_file_removes_harmful_content(self):
        # Assuming we have a method to create a test file with harmful content
        test_file_path = 'test_harmful_file.txt'
        with open(test_file_path, 'w') as f:
            f.write("This is a test file with harmful content: <script>alert('xss');</script>")

        # Sanitize the file
        self.sanitizer.sanitize_file(test_file_path)

        # Read the sanitized file
        with open(test_file_path, 'r') as f:
            content = f.read()

        # Check that harmful content has been removed
        self.assertNotIn("<script>alert('xss');</script>", content)

    def test_sanitize_file_handles_nonexistent_file(self):
        # Test sanitizing a nonexistent file
        result = self.sanitizer.sanitize_file('nonexistent_file.txt')
        self.assertFalse(result)  # Assuming the method returns False for nonexistent files

    def tearDown(self):
        # Clean up test files if necessary
        import os
        if os.path.exists('test_harmful_file.txt'):
            os.remove('test_harmful_file.txt')

if __name__ == '__main__':
    unittest.main()