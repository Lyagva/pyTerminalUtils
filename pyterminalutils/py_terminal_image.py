#  Copyright (c) 2022 Lyagva
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import io
import pathlib
import shutil
from os import system, name  # Used to clear console
from typing import Union, List

import PIL.Image
from PIL import ImageEnhance


class ImageToASCII:
    # String (List) of all symbols from invisible to solid
    symbols = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    # Contains all colors and color codes
    class Colors:
        WHITE = "\033[0m"
        BLACK = "\033[30m"  # "\033[90m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        ORANGE = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        LIGHT_GREY = "\033[37m"
        DARK_GREY = "\033[90m"
        LIGHT_RED = "\033[91m"
        LIGHT_GREEN = "\033[92m"
        YELLOW = "\033[93m"
        LIGHT_BLUE = "\033[94m"
        PINK = "\033[95m"
        LIGHT_CYAN = "\033[96m"

        color_dict = {
            WHITE: (238, 238, 236),
            BLACK: (46, 52, 54),
            RED: (204, 0, 0),
            GREEN: (78, 154, 6),
            ORANGE: (196, 160, 0),
            BLUE: (52, 101, 164),
            PURPLE: (117, 80, 123),
            CYAN: (6, 152, 154),
            LIGHT_GREY: (211, 215, 207),
            DARK_GREY: (85, 87, 83),
            LIGHT_RED: (239, 41, 41),
            LIGHT_GREEN: (138, 226, 52),
            YELLOW: (252, 233, 79),
            LIGHT_BLUE: (114, 159, 207),
            PINK: (173, 127, 168),
            LIGHT_CYAN: (52, 226, 226)
        }

    @staticmethod
    def closest_color(rgb: tuple):
        """
        Finds closest ANSI color from given rgb
        :param rgb: tuple contains 3 numbers from [0, 255]
        :return:
        """

        r, g, b = rgb
        color_diffs = []  # contains tuples of (difference value [0;inf), color key)
        for key, value in ImageToASCII.Colors.color_dict.items():  # Loop through all colors
            cr, cg, cb = value
            color_diff = ((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) ** 0.5  # get difference for given color
            color_diffs.append((color_diff, key))  # store difference and ANSI string
        return min(color_diffs)[1]  # return ANSI string with minimal difference

    # TODO: Refactor. Too many arguments.
    def __init__(self, file: Union[str, io.BytesIO, pathlib.Path], width: int = 120,
                 is_colored: bool = False, char_size: tuple = (16, 8), brightness: float = 1.0):
        """
            Class that outputs ASCII Image.
            To draw an image use ImageToASCII.image_to_text() + ImageToASCII.print_image()
        :param file: A filename (string), pathlib.Path object or a file object.
           The file object must implement ``file.read``,
           ``file.seek``, and ``file.tell`` methods,
           and be opened in binary mode.
        :param width: integer value which defines width of output image
        :param is_colored: bool defines will image be black/white or with ANSI colors
        :param char_size: tuple of (width, height) of single char, used to get ratio of w/h
        :param brightness: float brightness modifier (use ~1.5 for colored and 0.5 for b/w)
        """
        self.file: Union[str, io.BytesIO, pathlib.Path] = file

        self.symbol_aspect = char_size[0] / char_size[1]  # Get symbol aspect
        self.width = width
        self.height = 0

        self.is_colored = is_colored
        self.brightness = brightness

        self.screen: List[List[str]] = [[]]

    def image_to_text(self):
        """
            Process and outputs image to self.screen list
        """
        image = PIL.Image.open(self.file)  # Opening image

        # Calculate output image height based on width and aspect
        self.height = int(self.width / image.size[0] * image.size[1] / self.symbol_aspect)

        # Create self.screen matrix for image
        self.screen = [[" " for _ in range(self.width)] for _ in range(self.height)]

        image = image.convert("RGB")  # Convert image to RGB values (if you open png, it is RGBA by default)
        image = image.resize((self.width, self.height),
                             resample=PIL.Image.Resampling.BILINEAR)  # Resizing image to given size
        image = ImageEnhance.Brightness(image).enhance(self.brightness)  # Adjust brightness of image

        pixels = image.load()  # Get pixels matrix

        # is_colored == True
        if self.is_colored:
            # Loop through all pixels
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = pixels[x, y]  # Gets rgb values of pixel
                    # Finds char using greyscale value
                    char = self.symbols[int(sum([r, g, b]) / 3 / 255 * len(self.symbols)) - 1]
                    # Replaces screen char by ANSI + given char
                    self.screen[y][x] = self.closest_color((r, g, b)) + char
        else:
            # Loop through all pixels
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = pixels[x, y]  # Gets rgb values of pixel
                    # Finds char using greyscale value
                    char = self.symbols[int(sum([r, g, b]) / 3 / 255 * len(self.symbols)) - 1]
                    # Replaces screen char by given char
                    self.screen[y][x] = char

        image.close()  # Closes image to free RAM

    def print_image(self):
        """
            Prints self.screen to console
        """
        system("cls" if name == "nt" else "clear")

        # Loop through rows of self.screen
        for y in range(self.height):
            print("".join(self.screen[y]))  # Prints row to console

        print(ImageToASCII.Colors.WHITE)  # Prints ANSI default color


def main(args: argparse.Namespace):
    """Run the program with the given command line arguments"""
    image_to_ascii = ImageToASCII(args.input,
                                  width=args.width, brightness=1.5 if args.colorized else 0.5,
                                  is_colored=args.colorized)
    image_to_ascii.image_to_text()  # Converts image to text
    image_to_ascii.print_image()  # Prints image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility for outputting a picture in ASCII"
    )
    parser.add_argument("input", type=argparse.FileType('rb'))
    parser.add_argument('--colorized', action='store_true', help='Prints colorized ascii')
    parser.add_argument('--no-colorized', dest='colorized', action='store_false', help='Do not print colorized ascii')
    parser.set_defaults(colorized=False)  # Setting colorized default behavior.
    parser.add_argument("--width", type=int, default=shutil.get_terminal_size().columns, help="Set height of picture")
    # TODO: add height argument
    main(parser.parse_args())
