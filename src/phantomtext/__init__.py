"""
PhantomText Toolkit

A string-first library for Unicode/text obfuscation, document injection, scanning,
and sanitization across plain text and the PDF / DOCX / HTML formats.

The recommended surface is the top-level verbs::

    import phantomtext as pt

    pt.obfuscate(text, target, technique="zero_width")   # str -> str
    pt.scan(text)                                         # str -> ScanReport
    pt.sanitize(text)                                     # str -> str
    pt.inject(path, payload, technique="zero_size", output_path=...)   # document-level
    pt.scan_file(path); pt.sanitize_file(path, output_path=...)        # file wrappers

The 0.1 facade classes (``ContentObfuscator``, ``ContentInjector``, ``FileScanner``,
``FileSanitizer``) remain importable as deprecation shims and are removed at 1.0.
"""

# Version information (single-sourced from package metadata; see pyproject.toml)
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

# String-first public API (ADR-009) plus the 0.1 facade shims (each of which imports the
# new API directly, so import order here is irrelevant).
from .api import inject, obfuscate, sanitize, sanitize_file, scan, scan_file
from .content_injection import ContentInjector
from .content_obfuscation import ContentObfuscator
from .core.registry import Technique
from .core.report import Finding, ScanReport
from .file_sanitization import FileSanitizer
from .file_scanning import FileScanner

try:
    __version__ = _version("phantomtext")
except PackageNotFoundError:  # package is not installed (e.g. running from source)
    __version__ = "0.0.0"

__author__ = "Luca Pajola"
__email__ = "lucapajola94@gmail.com"

__all__ = [
    # string-first verbs
    "obfuscate",
    "scan",
    "sanitize",
    "inject",
    "scan_file",
    "sanitize_file",
    # supporting types
    "Technique",
    "ScanReport",
    "Finding",
    # deprecated 0.1 facades
    "ContentInjector",
    "ContentObfuscator",
    "FileScanner",
    "FileSanitizer",
]
