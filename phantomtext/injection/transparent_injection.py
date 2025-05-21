from ..attack_base_injection import AttackBase

class TransparentInjection(AttackBase):
    def __init__(self, modality="default", file_format="pdf"):
        pass

    def apply(self, input_document, injection, font_size=12, x_coord=100, y_coord=730, image_file=None, output_path=None):
        pass
    
    def check(self, input_document):
        return True