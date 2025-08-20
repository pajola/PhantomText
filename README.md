# PhantomText Toolkit

<img src="./phantomText.jpg" alt="image info" width="200"/>

PhantomText is a Python library designed for handling content injection, content obfuscation, file scanning, and file sanitization across various document formats. This toolkit provides a comprehensive set of tools to manage and secure document content effectively.

## Features

- **Content Injection**: Easily inject content into different document formats using various steganographic techniques like zero-size text, transparent text, and out-of-bound positioning.
- **Content Obfuscation**: Protect sensitive information with advanced obfuscation techniques including zero-width characters, homoglyphs, diacritical marks, and bidirectional text reordering.
- **File Scanning**: Scan files for malicious content or vulnerabilities using the `FileScanner` class that detects obfuscated and injected content.
- **File Sanitization**: Sanitize files to remove harmful content with the `FileSanitizer` class.

## Attack Families

### Obfuscation Attacks
- **Zero-Width Characters**: Uses invisible Unicode characters (Zero Width Space, Zero Width Non-Joiner, etc.) to obfuscate text
- **Homoglyph Characters**: Replaces characters with visually similar Unicode characters from different scripts
- **Diacritical Marks**: Adds combining diacritical marks to characters to alter their appearance
- **Bidi/Reordering**: Uses Unicode bidirectional override characters to manipulate text direction and rendering

### Injection Attacks
- **Zero-Size Injection**: Injects content using zero or near-zero font sizes to make text invisible
- **Transparent Injection**: Injects content using transparent colors or opacity settings
- **Camouflage Injection**: (In development) Hides content by matching background colors or patterns
- **Out-of-Bound Injection**: (In development) Places content outside visible document boundaries
- **Metadata Injection**: (In development) Embeds content in document metadata

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

# Basic obfuscation
obfuscated_content = obfuscator.obfuscate_content('Sensitive Information')

# Advanced obfuscation with specific techniques
content = "Sensitive info: email@example.com and phone 123-456-7890."
target = "email@example.com"

# Zero-width character obfuscation
obfuscated = obfuscator.obfuscate(content, target, 
                                  obfuscation_technique="zeroWidthCharacter", 
                                  modality="default", 
                                  file_format="html")

# Homoglyph character obfuscation
obfuscated = obfuscator.obfuscate(content, target, 
                                  obfuscation_technique="homoglyph", 
                                  file_format="pdf")

# Diacritical marks obfuscation
obfuscated = obfuscator.obfuscate(content, target, 
                                  obfuscation_technique="diacritical", 
                                  modality="heavy", 
                                  file_format="docx")

# Bidi/reordering character obfuscation
obfuscated = obfuscator.obfuscate(content, target, 
                                  obfuscation_technique="bidi", 
                                  modality="default", 
                                  file_format="html")
```

### Content Injection Example

```python
from phantomtext.injection.zerosize_injection import ZeroSizeInjection
from phantomtext.injection.transparent_injection import TransparentInjection

# Zero-size injection
injector = ZeroSizeInjection(modality="default", file_format="pdf")
injector.apply(input_document="document.pdf", 
               injection="Hidden content", 
               output_path="injected_document.pdf")

# Transparent injection
injector = TransparentInjection(modality="opacity-0", file_format="html")
injector.apply(input_document="document.html", 
               injection="Invisible text", 
               output_path="injected_document.html")
```

#### Supported Attacks

##### Obfuscation Attacks

| **Attack Family** | **Attack Name**           | **Variant**   | **HTML** | **DOCX** | **PDF** |
|-------------------|---------------------------|---------------|----------|----------|---------|
| Obfuscation       | diacritical_marks         | default       | ✅        | ✅        | ✅       |
|                   |                           | heavy         | ✅        | ✅        | ✅       |
| Obfuscation       | homoglyph_characters      | default       | ✅        | ✅        | ✅       |
| Obfuscation       | zero_width_characters     | default       | ✅        | ✅        | ✅       |
|                   |                           | heavy         | ✅        | ✅        | ✅       |
| Obfuscation       | bidi_reordering           | default       | ✅        | ✅        | ✅       |
|                   |                           | heavy         | ✅        | ✅        | ✅       |

##### Injection Attacks

| **Attack Family** | **Attack Name**           | **Variant**          | **HTML** | **DOCX** | **PDF** |
|-------------------|---------------------------|----------------------|----------|----------|---------|
| Injection         | zero_size                 | default              | ✅        | ✅        | ✅       |
|                   |                           | close-to-zero        | ✅        | ❌        | ✅       |
| Injection         | transparent               | default              | ✅        | ✅        | ✅       |
|                   |                           | opacity-0            | ✅        | ❌        | ✅       |
|                   |                           | opacity-close-to-zero| ✅        | ❌        | ✅       |
|                   |                           | vanish               | ❌        | ✅        | ❌       |
| Injection         | camouflage                | default              | 🚧        | 🚧        | 🚧       |
| Injection         | out_of_bound              | default              | 🚧        | 🚧        | 🚧       |
| Injection         | metadata                  | default              | 🚧        | 🚧        | 🚧       |

**Legend:**
- ✅ Implemented and working
- ❌ Not supported for this format
- 🚧 Placeholder implementation (not yet functional)

### File Scanning Example

```python
from phantomtext.file_scanning import FileScanner

scanner = FileScanner()

# Scan a single file
result = scanner.scan_file('document.docx')
print(f"Malicious content found: {result['malicious_content_found']}")
print(f"Vulnerabilities: {result['vulnerabilities']}")

# Scan an entire directory
reports = scanner.scan_dir('./output')
for report in reports:
    if report['malicious_content_found']:
        print(f"⚠️ Issues found in {report['file_path']}")
        for vulnerability in report['vulnerabilities']:
            print(f"  - {vulnerability}")
```

### Detection Capabilities

The FileScanner can detect the following obfuscation techniques:
- Zero-width character sequences
- Homoglyph character substitutions  
- Diacritical mark insertions
- Bidirectional text overrides

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
