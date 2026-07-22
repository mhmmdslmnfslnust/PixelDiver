import csv
import os


class Palette:

    def __init__(self, name, colors):
        self.name = name
        self.colors = colors


class PaletteManager:

    def __init__(self):

        self.palettes = {}

    ##################################################

    def load(self, csv_file):

        palette = self._read_csv(csv_file)

        self.palettes[palette.name] = palette

    ##################################################

    def get(self, name):

        return self.palettes.get(name)

    ##################################################

    def names(self):

        return sorted(self.palettes.keys())

    ##################################################

    @staticmethod
    def rgb_list(palette):

        return [

            color["rgb"]

            for color in palette.colors

        ]

    ##################################################

    @staticmethod
    def _read_csv(csv_file):

        colors = []

        with open(csv_file, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                colors.append({

                    "name": row["Name"],

                    "code": row["Code"],

                    "rgb": (
                        int(row["R"]),
                        int(row["G"]),
                        int(row["B"])
                    )

                })

        name = os.path.splitext(
            os.path.basename(csv_file)
        )[0]

        return Palette(name, colors)

    @staticmethod
    def rgb_list(palette):

        return [

            color["rgb"]

            for color in palette.colors

        ]