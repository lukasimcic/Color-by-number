# import modules
from PIL import Image, ImageDraw, ImageFont, ImageOps
from colorthief import ColorThief
import math
import os

#########################################################################
# built-in funcitons

# find how similar two colors are
def distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2

# find most similar color and update repetitions
def new_color(color):
    current_distance = -1
    current_color = -1
    for color1 in colors:
        new_distance = distance(color1, color)
        if current_distance == -1 or new_distance < current_distance:
            current_distance, current_color = new_distance, color1
    repetitions[colors.index(current_color)] += 1
    return current_color

# sort colors so repetitions.png turns out nice
def sort_colors(list):
    new_list = []
    current_color = (0, 0, 0)
    while list != []:
        colors.sort(key=lambda p: distance(p, current_color))
        current_color = colors.pop(0)
        new_list.append(current_color)
    return new_list
#########################################################################

# set variables
while True:
    try:
        PICTURE_NAME = input('Enter the name of the picture (e.g. template.png): ')
        img = Image.open(PICTURE_NAME)
        break
    except FileNotFoundError:
        print("There is no picture with this name. Please try again.")
while True:
    try:
        H = int(input('Enter desired number of rows of tiles (number of colummns will then be calculated automatically): '))
        if not 1 <= H:
            print("Please enter an integer.")
        else:
            break
    except ValueError:
        print("Please enter an integer.")
W = int(H * img.size[0] / img.size[1])
while True:
    try:
        NUMBER_OF_COLORS = int(input('Enter desired number of colors (min 4, max 20): '))
        if not (4 <= NUMBER_OF_COLORS <= 20):
            print("Please enter a number between 4 and 20")
        else:
            break
    except ValueError:
        print("Please enter a number between 4 and 20")

# create small pictures with symbols that will construct the result
symbols = "#$&01x23456789€÷¤?!%@"
symbols_pictures = []
for j in range(NUMBER_OF_COLORS):
    background = Image.new('RGB', (60, 60), color = (250, 250, 250))
    draw = ImageDraw.Draw(background)
    draw.text((18,9), symbols[j], fill=(0, 0, 0))
    background = ImageOps.expand(background, border=1, fill='black')
    symbols_pictures.append(background)

# get dominant colors
if NUMBER_OF_COLORS > 7:
    NUMBER_OF_COLORS += 1 # to fix a bug of get_palette function
picture = img.resize((W, H), resample=Image.BILINEAR)
picture.resize(img.size,Image.NEAREST).save("not_important.png")
color_thief = ColorThief("not_important.png")
colors = color_thief.get_palette(color_count=NUMBER_OF_COLORS)
colors = sort_colors(colors)
os.remove("not_important.png")

# count repetitions of colors
repetitions = [0 for _ in range(len(colors))]

# process every pixel and save result
output = Image.new('RGB', (60 * W, 60 * H))
for k in range(W):
    for j in range(H):
        color = new_color(picture.getpixel((k, j)))
        picture.putpixel((k, j), color)
        x, y = k*60, j*60
        output.paste(symbols_pictures[colors.index(color)], (x, y))
output.save("result.png")

# save repetitions
n = len([c for c in repetitions if c != 0])
w, h = (500, n) if n <= 10 else (1000, math.ceil(n / 2))
repetition_picture = Image.new('RGB', (w, 200 * h), color = (255, 255, 255))
draw = ImageDraw.Draw(repetition_picture)
for k in range(n):
    x, y = (0, k) if (k < h) else (500, (k % math.ceil(n / 2)))
    repetition_picture.paste(Image.new('RGB', (200, 200), color = colors[k]), (x, 200 * y))
    draw.text((x + 210, 200 * y + 70), f" {symbols[k]}  -  x{repetitions[k]}", fill=(0, 0, 0))
repetition_picture.save("repetitions.png")

# save colored result
picture.resize(img.size,Image.NEAREST).save('colored result.png')
