import unittest
from phantomtext.content_obfuscation import ContentObfuscator
from phantomtext.text_saver import TextSaver

class TestContentObfuscation(unittest.TestCase):

    def setUp(self):
        self.obfuscator = ContentObfuscator()
        self.text_saver = TextSaver()

    def test_obfuscate_and_save_zew(self):
        content = "Sensitive info: email@example.com and phone 123-456-7890."
        target = "email@example.com"

        # --- TEST CASE: Obfuscation ZWC default ---
        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="zeroWidthCharacter", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/zwc_default.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="zeroWidthCharacter", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/zwc_default.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="zeroWidthCharacter", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/zwc_default.docx", obfuscated_content)

        # --- TEST CASE: Obfuscation ZWC heavy ---        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="zeroWidthCharacter", modality="heavy", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/zwc_heavy.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="zeroWidthCharacter", modality="heavy", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/zwc_heavy.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="zeroWidthCharacter", modality="heavy", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/zwc_heavy.docx", obfuscated_content)

    def test_obfuscate_and_save_diacritical(self):
        content = "Sensitive info: email@example.com and phone 123-456-7890."
        target = "email@example.com"

        # --- TEST CASE: Obfuscation diacritical default ---
        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="diacritical", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/diac_default.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="diacritical", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/diac_default.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="diacritical", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/diac_default.docx", obfuscated_content)

        # --- TEST CASE: Obfuscation diacritical heavy ---        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="diacritical", modality="heavy", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/diac_heavy.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="diacritical", modality="heavy", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/diac_heavy.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="diacritical", modality="heavy", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/diac_heavy.docx", obfuscated_content)

    def test_obfuscate_and_save_homo(self):
        content = "Sensitive info: email@example.com and phone 123-456-7890."
        target = "email@example.com"

        # --- TEST CASE: Obfuscation homo default ---
        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="homoglyph", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/homo_default.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="homoglyph", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/homo_default.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="homoglyph", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/homo_default.docx", obfuscated_content)
    
    def test_obfuscate_and_save_bidi(self):
        content = "Sensitive info: email@example.com and phone 123-456-7890."
        target = "email@example.com"

        # --- TEST CASE: Obfuscation Bidi default ---
        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="bidi", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/bidi_default.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="bidi", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/bidi_default.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="bidi", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/bidi_default.docx", obfuscated_content)

        # --- TEST CASE: Obfuscation Bidi heavy ---        
        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="bidi", modality="heavy", file_format="pdf")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/bidi_heavy.pdf", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="bidi", modality="heavy", file_format="html")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/bidi_heavy.html", obfuscated_content)

        obfuscated_content = self.obfuscator.obfuscate(content, target, obfuscation_technique="bidi", modality="heavy", file_format="docx")
        self.assertNotIn("email@example.com", obfuscated_content)
        self.text_saver.save_text("./output/bidi_heavy.docx", obfuscated_content)

    

if __name__ == '__main__':
    unittest.main()

    # python -m unittest tests/test_content_obfuscation.py
