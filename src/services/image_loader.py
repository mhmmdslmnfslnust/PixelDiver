from PIL import Image


class ImageLoader:
    """
    Responsible only for loading images.

    Future versions will also:
    - resize images
    - convert image formats
    - validate images
    """

    @staticmethod
    def load(path: str):
        return Image.open(path)