from phantomtext.file_sanitization import FileSanitizer

def main():
    file_path = "path/to/your/document.txt"  # Replace with your file path
    sanitizer = FileSanitizer()
    
    try:
        sanitizer.sanitize_file(file_path)
        print(f"File '{file_path}' has been sanitized successfully.")
    except Exception as e:
        print(f"An error occurred while sanitizing the file: {e}")

if __name__ == "__main__":
    main()