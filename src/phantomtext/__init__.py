"""
PhantomText Toolkit

A Python library for content injection, obfuscation, file scanning, and sanitization
across various document formats including PDF, DOCX, and HTML.
"""

# Import main classes for easy access
# Version information (single-sourced from package metadata; see pyproject.toml)
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

from .content_injection import ContentInjector
from .content_obfuscation import ContentObfuscator
from .file_sanitization import FileSanitizer
from .file_scanning import FileScanner

try:
    __version__ = _version("phantomtext")
except PackageNotFoundError:  # package is not installed (e.g. running from source)
    __version__ = "0.0.0"

__author__ = "Luca Pajola"
__email__ = "lucapajola94@gmail.com"

# Package metadata
__all__ = [
    "ContentInjector",
    "ContentObfuscator",
    "FileScanner",
    "FileSanitizer",
]
