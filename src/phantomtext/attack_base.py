from abc import ABC, abstractmethod

class AttackBase(ABC):
    """
    Abstract base class for defining attack families.
    """

    def __init__(self, modality="default", file_format="pdf"):
        """
        Initializes the attack with default modality and file format.

        Args:
            modality (str): The modality of the attack (e.g., "default"). 
            file_format (str): The format of the file (e.g., "pdf"). Default is "pdf".
        """
        self.modality = modality
        self.file_format = file_format

    @abstractmethod
    def apply(self, input_text):
        """
        Abstract method to define the attack technique.

        Args:
            input_text (str): The text to obfuscate.

        Returns:
            str: The obfuscated text.
        """
        pass

    @abstractmethod
    def sanitized(self, input_text):
        """
        Abstract method to sanitize the input text.

        Args:
            input_text (str): The text to sanitize.

        Returns:
            str: The sanitized text.
        """
        pass

    @abstractmethod
    def check(self, input_text):
        """
        Abstract method to check the validity of the input text.

        Args:
            input_text (str): The text to check.

        Returns:
            bool: True if the text is valid, False otherwise.
        """
        pass