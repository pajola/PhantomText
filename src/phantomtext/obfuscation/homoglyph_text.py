import requests
import numpy as np
from ..attack_base import AttackBase

class HomoglyphText(AttackBase):
    """
    An obfuscation attack that uses homoglyph substitution to obfuscate text.
    """

    def __init__(self, modality="default", file_format="pdf"):
        """
        Initializes the HomoglyphText attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default"). 
            file_format (str): The format of the file (e.g., "pdf"). Default is "pdf".
        """
        super().__init__(modality, file_format)

        # Retrieve Unicode intentional homoglyph characters
        self.homoglyphs = self._load_homoglyphs()

    def _load_homoglyphs(self):
        """
        Loads intentional homoglyph mappings from Unicode.

        Returns:
            dict: A dictionary mapping base characters to their homoglyphs.
        """
        intentionals = dict()
        int_resp = requests.get("https://www.unicode.org/Public/security/latest/intentional.txt", stream=True)
        for line in int_resp.iter_lines():
            if len(line):
                line = line.decode('utf-8-sig')
                if line[0] != '#':
                    line = line.replace("#*", "#")
                    _, line = line.split("#", maxsplit=1)
                    if line[3] not in intentionals:
                        intentionals[line[3]] = []
                    intentionals[line[3]].append(line[7])
        return intentionals

    def apply(self, input_text):
        """
        Implements the homoglyph substitution obfuscation technique.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text with homoglyph substitutions.
        """
        if self.file_format == "pdf":
            return self._obfuscate_pdf(input_text)
        elif self.file_format == "docx":
            return self._obfuscate_docx(input_text)
        elif self.file_format == "html":
            return self._obfuscate_html(input_text)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")

    def _obfuscate_docx(self, input_text):
        """
        Obfuscates DOCX text using homoglyph substitution.
        """
        return self._apply_homoglyphs(input_text)

    def _obfuscate_pdf(self, input_text):
        """
        Obfuscates PDF text using homoglyph substitution.
        """
        return self._apply_homoglyphs(input_text)

    def _obfuscate_html(self, input_text):
        """
        Obfuscates HTML text using homoglyph substitution.
        """
        return self._apply_homoglyphs(input_text)

    def _apply_homoglyphs(self, input_text):
        """
        Applies homoglyph substitution to the input text.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text with homoglyph substitutions.
        """
        output = []
        for char in input_text:
            if char in self.homoglyphs:
                output.append(np.random.choice(self.homoglyphs[char]))
            else:
                # Keep the character as is if no homoglyph is available
                output.append(char)

        return ''.join(output)

    def check(self, input_text):
        """
        Checks if the input text contains homoglyph substitutions.

        Args:
            input_text (str): The text to check.

        Returns:
            bool: True if the text contains homoglyph substitutions, False otherwise.
        """
        homoglyph_set = {glyph for glyphs in self.homoglyphs.values() for glyph in glyphs}
        return any(c in homoglyph_set for c in input_text)

    def sanitized(self, input_text):
        """
        Sanitizes the input text by replacing homoglyphs with their base characters.

        Args:
            input_text (str): The text to sanitize.

        Returns:
            str: The sanitized text with homoglyphs replaced by base characters.
        """
        reverse_mapping = {glyph: base for base, glyphs in self.homoglyphs.items() for glyph in glyphs}
        sanitized_text = ''.join(reverse_mapping.get(c, c) for c in input_text)
        return sanitized_text