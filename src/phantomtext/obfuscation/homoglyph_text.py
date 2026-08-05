import functools
from importlib import resources

import numpy as np

from ..core.base import ObfuscationAttack


@functools.lru_cache(maxsize=1)
def _load_homoglyph_table() -> dict[str, list[str]]:
    """Parse the vendored Unicode UTS#39 confusables table (offline, cached once).

    Maps each base character to the look-alike glyph(s) it can be replaced with,
    e.g. ``{"A": ["Α"], "C": ["С"]}``. Multi-codepoint sequences are skipped.
    """
    text = resources.files("phantomtext.data").joinpath("intentional.txt").read_text("utf-8-sig")
    mapping: dict[str, list[str]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        data = line.split("#", 1)[0]
        if ";" not in data:
            continue
        src_field, tgt_field = data.split(";", 1)
        src_cps, tgt_cps = src_field.split(), tgt_field.split()
        if len(src_cps) != 1 or len(tgt_cps) != 1:  # skip multi-codepoint sequences
            continue
        try:
            base = chr(int(src_cps[0], 16))
            glyph = chr(int(tgt_cps[0], 16))
        except ValueError:
            continue
        mapping.setdefault(base, []).append(glyph)
    return mapping


class HomoglyphText(ObfuscationAttack):
    """
    An obfuscation attack that uses homoglyph substitution to obfuscate text.
    """

    name = "homoglyph"

    def __init__(self, modality="default", file_format="pdf"):
        """
        Initializes the HomoglyphText attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default").
            file_format (str): The format of the file (e.g., "pdf"). Default is "pdf".
        """
        super().__init__(modality, file_format)

        # Load the vendored Unicode UTS#39 confusables table (offline, cached).
        self.homoglyphs = _load_homoglyph_table()

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

        return "".join(output)

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

    def sanitize(self, input_text):
        """
        Sanitizes the input text by replacing homoglyphs with their base characters.

        Args:
            input_text (str): The text to sanitize.

        Returns:
            str: The sanitized text with homoglyphs replaced by base characters.
        """
        reverse_mapping = {
            glyph: base for base, glyphs in self.homoglyphs.items() for glyph in glyphs
        }
        sanitized_text = "".join(reverse_mapping.get(c, c) for c in input_text)
        return sanitized_text
