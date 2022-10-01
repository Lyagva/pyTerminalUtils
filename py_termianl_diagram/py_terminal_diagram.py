from shutil import get_terminal_size


class DiagramStatic:
    class Colors:
        PURPLE = "\033[95m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        WHITE = "\033[37m"
        RESET = "\033[0m"

    def __init__(self, data: dict) -> None:
        """
            Class that outputs simple diagram by given data.
            To draw a diagram use DiagramStatic.draw() method
        :param data: Dictionary with every [key is string name of a column] and [value is int/float positive number]
        """
        self.data = dict(data)

        # Getting screen size
        self.width, self.height = get_terminal_size()
        self.width -= 1

        # Creating matrix for screen
        self.screen = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def draw(self, color: str = ""):
        """
            Process and draw an image
        """
        self.get_image()
        self.render(color=color)

    def get_image(self):
        """
            Draws all art to screen matrix
        """

        from textwrap import TextWrapper  # Necessary for wrapping lines

        left_margin = len(str(max(self.data.values()))) + 1  # Distance between left edge and vertical line
        bottom_margin = 5  # Distance between bottom corner and horizontal line (from bottom to top)

        # Vertical line
        for y in range(self.height - bottom_margin):  # From top edge to bottom corner (bottom margin)
            self.screen[y][left_margin] = "│"  # Set vertical line symbol
        # Horizontal bar
        for x in range(left_margin + 1, self.width):  # From left corner (left margin) to right edge
            self.screen[self.height - bottom_margin][x] = "─"  # Set horizontal line symbol
        # Corner
        self.screen[self.height - bottom_margin][left_margin] = "└"  # Set top-right corner symbol

        # ==== Operating Data =====
        max_value = max(self.data.values()) * 1.1  # Getting max value on columns (110% of max value in data)
        max_column_height = self.height - bottom_margin - 1  # Max column height without bottom margin

        record_width = (self.width - left_margin) // (len(self.data.keys()))  # width of one record (column, key)
        column_width = record_width * 2 // 3  # Width of column
        column_spacing = record_width - column_width  # Width of spacing between columns

        col = 0  # Column number
        for key, value in self.data.items():  # Loop through all items in data
            # Drawing column
            col_height = int(value / max_value * max_column_height)  # Height of current column without bottom margin

            # Left X value of column. With margins, spaces and prev columns
            min_x = col * (column_width + column_spacing) + column_spacing // 2 + left_margin + 1

            # Looping through all Y rows to paint them
            for y in range(max_column_height - col_height, self.height - bottom_margin):
                for x in range(min_x, min_x + column_width):  # Looping through all X"s to make columns thicc
                    self.screen[y][x] = "█"  # Paint point with solid

            # Record value (Left)
            str_value = str(value).rjust(left_margin, " ")  # Fill spaces from left edge (margin word to the right)
            for x in range(left_margin):
                self.screen[max_column_height - col_height][x] = str_value[x]  # Copy word char by char

            # Record name (Bottom)
            # TextWrapper needed to automatically wrap lines
            # max lines = 4
            # long words will be shortened
            # if name is too long it will become "..."
            # max width = column_width
            text = TextWrapper(max_lines=4, break_long_words=True,
                               placeholder="...", width=column_width).fill(key).split("\n")  # split by lines
            for y, line in enumerate(text):  # Go through all lines
                str_value = str(line).center(column_width)  # Center text
                for x in range(min_x, min_x + len(str_value)):  # Go through all X"s
                    self.screen[self.height - bottom_margin + 1 + y][x] = str_value[x - min_x]  # Copy word char by char

            col += 1  # Increase column number

    def render(self, color: str = ""):
        """
            Renders image from self.screen using prints
        """

        from os import system, name
        system("cls" if name == "nt" else "clear")

        for y in range(self.height):
            print(color + "".join(self.screen[y]))


if __name__ == "__main__":
    # Fills data with values
    data = {"oak": 100,
            "pine": 79,
            "birch": 200,
            "banana": 25,
            "coconut tree with long name. Why the hell is it so long?!": 0,
            "apple": 134}

    diagram_static = DiagramStatic(data)  # Creating object for Diagram
    diagram_static.draw(color=diagram_static.Colors.GREEN)  # Draw diagram
