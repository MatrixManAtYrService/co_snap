from PIL import Image, ImageDraw, ImageFont
from Screenshot import Screenshot_Clipping
from pathlib import Path
import IPython
import cv2


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
arrow_thickness = 3
font = ImageFont.truetype(str(Path(__file__).parents[0] / "Now-Bold.otf"), 25)


def arrow_from_to(orig_file, from_xy, to_xy, new_file):
    image = cv2.imread(orig_file)
    image = cv2.arrowedLine(image, from_xy, to_xy, color, arrow_thickness)
    cv2.imwrite(new_file, image)
    print(f"arrow from {from_xy} -> {to_xy}")


def text_at(orig_file, text, at_xy, new_file):
    image = Image.open(orig_file)
    draw = ImageDraw.Draw(image)
    draw.text(at_xy, text, font=font, fill=color[::-1])
    image.save(new_file, "PNG")
    print(f"'{text} at {at_xy}")
