from PIL import Image


class ImageExporter:

    @staticmethod
    def save(image, filename, scale=1):

        if image is None:
            return

        if scale > 1:

            image = image.resize(

                (
                    image.width * scale,
                    image.height * scale
                ),

                Image.Resampling.NEAREST

            )

        image.save(filename)