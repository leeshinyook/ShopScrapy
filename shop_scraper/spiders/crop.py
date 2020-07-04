# from PIL import Image
#
# im = Image.open('')  # INPUT Image
# pix = im.load()
# width, height = im.size[0], im.size[1]
# stand = pix[1, 1]
#
#
# def find_border_top(start_x):
#     for h in range(start_x):
#         if pix[width / 2, h] != stand:
#             return h
#
#
# def find_border_bottom(start_x, start_y):
#     cnt = 0
#     for h in range(start_x, height):
#         for w in range(start_y):
#             if pix[w, h] == stand:
#                 cnt += 1
#         if cnt == width - 1:
#             return h
#         cnt = 0
#
#
# crop_h1 = find_border_top(height)
# crop_h2 = find_border_bottom(crop_x1 + 30, width - 1)
# area = (1, crop_h1, width, crop_h2)
# crop_img = im.crop(area)
# crop_img.show()
