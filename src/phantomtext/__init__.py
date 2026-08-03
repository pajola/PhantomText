"""
PhantomText Toolkit

A Python library for content injection, obfuscation, file scanning, and sanitization
across various document formats including PDF, DOCX, and HTML.
"""

# Import main classes for easy access
from .content_injection import ContentInjector
from .content_obfuscation import ContentObfuscator
from .file_scanning import FileScanner
from .file_sanitization import FileSanitizer

# Version information
__version__ = "0.1.0"
__author__ = "Luca Pajola"
__email__ = "luca.pajola@example.com"

# Package metadata
__all__ = [
    'ContentInjector',
    'ContentObfuscator', 
    'FileScanner',
    'FileSanitizer',
]