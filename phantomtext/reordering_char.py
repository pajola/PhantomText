from .attack_base import AttackBase
import numpy as np

# Define Unicode Bidi override characters
PDF = chr(0x202C)
LRE = chr(0x202A)
RLE = chr(0x202B)
LRO = chr(0x202D)
RLO = chr(0x202E)

class BidiText(AttackBase):
    """
    An obfuscation attack that uses Unicode Bidi characters to obfuscate text.
    """

    def __init__(self, modality="default", file_format="html"):
        """
        Initializes the BidiText attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default"). 
            file_format (str): The format of the file (e.g., "html"). Default is "html".
        """
        super().__init__(modality, file_format)

        # Define the list of Bidi characters
        self.bidi_chars = [LRO, RLO, LRE, RLE, PDF]
        self.num_bidi_chars = len(self.bidi_chars)

    def apply(self, input_text):
        """
        Implements the Bidi text obfuscation technique.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text with Bidi characters.
        """
        if self.file_format == "html":
            return self._obfuscate_html(input_text)
        elif self.file_format == "docx":
            return self._obfuscate_docx(input_text)
        elif self.file_format == "pdf":
            return self._obfuscate_pdf(input_text)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")

    def _obfuscate_html(self, input_text):
        """
        Obfuscates HTML text using Bidi characters while keeping the visualized text identical.
        """
        output = []

        if self.modality == "default":
            # Wrap each character with Bidi override characters
            for c in input_text:
                output.append(LRO)  # Start Left-to-Right override
                output.append(c)    # Add the actual character
                output.append(PDF)  # End override

            # Convert list to string
            output = ''.join(output)
        elif self.modality == "heavy":
            """ This modality wraps each character with multiple Bidi overrides. """
            for c in input_text:
                for _ in range(5):  # Add multiple Bidi overrides for heavy obfuscation
                    output.append(LRO)  # Start Left-to-Right override
                output.append(c)        # Add the actual character
                for _ in range(5):  # Add multiple Bidi overrides for heavy obfuscation
                    output.append(PDF)  # End override

            # Convert list to string
            output = ''.join(output)
        else:
            raise ValueError(f"Unsupported modality: {self.modality} for HTML")

        return output

    def _obfuscate_docx(self, input_text):
        """
        Obfuscates DOCX text using Bidi characters.
        """
        # Reuse the HTML implementation for DOCX
        return self._obfuscate_html(input_text)

    def _obfuscate_pdf(self, input_text):
        """
        Obfuscates PDF text using Bidi characters.
        """
        # Reuse the HTML implementation for PDF
        return self._obfuscate_html(input_text)

    def check(self, input_text):
        """
        Checks if the input text contains Bidi characters.

        Args:
            input_text (str): The text to check.

        Returns:
            bool: True if the text contains Bidi characters, False otherwise.
        """
        # Check for Bidi characters
        return any(c in self.bidi_chars for c in input_text)

    def sanitized(self, input_text):
        """
        Sanitizes the input text by removing Bidi characters.

        Args:
            input_text (str): The text to sanitize.

        Returns:
            str: The sanitized text without Bidi characters.
        """
        # Remove Bidi characters
        sanitized_text = ''.join(c for c in input_text if c not in self.bidi_chars)
        return sanitized_text