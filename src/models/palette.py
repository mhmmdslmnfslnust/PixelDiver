class PaletteColor:

    def __init__(
        self,
        id,
        name,
        code,
        rgb
    ):

        self.id = id
        self.name = name
        self.code = code
        self.rgb = rgb


class Palette:

    def __init__(
        self,
        name,
        colors
    ):

        self.name = name
        self.colors = colors


    def rgb_values(self):

        return [
            color.rgb
            for color in self.colors
        ]