import unittest
from phantomtext.content_injection import ContentInjector

class TestContentInjector(unittest.TestCase):

    def setUp(self):
        self.injector = ContentInjector()

    def test_inject_content_into_pdf(self):
        document = "sample.pdf"
        content = "Injected Content"
        result = self.injector.inject_content(document, content)
        self.assertTrue(result)  # Assuming the method returns True on success

    def test_inject_content_into_docx(self):
        document = "sample.docx"
        content = "Injected Content"
        result = self.injector.inject_content(document, content)
        self.assertTrue(result)

    def test_inject_content_into_txt(self):
        document = "sample.txt"
        content = "Injected Content"
        result = self.injector.inject_content(document, content)
        self.assertTrue(result)

    def test_inject_content_into_html(self):
        document = "sample.html"
        content = "Injected Content"
        result = self.injector.inject_content(document, content)
        self.assertTrue(result)

    def test_inject_content_invalid_document(self):
        document = "invalid_file.xyz"
        content = "Injected Content"
        with self.assertRaises(ValueError):  # Assuming it raises ValueError for unsupported formats
            self.injector.inject_content(document, content)

if __name__ == '__main__':
    unittest.main()