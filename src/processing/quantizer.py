from PIL import Image


class ColorQuantizer:

    @staticmethod
    def color_distance(c1, c2):

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
                best = candidate
                best_distance = distance

        return best

    #######################################################

    @staticmethod
    def clamp(value):

        return max(0, min(255, round(value)))

    #######################################################

    @classmethod
    def quantize(cls, image, palette, dithering=False):

        image = image.convert("RGB")

        if not dithering:
            return cls._nearest_quantization(image, palette)

        return cls._floyd_steinberg(image, palette)

    #######################################################

    @classmethod
    def _nearest_quantization(cls, image, palette):

        output = Image.new("RGB", image.size)

        width, height = image.size

        for y in range(height):

            for x in range(width):

                pixel = image.getpixel((x, y))

                output.putpixel(
                    (x, y),
                    cls.nearest_color(pixel, palette)
                )

        return output

    #######################################################

    @classmethod
    def _floyd_steinberg(cls, image, palette):

        pixels = image.load()

        width, height = image.size

        for y in range(height):

            for x in range(width):

                old = pixels[x, y]

                new = cls.nearest_color(old, palette)

                pixels[x, y] = new

                error = (
                    old[0] - new[0],
                    old[1] - new[1],
                    old[2] - new[2]
                )

                cls._add_error(
                    pixels,
                    x + 1,
                    y,
                    width,
                    height,
                    error,
                    7 / 16
                )

                cls._add_error(
                    pixels,
                    x - 1,
                    y + 1,
                    width,
                    height,
                    error,
                    3 / 16
                )

                cls._add_error(
                    pixels,
                    x,
                    y + 1,
                    width,
                    height,
                    error,
                    5 / 16
                )

                cls._add_error(
                    pixels,
                    x + 1,
                    y + 1,
                    width,
                    height,
                    error,
                    1 / 16
                )

        return image

    #######################################################

    @classmethod
    def _add_error(
        cls,
        pixels,
        x,
        y,
        width,
        height,
        error,
        factor
    ):

        if x < 0 or y < 0:
            return

        if x >= width or y >= height:
            return

        r, g, b = pixels[x, y]

        pixels[x, y] = (

            cls.clamp(r + error[0] * factor),

            cls.clamp(g + error[1] * factor),

            cls.clamp(b + error[2] * factor)

        )