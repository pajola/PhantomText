from phantomtext.formats.pdf import PDFHandler
from phantomtext.formats.docx import DOCXHandler
from phantomtext.formats.html import HTMLHandler

class TextLoader:
    def __init__(self):
        self.pdf_handler = PDFHandler()
        self.docx_handler = DOCXHandler()
        self.html_handler = HTMLHandler()

    def load_text(self, file_path):
        """
        Loads text from a given file based on its format.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The text content of the file.

        Raises:
            ValueError: If the file format is unsupported.
        """
        if file_path.endswith('.pdf'):
            return self.pdf_handler.read_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self.docx_handler.read_docx(file_path)
        elif file_path.endswith('.html'):
            return self.html_handler.read_html(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")