from abc import ABC, abstractmethod

class AttackBase(ABC):
    """
    Abstract base class for defining attack families.
    """

    def __init__(self, modality, file_format="pdf"):
        """
        Initializes the attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default"). 
            file_format (str): The format of the file (e.g., "pdf"). Default is "pdf".
        """
        self.modality = modality
        self.file_format = file_format

    @abstractmethod
    def apply(self, input_document, injection, font_size=12, x_coord=100, y_coord=730, image_file=None, output_path=None):
        """
        Abstract method to define the attack technique.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text.
        """
        pass

    @abstractmethod
    def check(self, input_document):
        """
        Abstract method to check if the input document contains an injection.

        Args:
            input_document (str): The document to check.

        Returns:
            bool: True if the document contain an injection, false otherwise.
        """
        pass