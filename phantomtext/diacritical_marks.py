from .attack_base import AttackBase

import numpy as np

class DiacriticalMarks(AttackBase):
    """
    An obfuscation attack that uses diacritical marks to obfuscate text.
    """

    def __init__(self, modality="default", file_format="pdf"):
        """
        Initializes the DiacriticalMarksText attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default"). 
            file_format (str): The format of the file (e.g., "pdf"). Default is "pdf".
        """
        super().__init__(modality, file_format)

        # Define the list of diacritical marks
        self.diacritical_marks = [
            u"\u0300",  # Grave Accent
            u"\u0301",  # Acute Accent
            u"\u0302",  # Circumflex
            u"\u0303",  # Tilde
            u"\u0304",  # Macron
            u"\u0305",  # Overline
            u"\u0306",  # Breve
            u"\u0307",  # Dot Above
            u"\u0308",  # Diaeresis
            u"\u0309",  # Hook Above
            u"\u030A",  # Ring Above
        ]
        self.num_diacritical_marks = len(self.diacritical_marks)

    def apply(self, input_text):
        """
        Implements the diacritical marks obfuscation technique.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text with diacritical marks.
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
        Obfuscates DOCX text using diacritical marks.
        """
        output = []
        if self.modality == "default":
            # Split text into words
            words = input_text.split()
            
            # Insert a random diacritical mark in each word
            for word in words:
                if len(word) > 2:
                    diacritical = self.diacritical_marks[np.random.randint(0, self.num_diacritical_marks)]
                    insert_position = np.random.randint(1, len(word) -1)
                    obfuscated_word = word[:insert_position] + diacritical + word[insert_position:]
                    output.append(obfuscated_word)
                else:
                    # If the word is too short, just append it without obfuscation
                    output.append(word)
            
            # Join words back into a string
            output = ' '.join(output)
        elif self.modality == "heavy":
            """ This modality inserts multiple diacritical marks in each word. """
            words = input_text.split()
            
            for word in words:
                obfuscated_word = word
                diacritical = self.diacritical_marks[np.random.randint(0, self.num_diacritical_marks)]
                insert_position = np.random.randint(1, len(word) -1)
                obfuscated_word = word[:insert_position] + ''.join([diacritical] * 10) + word[insert_position:]
                output.append(obfuscated_word)
                
            output = ' '.join(output)
        else:
            raise ValueError(f"Unsupported modality: {self.modality} for DOCX")
        
        return output

    def _obfuscate_pdf(self, input_text):
        """
        Obfuscates PDF text using diacritical marks.
        """
        # This is identical to the DOCX implementation
        return self._obfuscate_docx(input_text)

    def _obfuscate_html(self, input_text):
        """
        Obfuscates HTML text using diacritical marks.
        """
        # This is identical to the DOCX implementation
        return self._obfuscate_docx(input_text)

    def check(self, input_text):
        """
        Checks if the input text contains diacritical marks.

        Args:
            input_text (str): The text to check.

        Returns:
            bool: True if the text contains diacritical marks, False otherwise.
        """
        # Check for diacritical marks
        return any(c in self.diacritical_marks for c in input_text)
    
    def sanitized(self, input_text):
        """
        Sanitizes the input text by removing diacritical marks.

        Args:
            input_text (str): The text to sanitize.

        Returns:
            str: The sanitized text without diacritical marks.
        """
        # Remove diacritical marks
        sanitized_text = ''.join(c for c in input_text if c not in self.diacritical_marks)
        return sanitized_text