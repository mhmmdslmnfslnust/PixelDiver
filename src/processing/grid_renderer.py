from PIL import Image, ImageDraw


class GridRenderer:

    @staticmethod
    def render(
        image,
        cell_size=20,
        grid_color=(180, 180, 180)
    ):

        width, height = image.size

        canvas = Image.new(
            "RGB",
            (
                width * cell_size,
                height * cell_size
            ),
            "white"
        )

        draw = ImageDraw.Draw(canvas)

        pixels = image.load()

        for y in range(height):

            for x in range(width):

                color = pixels[x, y]

                left = x * cell_size
                top = y * cell_size

                right = left + cell_size
                bottom = top + cell_size

                draw.rectangle(
                    (
                        left,
                        top,
                        right,
                        bottom
                    ),
                    fill=color,
                    outline=grid_color
                )

        return canvas