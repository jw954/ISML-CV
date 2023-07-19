from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

def gen_mask():
    

subframe_count = 319
width = 40
overlap = 0
height = 8

pix = np.zeros((subframe_count,320,512), dtype=bool)


# for i in range(6400):
#     print("pre processing subframe: {}".format(i), end="\r")
#     for j in range(320):
#         for k in range(512):
#             pix[i][j][k] = False

x = 0
y = 0

for i in range(subframe_count):
    print("processing subframe: {}".format(i), end="\r")
    for a in range(x*width, x*width+width+overlap):
        for b in range(y*height, y*height+height):
            pix[i][b][a] = True

    if x == 320/width-1:
        x = 0
        y += 1
    else:
        x += 1

    if y == 40:
        y = 0
    

pix = pix.reshape(-1, 512)
img = Image.fromarray(pix)
img = img.convert('1')
img.save('./wm4_40_ol.bmp')