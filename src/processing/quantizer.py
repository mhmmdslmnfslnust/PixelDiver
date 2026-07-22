from PIL import Image


class ColorQuantizer:

    @staticmethod
    def color_distance(c1, c2):
        """
        Squared Euclidean distance in RGB.
        No sqrt() needed because we only compare distances.
        """

        return (
            (c1[0] - c2[0]) ** 2 +
            (c1[1] - c2[1]) ** 2 +
            (c1[2] - c2[2]) ** 2
        )

    @classmethod
    def nearest_color(cls, color, palette):

        best = palette[0]
        best_distance = cls.color_distance(color, best)

        for candidate in palette[1:]:

            distance = cls.color_distance(color, candidate)

            if distance < best_distance:
                best_distance = distance
                best = candidate

        return best

    @classmethod
    def quantize(
        cls,
        image,
        palette,
        dithering=False
    ):
        """
        Currently ignores dithering.

        That will be implemented in Phase 7.
        """

        image = image.convert("RGB")

        output = Image.new(
            "RGB",
            image.size
        )

        width, height = image.size

        for y in range(height):

            for x in range(width):

                pixel = image.getpixel((x, y))

                nearest = cls.nearest_color(
                    pixel,
                    palette
                )

                output.putpixel(
                    (x, y),
                    nearest
                )

        return output