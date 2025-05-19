# PhantomText Toolkit

PhantomText is a Python library designed for handling content injection, content obfuscation, file scanning, and file sanitization across various document formats. This toolkit provides a comprehensive set of tools to manage and secure document content effectively.

## Features

- **Content Injection**: Easily inject content into different document formats using the `ContentInjector` class.
- **Content Obfuscation**: Protect sensitive information with the `ContentObfuscator` class, which obfuscates content to prevent unauthorized access.
- **File Scanning**: Scan files for malicious content or vulnerabilities using the `FileScanner` class.
- **File Sanitization**: Sanitize files to remove harmful content with the `FileSanitizer` class.

## Supported Formats

PhantomText supports the following document formats:

- PDF
- DOCX
- HTML

## Installation

To install PhantomText, you can use pip:

```
pip install phantomtext
```

## Usage

### Content Injection Example

```python
from phantomtext.content_injection import ContentInjector

injector = ContentInjector()
injector.inject_content('document.pdf', 'New Content')
```

### Content Obfuscation Example

```python
from phantomtext.content_obfuscation import ContentObfuscator

obfuscator = ContentObfuscator()
obfuscated_content = obfuscator.obfuscate_content('Sensitive Information')
```

#### Supported Obfuscation Attacks

| **Attack Family** | **Attack Name**         | **Variant**   | **HTML** | **DOCX** | **PDF** |
|--------------------|-------------------------|---------------|----------|----------|---------|
| Obfuscation        | diacritical_marks      | default       | ✅        | ✅        | ✅       |
|                    |                        | heavy         | ✅        | ✅        | ✅       |
| Obfuscation        | homoglyph_characters   | default       | ✅        | ✅        | ✅       |
| Obfuscation        | zero_width_characters  | default       | ✅        | ✅        | ✅       |
|                    |                        | heavy         | ✅        | ✅        | ✅       |

### File Scanning Example

```python
from phantomtext.file_scanning import FileScanner

scanner = FileScanner()
scanner.scan_file('document.docx')
```

### File Sanitization Example

```python
from phantomtext.file_sanitization import FileSanitizer

sanitizer = FileSanitizer()
sanitizer.sanitize_file('malicious_file.txt')
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
