class ImageExporter:

    @staticmethod
    def save(image, filename):

        if image is None:
            return

        image.save(filename)