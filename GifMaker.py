"""
Authors: George Engel, Cory Johns, Justin Keeling
"""
import imageio
import zlib
import struct
import os
import re


class GifMaker:
    @staticmethod
    def __make_png(data, height=None, width=None):
        """
        Converts a 2D list of rgb lists into a true-colour PNG image.
        Slightly modified from original code which only generated grayscale pngs
        """
        __copyright__ = "Copyright (C) 2014 Guido Draheim"
        __licence__ = "Public Domain"

        def I1(value):
            return struct.pack("!B", value & (2**8-1))

        def I4(value):
            return struct.pack("!I", value & (2**32-1))
        # compute width&height from data if not explicit
        if height is None:
            height = len(data)  # rows
        if width is None:
            width = 0
            for row in data:
                if width < len(row):
                    width = len(row)
        # generate these chunks depending on image type
        makeIHDR = True
        makeIDAT = True
        makeIEND = True
        png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')
        if makeIHDR:
            colortype = 2 # truecolour image (no palette)
            bitdepth = 8 # with one byte per pixel (0..255)
            compression = 0 # zlib (no choice here)
            filtertype = 0 # adaptive (each scanline seperately)
            interlaced = 0 # no
            IHDR = I4(width) + I4(height) + I1(bitdepth)
            IHDR += I1(colortype) + I1(compression)
            IHDR += I1(filtertype) + I1(interlaced)
            block = "IHDR".encode('ascii') + IHDR
            png += I4(len(IHDR)) + block + I4(zlib.crc32(block))
        if makeIDAT:
            raw = b""
            for y in range(height):
                raw += b"\0" # no filter for this scanline
                for x in range(width):
                    red = b"\0" # default black pixel
                    grn = b"\0"
                    blu = b"\0"
                    if y < len(data) and x < len(data[y]):
                        red = I1(data[y][x][0])
                        grn = I1(data[y][x][1])
                        blu = I1(data[y][x][2])
                    raw += red
                    raw += grn
                    raw += blu
            compressor = zlib.compressobj()
            compressed = compressor.compress(raw)
            compressed += compressor.flush() #!!
            block = "IDAT".encode('ascii') + compressed
            png += I4(len(compressed)) + block + I4(zlib.crc32(block))
        if makeIEND:
            block = "IEND".encode('ascii')
            png += I4(0) + block + I4(zlib.crc32(block))
        return png

    @staticmethod
    def make_png_from_maze(maze, domain, colors, name):
        """
        Makes a png image to the png-list directory from the given maze
        :param maze: maze containing values in the domain, values not in the domain will be set to black
        :param domain: list of each string representation of each color, as used in the maze
        :param colors: list of RGB color lists in the same order as the domain
        :param name: the name for the png
        :return: Nothing, but will place the created png into the png-list folder
        """
        file_name = "png-list/" + name + ".png"
        data = []
        scale = 10  # each square will be this many pixels on a side
        for row in maze:
            d_row = []
            for square in row:
                try:
                    i = domain.index(square)
                    # add scale number of pixels instead of one, for horizontal size
                    for n in range(scale):
                        d_row.append(colors[i])
                except ValueError:
                    # square does not contain a color
                    # default to black
                    # add scale number of pixels instead of one, for horizontal size
                    for n in range(scale):
                        d_row.append([0, 0, 0])

            # add scale number of identical rows to data
            for n in range(scale):
                data.append(d_row)

        with open(file_name, "wb") as f:
            f.write(GifMaker.__make_png(data))

    @staticmethod
    def make_gif(gif_name, png_name):
        # get entire contents of the directory
        filenames = os.listdir("png-list")

        # don't include non-relevant files
        for file in filenames.copy():
            if not re.match(r"" + png_name + "_" + "(\d*).png", file):
                filenames.remove(file)

        # sort on the frame number
        filenames.sort(key=lambda x: int(re.search(png_name + "_" + "(\d*).png", x).group(1)))
        with imageio.get_writer(gif_name + ".gif", mode='I') as writer:
            for filename in filenames:
                image = imageio.imread("png-list/" + filename)
                writer.append_data(image)