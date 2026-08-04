from ..core.base import InjectionAttack


class CamouflageInjection(InjectionAttack):
    name = "camouflage"

    def __init__(self, modality="default", file_format="pdf"):
        pass

    def apply(
        self,
        input_document,
        injection,
        font_size=12,
        x_coord=100,
        y_coord=730,
        image_file=None,
        output_path=None,
    ):
        pass

    def check(self, input_document):
        return False  # TODO(ARC-202): implement injection detection
