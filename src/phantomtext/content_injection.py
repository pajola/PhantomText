class ContentInjector:
    def __init__(self):
        self.injection_techniques = [
            'Camouflage',
            'Out of bound',
            'Transparent',
            'Zero-size',
            'Metadata',
        ]
        pass
    def inject_content(self, document, content):
        """
        Injects the specified content into the given document.
        
        Parameters:
        document (str): The document into which content will be injected.
        content (str): The content to be injected.
        
        Returns:
        str: The document with the injected content.
        """
        # Implementation for injecting content into the document
        # This is a placeholder for actual logic
        return document + "\n" + content
    
    def inject(self, original_document, injection, obfuscation_technique, modality='default', output_document=None):
        
        # Check if document type is either pdf, html or docx
        if not original_document.endswith('.pdf') and not original_document.endswith('.html') and not original_document.endswith('.docx'):
            raise ValueError("Document type must be either pdf, html or docx")
        
        # Check for obfuscation technique type
        if obfuscation_technique not in self.injection_techniques:
            raise ValueError("Invalid obfuscation technique")
        
        
        
        