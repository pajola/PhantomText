from .attack_base import AttackBase

import numpy as np

class ZeroWidthText(AttackBase):
    """
    An obfuscation attack that uses zero-width characters to obfuscate text.
    """

    def __init__(self, modality="default", file_format="pdf"):
        """
        Initializes the ZeroWidthText attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default"). 
            file_format (str): The format of the file (e.g., "pdf"). Default is "pdf".
        """
        super().__init__(modality, file_format)

        #define the list of malicious symbols
        self.symbols = [
            u"\u200B",  # Zero Width Space
            u"\u200C",  # Zero Width Non-Joiner
            u"\u200D",  # Zero Width Joiner
            u"\u2060",  # Word Joiner
            u"\uFEFF"   # Zero Width No-Break Space
        ]
        self.num_malicius_chars = len(self.symbols)



    def apply(self, input_text):
        """
        Implements the zero-width text obfuscation technique.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text with zero-width characters.
        """
        if self.file_format == "pdf":
            return self._obfuscate_pdf(input_text)
        elif self.file_format == "docx":
            return self._obfuscate_docx(input_text)
        # elif self.file_format == "markdown":
        #     return self._obfuscate_markdown(input_text)
        elif self.file_format == "html":
            return self._obfuscate_html(input_text)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")


    def _obfuscate_docx(self, input_text):
        """
        Obfuscates DOCX text using zero-width characters.
        """
        output = []
        if self.modality == "default":
            #convert text to list
            input_text = list(input_text)
            
            #insert a randomic zero-width character in between each character
            for c in input_text:
                output.append(self.symbols[np.random.randint(0, self.num_malicius_chars-1)]) #add the malicious character
                output.append(c) #add the benign character

            #add a randomic zero-width character at the end            
            output.append(self.symbols[np.random.randint(0, self.num_malicius_chars-1)]) #add the malicious character
        
            #convert list to string
            output = ''.join(output)
        elif self.modality == "heavy": 
            """ This modality inserts 10 zero-width characters between each character. """
            #convert text to list
            input_text = list(input_text)
            
            #insert a randomic zero-width character in between each character
            for c in input_text:
                for _ in range(10): #insert 10 zero-width characters
                    output.append(self.symbols[np.random.randint(0, self.num_malicius_chars-1)]) #add the malicious character
                output.append(c) #add the benign character

            #add a randomic zero-width character at the end            
            for _ in range(10): #insert 10 zero-width characters
                output.append(self.symbols[np.random.randint(0, self.num_malicius_chars-1)]) #add the malicious character
        
            #convert list to string
            output = ''.join(output)            

        else:
            raise ValueError(f"Unsupported modality: {self.modality} for DOCX")
        
        return output
    
    def _obfuscate_pdf(self, input_text):
        """
        Obfuscates pdf text using zero-width characters.
        """
        output = []
        if self.modality == "default":
            #this is identical to the docx implementation
            output = self._obfuscate_docx(input_text)
        elif self.modality == "heavy": 
            #this is identical to the docx implementation
            output = self._obfuscate_docx(input_text)
        else:
            raise ValueError(f"Unsupported modality: {self.modality} for PDF")
        
        return output


    
    def _obfuscate_html(self, input_text):
        """
        Obfuscates HTML text using zero-width characters.
        """
        output = []

        if self.modality == "default":  
            #this is identical to the docx implementation
            output = self._obfuscate_docx(input_text)
        elif self.modality == "heavy": 
            #this is identical to the docx implementation
            output = self._obfuscate_docx(input_text)
        else:
            raise ValueError(f"Unsupported modality: {self.modality} for HTML")
        
        return output
        
    def check(self, input_text):
        """
        Checks if the input text contains zero-width characters.

        Args:
            input_text (str): The text to check.

        Returns:
            bool: True if the text contains zero-width characters, False otherwise.
        """
        # Check for zero-width characters
        return any(c in self.symbols for c in input_text)
    
    def sanitized(self, input_text):
        """
        Sanitizes the input text by removing zero-width characters.

        Args:
            input_text (str): The text to sanitize.

        Returns:
            str: The sanitized text without zero-width characters.
        """
        # Remove zero-width characters
        sanitized_text = ''.join(c for c in input_text if c not in self.symbols)
        return sanitized_text