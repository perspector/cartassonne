# Thank you tsaglam for the wonderful Carcassonne tiles
# See https://github.com/tsaglam/Carcassonne

# uses Pillow for fast image concatenation
from PIL import Image
import matplotlib.pyplot as plt

# use time for performance timing of operations
import time

# use math to round the amount of tiles to compute based on wall dimensions, rounds up
import math

# uses glob (standard library) to find tile files
import glob

# uses random to randomly choose tiles that match criteria
#import random
import secrets as random

# os is used only to get the current working directory
import os


# TODO: find out how to synthesize images/pdfs for printing


# find all the tile files (tile files is fun to say!)
tile_names = glob.glob('tiles/*.png')
for tile_index in range(len(tile_names)):
    tile_names[tile_index] = tile_names[tile_index][6:]

# width and height of the wall, measured in tiles

width = float(input('What is the width of your wall? (meters) ')) # 3.09
height = float(input('What is the height of your wall? (meters) ')) # 1.51

width = math.ceil(width / 0.045)
height = math.ceil(height / 0.045)

no_border_cross = input("Can roads and cities cross over the border? (y/N) ").lower()
if no_border_cross == "n" or no_border_cross == "":
    no_border_cross = True
else:
    no_border_cross = False

print(f"\n[INFO] Creating a {width} by {height} grid of Carcassonne tiles!\n")

tile_width = 300
tile_height = tile_width


t1_algorithm = time.time()
wall_tiles = []
for row in range(height):
    wall_tiles.append([])
    for column in range(width):
        tile = random.choice(tile_names)
        if column == 0: # first tile in the row
            if row == 0: # upper left corner
                if no_border_cross == True:
                    while tile[0] != 'f' or tile[1] != 'f':
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
            elif row == height - 1: # last row
                if no_border_cross == True:
                    while wall_tiles[row - 1][column][3] != tile[1] or tile[0] != 'f' or tile[3] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row - 1][column][3] != tile[1]: # bottom of previous row's tile does NOT match top of this tile
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
            else: # not the first row or last row
                if no_border_cross == True:
                    while wall_tiles[row - 1][column][3] != tile[1] or tile[0] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row - 1][column][3] != tile[1]: # bottom of previous row's tile does NOT match top of this tile
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
        elif column == width - 1: # last tile in the row
            if row == 0: # top row
                if no_border_cross == True:
                    while wall_tiles[row][column - 1][2] != tile[0] or tile[1] != 'f' or tile[2] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row][column - 1][2] != tile[0]:
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
            elif row != height - 1: # not last row
                if no_border_cross == True:
                    while wall_tiles[row - 1][column][3] != tile[1] or wall_tiles[row][column - 1][2] != tile[0] or tile[2] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row - 1][column][3] != tile[1] or wall_tiles[row][column - 1][2] != tile[0]:
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
            else: # last row
                if no_border_cross == True:
                    while wall_tiles[row - 1][column][3] != tile[1] or wall_tiles[row][column - 1][2] != tile[0] or tile[2] != 'f' or tile[3] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row - 1][column][3] != tile[1] or wall_tiles[row][column - 1][2] != tile[0]:
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
        else: # not the first or last tile in the row
            if row == 0: # top row
                if no_border_cross == True:
                    while wall_tiles[row][column - 1][2] != tile[0] or tile[1] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row][column - 1][2] != tile[0]: # right of previous row's tile does NOT match left of this tile
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
            elif row == height - 1: # bottom row
                if no_border_cross == True:
                    while wall_tiles[row][column - 1][2] != tile[0] or wall_tiles[row - 1][column][3] != tile[1] or tile[3] != 'f':
                        tile = random.choice(tile_names)
                else:
                    while wall_tiles[row][column - 1][2] != tile[0] or wall_tiles[row - 1][column][3] != tile[1]: # right of previous row's tile does NOT match left of this tile
                        tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
            else:
                while (
                    wall_tiles[row - 1][column][3] != tile[1] or # bottom of previous row's tile does NOT match top of this tile
                    wall_tiles[row][column - 1][2] != tile[0] # right of previous row's tile does NOT match left of this tile
                ):
                    tile = random.choice(tile_names)
                wall_tiles[row].append(tile)
print(f'\n\n[INFO] Tiling Algorithm Time: {(time.time() - t1_algorithm) * 1000} ms')


def vconcat(image_list, height=100):
    result = Image.new('RGB',(image_list[0].width, len(image_list) * height))
    for i in range(len(image_list)):
        result.paste(image_list[i], (0, i*height))
    return result


def hconcat(image_list, width=100):
    result = Image.new('RGB',(len(image_list) * width, width))
    for i in range(len(image_list)):
        result.paste(image_list[i], (i*width, 0))
    return result

t1_concat = time.time()

tiled_image = vconcat(
    [
        hconcat(
            [
                Image.open(i).resize((tile_width, tile_height)) for i in ['tiles/' + img for img in row]
            ], width=tile_width
        ) for row in wall_tiles
    ], height=tile_height
)

delta_concat = time.time() - t1_concat
print(f'[INFO] Image Concatenation Time: {(delta_concat) * 1000} ms')
print(f'           Per Tile: {(delta_concat)/(width * height) * 1000} ms')
t1_save = time.time()
tiled_image.save('tiled-result.pdf')

print(f'[INFO] File Saving Time: {(time.time() - t1_save) * 1000} ms')

print(f'[INFO] Total Time: {(time.time() - t1_algorithm) * 1000} ms')

print(f"\n[RESULT] Output saved to:\n{os.getcwd() + '/tiled-result.pdf'}")
