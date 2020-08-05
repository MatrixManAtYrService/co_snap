from PIL import Image, ImageDraw, ImageFont
from Screenshot import Screenshot_Clipping
from pathlib import Path
import cv2
from math import sqrt


def screenshot_element(driver, element, file_name):
    ob = Screenshot_Clipping.Screenshot()
    temp_path = Path(ob.get_element(driver, element, "."))
    temp_path.rename(file_name)
    (temp_path.parents[0] / "clipping_shot.png").unlink()
    print(f"wrote element screenshot to {file_name}")


def top_only(orig_file, new_height, new_file):
    im = Image.open(orig_file)
    orig_size = im.size

    left = 0
    top = 0
    right = orig_size[0]
    bottom = new_height
    im2 = im.crop((left, top, right, bottom))
    im2.save(new_file)
    print(f"height({new_height}, {orig_file}) -> {new_file}")


color = (66, 203, 245)  # BGR
arrow_thickness = 2
font = ImageFont.truetype(str(Path(__file__).parents[0] / "Now-Bold.otf"), 25)
arrowhead_size = 12


def arrow(orig_file, path, new_file):

    if len(path) < 2:
        raise ValueError("arrow path must contain at least two points")

    image = cv2.imread(orig_file)
    for (from_xy, to_xy) in zip(path[:-2], path[1:-1]):
        print(f"leg from {from_xy} -> {to_xy}")
        image = cv2.line(image, from_xy, to_xy, color, arrow_thickness)

    from_xy = path[-2]
    to_xy = path[-1]

    # special thanks to Pythagoras, Euclid, and Descartes
    arrow_length = sqrt((to_xy[0] - from_xy[0]) ** 2 + (to_xy[1] - from_xy[1]) ** 2)

    tip_length_ratio = arrowhead_size / arrow_length
    image = cv2.arrowedLine(
        image, from_xy, to_xy, color, arrow_thickness, tipLength=tip_length_ratio
    )
    print(f"arrow from {from_xy} -> {to_xy}")

    cv2.imwrite(new_file, image)


def text_at(orig_file, text, at_xy, new_file):
    image = Image.open(orig_file)
    draw = ImageDraw.Draw(image)
    draw.text(at_xy, text, font=font, fill=color[::-1])
    image.save(new_file, "PNG")
    print(f"'{text} at {at_xy}")
