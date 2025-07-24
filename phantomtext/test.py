from .injection.zerosize_injection import ZeroSizeInjection
from .injection.transparent_injection import TransparentInjection
from .injection.outofbound_injection import OutOfBoundInjection
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

    # Transparent Injection Tests
    transparent_injection_default_pdf = TransparentInjection('default', 'pdf')
    transparent_injection_opacity0_pdf = TransparentInjection('opacity-0', 'pdf')
    transparent_injection_opacityclose_pdf = TransparentInjection('opacity-close-to-zero', 'pdf')
    transparent_injection_default_html = TransparentInjection('default', 'html')
    transparent_injection_opacity0_html = TransparentInjection('opacity-0', 'html')
    transparent_injection_opacityclose_html = TransparentInjection('opacity-close-to-zero', 'html')
    transparent_injection_default_docx = TransparentInjection('default', 'docx')
    transparent_injection_vanish_docx = TransparentInjection('vanish', 'docx')

    transparent_injection_default_pdf.apply(PDF_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-default.pdf')
    transparent_injection_opacity0_pdf.apply(PDF_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-opacity-0.pdf')
    transparent_injection_opacityclose_pdf.apply(PDF_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-opacity-close.pdf')
    transparent_injection_default_html.apply(HTML_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-default.html')
    transparent_injection_opacity0_html.apply(HTML_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-opacity-0.html')
    transparent_injection_opacityclose_html.apply(HTML_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-opacity-close.html')
    transparent_injection_default_docx.apply(DOCX_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-default.docx')
    transparent_injection_vanish_docx.apply(DOCX_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'transparent-vanish.docx')          

    #out of bounds injection tests
    out_of_bounds_injection_default_pdf = OutOfBoundInjection('default', 'pdf')
    out_of_bounds_injection_specific_pdf = OutOfBoundInjection('specific-position', 'pdf')
    out_of_bounds_injection_default_html = OutOfBoundInjection('default', 'html')
    out_of_bounds_injection_specific_html = OutOfBoundInjection('specific-position', 'html')
    out_of_bounds_injection_default_docx = OutOfBoundInjection('default', 'docx')
    out_of_bounds_injection_specific_docx = OutOfBoundInjection('specific-position', 'docx') 

    out_of_bounds_injection_default_pdf.apply(PDF_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'outofbounds-default.pdf')
    out_of_bounds_injection_specific_pdf.apply(PDF_FILE, 'INJECTION WORKING',x_coord=100, y_coord=100, output_path=test_folder+'/'+'outofbounds-specific.pdf')    
    out_of_bounds_injection_default_html.apply(HTML_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'outofbounds-default.html')
    out_of_bounds_injection_specific_html.apply(HTML_FILE, 'INJECTION WORKING',x_coord=100, y_coord=100, output_path=test_folder+'/'+'outofbounds-specific.html')
    out_of_bounds_injection_default_docx.apply(DOCX_FILE, 'INJECTION WORKING', output_path=test_folder+'/'+'outofbounds-default.docx')
    out_of_bounds_injection_specific_docx.apply(DOCX_FILE, 'INJECTION WORKING',x_coord=100, y_coord=100, output_path=test_folder+'/'+'outofbounds-specific.docx')

    
    