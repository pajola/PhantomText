import PyPDF2

import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

class PDFHandler:
    def read_pdf(self, file_path):
        """
        Reads text from a PDF file.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Extracted text from the PDF.
        """
        text = ""
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        return text

    def write_pdf(self, file_path, content):
        """
        Creates a PDF with a simple structure.
        """
         # --- 1. Register the Unicode Font ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, "../fonts/DejaVuSans.ttf")
        # Make sure the font path is correct and the file exists
        if not os.path.exists(font_path):
            print(f"Error: Font file not found at '{font_path}'")
            print("Please download DejaVuSans.ttf and update the 'font_path'.")
            return

        # Register the font. 'DejaVuSans' is the name we'll use internally in ReportLab.
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

        # --- 2. Create Canvas ---
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter # Get page dimensions

        # --- 3. Set Font and Draw Text ---
        font_name = 'DejaVuSans'
        font_size = 12
        c.setFont(font_name, font_size)

        # Position the text (from bottom-left corner)
        x_margin = 72 # 1 inch margin
        y_position = height - 100 # Start near the top

        # Basic text drawing (single line)
        # c.drawString(x_margin, y_position, text_string)

         # --- Alternative: Draw wrapped text ---
        # For longer text that needs to wrap within margins
        text_object = c.beginText()
        text_object.setTextOrigin(x_margin, y_position)
        text_object.setFont(font_name, font_size)

        # Calculate available width for text
        available_width = width - 2 * x_margin

        # Split the text into lines that fit the available width
        lines = simpleSplit(content, font_name, font_size, available_width)

        for line in lines:
             text_object.textLine(line)

        c.drawText(text_object)
        
        # --- 4. Save the PDF ---
        c.save()

