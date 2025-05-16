from phantomtext.content_obfuscation import ContentObfuscator

def main():
    # Create an instance of the ContentObfuscator
    obfuscator = ContentObfuscator()

    # Example sensitive content
    sensitive_content = "My credit card number is 1234-5678-9012-3456."

    # Obfuscate the sensitive content
    obfuscated_content = obfuscator.obfuscate_content(sensitive_content)

    # Print the original and obfuscated content
    print("Original Content:", sensitive_content)
    print("Obfuscated Content:", obfuscated_content)

if __name__ == "__main__":
    main()