from phantomtext.content_injection import ContentInjector

def main():
    # Create an instance of ContentInjector
    injector = ContentInjector()

    # Example document and content to inject
    document = "This is an example document."
    content = "Injected content goes here."

    # Inject content into the document
    modified_document = injector.inject_content(document, content)

    # Print the modified document
    print("Original Document:")
    print(document)
    print("\nModified Document:")
    print(modified_document)

if __name__ == "__main__":
    main()