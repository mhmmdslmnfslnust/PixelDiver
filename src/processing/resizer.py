from PIL import Image


class ImageResizer:

    METHODS = {
        "Nearest": Image.Resampling.NEAREST,
        "Bilinear": Image.Resampling.BILINEAR,
        "Bicubic": Image.Resampling.BICUBIC,
        "Lanczos": Image.Resampling.LANCZOS,
    }

    @classmethod
    def resize(cls, image, width, height, method):

        return image.resize(
            (width, height),
            cls.METHODS[method]
        )