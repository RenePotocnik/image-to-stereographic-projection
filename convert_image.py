import math
import tkinter
from tkinter import filedialog
from typing import Tuple

from PIL import Image


def get_image():
    global img, img_name
    print("Open image", end="\r")
    root = tkinter.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename(filetypes=[("Image", ".png .jpg")])
    root.destroy()
    img = Image.open(img_path)
    img_name = img_path.split("/")[-1].split(".")[:]
    return img, img_name


def progress_update(y: int, height: int, prefix='Progress', suffix='', length=50):
    completed = int(length * y // height)
    empty = length - completed
    bar = "#" * completed + " " * empty
    percent = f"{100 * (y / float(height)):.2f}"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")
    if y == height:
        print(" " * (length + 30), end="\r")


img, img_name = get_image()
img = img.rotate(180)
img = img.resize((img.width, img.width))
imgX = img.width
imgY = img.height

new_image = Image.new("RGB", (imgX, imgY))

rscale = imgX / (math.sqrt(imgX ** 2 + imgY ** 2) / 2)
tscale = imgY / (2 * math.pi)

for y in range(0, imgY):
    dy = y - imgY / 2
    progress_update(y=y, height=img.height, prefix="Converting", suffix="", length=50)

    for x in range(0, imgX):
        dx = x - imgX / 2
        t = int(math.atan2(dy, dx) % (2 * math.pi) * tscale)
        r = int(math.sqrt(dx ** 2 + dy ** 2) * rscale)

        if 0 <= t < imgX and 0 <= r < imgY:
            try:
                r, g, b = img.getpixel((t, r))
            except ValueError:
                r, g, b, _ = img.getpixel((t, r))
            col = b * 65536 + g * 256 + r
            new_image.putpixel((x, y), col)

new_image_name = f"{img_name[0]}_new.png"
new_image.save(new_image_name, "PNG")
input(f"\nNew image saved as '{new_image_name}'")
