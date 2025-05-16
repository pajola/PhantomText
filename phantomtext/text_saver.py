from phantomtext.formats.pdf import PDFHandler
from phantomtext.formats.docx import DOCXHandler
from phantomtext.formats.html import HTMLHandler

class TextSaver:
    def __init__(self):
        self.pdf_handler = PDFHandler()
        self.docx_handler = DOCXHandler()
        self.html_handler = HTMLHandler()

    def save_text(self, file_path, text_content):
        """
        Saves text to a given file based on its format.

        Args:
            file_path (str): The path to the file.
            text_content (str): The text content to save.

        Raises:
            ValueError: If the file format is unsupported.
        """
        if file_path.endswith('.pdf'):
            self.pdf_handler.write_pdf(file_path, text_content)
        elif file_path.endswith('.docx'):
            self.docx_handler.write_docx(file_path, text_content)
        elif file_path.endswith('.html'):
            self.html_handler.write_html(file_path, text_content)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
