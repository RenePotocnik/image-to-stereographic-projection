import math
import time
import tkinter
from tkinter import filedialog

from PIL import Image


def get_image():
    """
    Open file explorer window to select 'png/jpg' image

    :return: Image and the image name
    """
    print("Open image", end="\r")
    root = tkinter.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename(filetypes=[("Image", ".png .jpg")])
    root.destroy()
    img = Image.open(img_path)
    img_name = img_path.split("/")[-1]
    return img, img_name


def progress_update(y: int, height: int,
                    prefix='Progress',
                    suffix='',
                    length=50):
    """
    Displays a progress bar in the console

    :param y: The current `y` value of the process
    :param height: The entire height/last `y`
    :param prefix: Text that appears before the progress bar
    :param suffix: Text that appears after the progress bar
    :param length: The length of the progress bar
    """
    completed = int(length * y // height)
    empty = length - completed
    bar = "#" * completed + " " * empty
    percent = f"{100 * (y / float(height)):.2f}"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")
    if y == height:
        print(" " * (length + 30), end="\r")


def to_stereographic_projection(img: Image,
                                scale_to_width: bool = True,
                                img_name: str = "new_image",
                                save_image: bool = True,
                                open_image: bool = True):
    """
    Convert the image into a stereographic_projection

    :param img: Image to be converted.
    :param scale_to_width: Should the image be scaled to its width instead of its height.
    Image is higher resolution, but greatly increases processing time.
    :param img_name: The name of the image.
    :param save_image: Should the image be saved (to the same directory as the script).
    :param open_image: Should the image open after processing is done.
    :return: The new image.
    """
    img = img.rotate(180)
    img = img.resize((img.width, img.width) if scale_to_width else (img.height, img.height))
    img_x = img.width
    img_y = img.height
    img_data = img.load()

    new_image = Image.new("RGB", (img_x, img_y))
    new_image_data = new_image.load()

    rscale = img_x / (math.sqrt(img_x ** 2 + img_y ** 2) / 2)
    tscale = img_y / (2 * math.pi)
    img_y_h, img_x_h = img_y / 2, img_x / 2
    s_time = time.time()
    for y in range(0, img_y):
        dy = y - img_y_h
        progress_update(y=y, height=img.height, prefix="Converting", suffix="", length=50)

        for x in range(0, img_x):
            dx = x - img_x_h
            t = int(math.atan2(dy, dx) % (2 * math.pi) * tscale)
            r = int(math.sqrt(dx ** 2 + dy ** 2) * rscale)

            if 0 <= t < img_x and 0 <= r < img_y:
                try:
                    r, g, b = img_data[t, r]
                except ValueError:
                    r, g, b, _ = img_data[t, r]
                col = b * 65536 + g * 256 + r
                # new_image.putpixel((x, y), col)
                new_image_data[x, y] = col

    print("Processing time:", round(time.time() - s_time, 3), "sec", " " * 50)
    new_image_name = f"new_{img_name}"
    if save_image:
        new_image.save(new_image_name, "PNG")
        print(f"\nNew image saved as '{new_image_name}'")
    if open_image:
        new_image.show(new_image_name)

    return new_image


if __name__ == '__main__':
    image, image_name = get_image()
    to_stereographic_projection(img=image, scale_to_width=True, img_name=image_name, save_image=True, open_image=True)
