from PIL import Image, ImageOps, ImageChops


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


def transparent(src):
    print("Start Transparent!")
    im = Image.open(src)
    im = im.convert("RGBA")
    pixels = im.load()

    for i in range(im.size[1]):
        for j in range(im.size[0]):
            if pixels[j, i] <= (255, 255, 255, 255) and pixels[j, i] >= (245, 245, 245, 245):
                pixels[j, i] = (0, 0, 0, 0)
            else:
                break
    for i in reversed(range(im.size[1])):
        for j in reversed(range(im.size[0])):
            if pixels[j, i] <= (255, 255, 255, 255) and pixels[j, i] >= (245, 245, 245, 245):
                pixels[j, i] = (0, 0, 0, 0)
            else:
                break

    print("End Transparent!")
    return im


# im.save("img2.png","PNG") # For storing transperant image in png format
# im.save("img5.jpg", "PNG")
