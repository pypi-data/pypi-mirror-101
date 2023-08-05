# Will eventually be a seperate package.
from PIL import Image, ImageDraw, ImageColor, ImageFont
import glob
from random import randint, choice


class grid:
    def __init__(self, initconfig, rulebook, resolution, grid=False):

        self.rulebook = rulebook

        width = len(initconfig)

        height = len(initconfig[0])

        self.grid_draw(width, height, resolution, grid=grid)

        for x in range(0, len(initconfig)):

            for y in range(0, len(initconfig[x])):

                self.block(x + 1, y + 1, rulebook[(initconfig[x])[y]])

    def grid_draw(self, width, height, block_size, grid=False):

        self.width = width * block_size
        self.height = height * block_size
        self.step_size = block_size
        self.image = Image.new(
            mode="RGB", size=(self.width, self.height), color="white"
        )

        if grid:

            for x in range(0, self.image.width + self.step_size, self.step_size):
                draw = ImageDraw.Draw(self.image)
                y_start = 0
                y_end = self.image.height
                line = ((x, y_start), (x, y_end))
                draw.line(line, fill="black")

            for y in range(0, self.image.height + self.step_size, self.step_size):
                draw = ImageDraw.Draw(self.image)
                x_start = 0
                x_end = self.image.width
                line = ((x_start, y), (x_end, y))
                draw.line(line, fill="black")

    def display(self):

        self.image.show()

    def block(self, x, y, colour):

        draw = ImageDraw.Draw(self.image)

        x = x - 1

        y = self.height / self.step_size - y

        x_top = x * self.step_size  # + 1

        y_top = y * self.step_size  # + 1

        x_lower = x_top + self.step_size  # - 2

        y_lower = y_top + self.step_size  # - 2

        draw.rectangle((x_top, y_top, x_lower, y_lower), fill=colour)

    def de_block(self, x, y):

        self.block(x, y, "white")

    def tower(self, x, y, wall_colour):

        for wall in range(0, y + 1):

            self.block(x, wall, wall_colour)

    def de_tower(self, x, y):

        for wall in range(0, y + 1):

            self.de_block(x, wall)

    def load_rulebook(self, rulebook):

        """Loads the rules for colouring number on the grid.
        Must be a dictionary with rulebook[number] = colour."""

        self.rulebook = rulebook

    def draw_config(self, config):

        """Draws the given config according to the loaded rulebook, config must
        be 1d or 2d array."""

        for x in range(0, len(config)):

            for y in range(0, len(config[x])):

                self.block(x + 1, y + 1, self.rulebook[(config[x])[y]])


def gridMaker(folderpath, width, height, offset, resolution, name):
    """ This function produces a grid of images from a folder of seperate images. The images must be square"""

    imageNames = [i for i in glob.glob("{}/*.png".format(folderpath))]

    widthPixels = offset * (width + 1) + resolution * width

    heightPixels = offset * (height + 1) + resolution * height

    mainImage = Image.new(mode="RGB", size=(widthPixels, heightPixels), color="white")

    i = 0

    for y in range(0, height):

        for x in range(0, width):

            xcord = x * resolution + offset * (x + 1)

            ycord = y * resolution + offset * (y + 1)

            tmp_img = Image.open(imageNames[i])

            mainImage.paste(tmp_img, (xcord, ycord))

            i += 1

    mainImage.save("{}.png".format(name))
