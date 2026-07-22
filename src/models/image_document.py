from PIL import Image


class ImageDocument:
    """
    Stores the current project.

    Future versions will store:
    - original image
    - resized image
    - processed image
    - palette
    - export settings
    """

    def __init__(self):
        self.original = None
        self.processed = None
        self.filename = None

    def load(self, filename):

        self.filename = filename
        self.original = Image.open(filename)
        self.processed = None