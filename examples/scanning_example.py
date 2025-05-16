from phantomtext.file_scanning import FileScanner

def main():
    scanner = FileScanner()
    file_path = "path/to/your/document.txt"  # Replace with the actual file path
    result = scanner.scan_file(file_path)
    
    if result:
        print("Malicious content detected!")
    else:
        print("File is clean.")

if __name__ == "__main__":
    main()