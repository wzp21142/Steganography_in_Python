import re
from random import seed, gauss
from numpy import *


def key_check(__key):
    if (len(__key) != 8) or (not re.findall('^[0-7]+$', __key)):
        print("密钥格式有误!")
        exit(1)
    for i in __key:
        for j in __key[__key.index(i) + 1:]:
            if j == i:
                print("密钥格式有误!")
                exit(1)
    else:
        return

def img_red_to_matrix(im_matrix):
    image_len = len(im_matrix)
    #image_width=len(im_matrix[0])
    # 获取每一img像素对应的R值存入矩阵中,进行LSB加密
    image_pixels = [[0 for i in range(8)] for j in range(image_len)]  # 与信息矩阵对应,列数由ascii码上限255决定
    i = 0
    j = 0
    while j < image_len:
        while i < 8:
            image_pixels[j][i] = im_matrix[j, i, 2]
            i += 1
        j += 1
        i = 0
    return image_pixels
