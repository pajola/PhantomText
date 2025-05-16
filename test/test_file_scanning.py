from phantomtext.file_scanning import FileScanner

def test_scan_output_folder():
    """
    Test function to scan the 'output' folder for malicious content or vulnerabilities.
    """
    # Initialize the FileScanner
    scanner = FileScanner()

    # Define the folder to scan
    output_folder = "output"

    # Perform the scan
    print(f"Scanning folder: {output_folder}")
    reports = scanner.scan_dir(output_folder)

    # Print the summary report
    print("\nTest completed. Summary report:")
    for report in reports:
        print(report)

# Run the test function
if __name__ == "__main__":
    test_scan_output_folder()