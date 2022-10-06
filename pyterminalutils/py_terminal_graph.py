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

class GraphStatic:
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

    def line(self, start=(0, 0), end=(10, 10), color=""):
        try:
            m = (end[1] - start[1]) / (end[0] - start[0])
        except ZeroDivisionError as e:
            return
        b = start[1] - m * start[0]

        for x in range(min(start[0], end[0]), max(start[0], end[0])):
            if self.screen[int(m * x + b)][x] == " ":
                self.screen[int(m * x + b)][x] = color + "█"

    def __init__(self, data: list, color: str = "") -> None:
        """
                Class that outputs simple graph by given data.
                To draw a graph use GraphStatic.draw() method
        :param data: list with tuple (float x, float y)
        """
        from os import get_terminal_size

        self.data = data
        self.color = color

        # Getting screen size
        self.width, self.height = get_terminal_size()
        self.width -= 1

        # Creating matrix for screen
        self.screen = [list(" " * self.width) for _ in range(self.height)]

    def draw(self, color: str = ""):
        """
                Process and draw an image
        """
        self.get_image()
        self.render()

    def get_image(self):
        """
                Draws all art to screen matrix
        """

        from textwrap import TextWrapper  # Necessary for wrapping lines

        left_margin = len(str(max([round(a, 5) for a, _ in self.data]))) + \
            1  # Distance between left edge and vertical line
        bottom_margin = 5  # Distance between bottom corner and horizontal line (from bottom to top)

        max_x = max([x for x, y in self.data])
        max_y = max([y for x, y in self.data])

        # ==== Operating Data =====
        prev_pos = (left_margin, self.height - bottom_margin)
        for num, (x, y) in enumerate(self.data):  # Loop through all items in data
            x_pos = left_margin + int(x / max_x * (self.width - left_margin - 1))
            y_pos = self.height - bottom_margin - int(y / max_y * (self.height - bottom_margin))
            pos = (x_pos, y_pos)

            self.line(prev_pos, pos, color=self.Colors.DARK_GREY)

            prev_pos = pos

            self.screen[pos[1]][pos[0]] = self.color + "█"  # Paint point with solid
            # Record value (Left)
            # Fill spaces from left edge (margin word to the right)
            str_value = str(round(y, 5)).rjust(left_margin, " ")
            for i in range(left_margin):
                self.screen[pos[1]][i] = self.color + str_value[i]  # Copy word char by char

            # Record name (Bottom)
            # TextWrapper needed to automatically wrap lines
            # max lines = 4
            # long words will be shortened
            # if name is too long it will become "..."
            # max width = column_width
            for i in range(len(str(x))):
                if str(x)[i] != " ":
                    self.screen[self.height - bottom_margin + num %
                                bottom_margin][x_pos - len(str(x)) // 2 + i] = str(x)[i]

        # Vertical line
        for y in range(self.height - bottom_margin):  # From top edge to bottom corner (bottom margin)
            self.screen[y][left_margin] = self.color + "│"  # Set vertical line symbol
        # Horizontal bar
        for x in range(left_margin + 1, self.width):  # From left corner (left margin) to right edge
            self.screen[self.height - bottom_margin][x] = self.color + "─"  # Set horizontal line symbol
        # Corner
        self.screen[self.height - bottom_margin][left_margin] = self.color + "└"  # Set top-right corner symbol

    def render(self):
        """
                Renders image from self.screen using prints
        """

        from os import system, name
        system("cls" if name == "nt" else "clear")

        for y in range(self.height):
            print("".join(self.screen[y]))
        # input("Press any key to continue... ")


if __name__ == "__main__":
    # Fills data with values

    from math import sin
    data = [(x, abs(sin(x / 20))) for x in range(0, 100)]

    diagram_static = GraphStatic(data, color=GraphStatic.Colors.GREEN)  # Creating object for graph
    diagram_static.draw()  # Draw graph
