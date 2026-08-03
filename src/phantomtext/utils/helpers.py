def validate_file_format(file_path):
    valid_formats = ['.pdf', '.docx', '.txt', '.html']
    return any(file_path.endswith(ext) for ext in valid_formats)