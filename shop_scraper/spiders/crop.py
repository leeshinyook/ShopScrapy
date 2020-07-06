import ssl
from urllib.request import urlopen
from PIL import Image

context = ssl._create_unverified_context()


def find_images_location_from_url(url):
    img = Image.open(urlopen(url, context=context))
    width, height = img.size  # x, y
    pix = img.load()
    vertical = find_vertical_border(width, height, pix)
    horizontal = find_horizontal_border(width, height, pix)
    points = []
    for v in range(0, len(vertical), 2):
        if 1500 > vertical[v + 1] - vertical[v] > 300:
            location = (horizontal[0], vertical[v], horizontal[1], vertical[v + 1])
            points.append(location)
    return points


def assert_one_line_width(h, width, pix):
    for w in range(width - 1):
        if pix[w, h] != pix[w + 1, h]:
            return True
    return False


def assert_one_line_height(w, height, pix):
    for h in range(height - 1):
        if pix[w, h] != pix[w, h + 1]:
            return True
    return False


def find_horizontal_border(width, height, pix):
    horizontal = []
    flag = True
    for w in range(width):
        if assert_one_line_height(w, height, pix):
            if flag:
                flag = False
                horizontal.append(w)
        else:
            if not flag:
                horizontal.append(w)
                flag = True
    if len(horizontal) == 1:
        horizontal.append(width - 1)
    return horizontal


def find_vertical_border(width, height, pix):
    vertical = []
    flag = True
    for h in range(height):
        if assert_one_line_width(h, width, pix):
            if flag:
                flag = False
                vertical.append(h)
        else:
            if not flag:
                vertical.append(h)
                flag = True
    if len(vertical) % 2:
        vertical.append(height - 1)
    return vertical


print(find_images_location_from_url('https://www.ggsing.com/yeook/itempage/corduroybasicpants_new7.jpg'))