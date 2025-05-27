from .injection.zerosize_injection import ZeroSizeInjection
import os
PDF_FILE='custom_simple_pdf.pdf'
HTML_FILE='simple_webpage.html'
DOCX_FILE='simple_pdf.docx'
test_folder='test_injection'

if __name__ == "__main__":
    injectorpdfdefault=ZeroSizeInjection('default', 'pdf')
    injectorpdfclosetozero=ZeroSizeInjection('close-to-zero', 'pdf')
    #TEST
    injectorpdfdefault.apply(PDF_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'zerosize-default.pdf')
    injectorpdfclosetozero.apply(PDF_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'zerosize-close-to-zero.pdf')

    injectorhtmldefault=ZeroSizeInjection('default', 'html')
    injectorhtmlclosetozero=ZeroSizeInjection('close-to-zero', 'html')
    #TEST
    injectorhtmldefault.apply(HTML_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'zerosize-default.html')
    injectorhtmlclosetozero.apply(HTML_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'zerosize-close-to-zero.html')

    injectordocxdefault=ZeroSizeInjection('default', 'docx')
    #TEST
    injectordocxdefault.apply(DOCX_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'zerosize-default.docx')

    
    