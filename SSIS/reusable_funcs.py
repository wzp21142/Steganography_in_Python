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


# 第二和第三轮加密需要的交错函数,根据密钥重组矩阵
def interleaving(length, password, b, c):
    j = 0
    while j < length:
        i = 0
        for pw in password:
            if i > 7:
                i = 0
            else:
                b[j][i] = c[j][pw]
            i += 1
            pw += 1
        j += 1


# AWGN噪声生成函数
def noise_generate(img_len):
    seed(1)  # 加解密随机数seed应一致
    # 噪声序列应满足高斯分布,即文中的additive white Gaussian noise (AWGN) series
    series_temp = [gauss(0.0, 1.0) for i in range(img_len * 8)]
    series = reshape(series_temp, (img_len, 8))  # 重组噪声序列格式
    mini = min(series_temp)
    z = series - mini
    maxi = z.max()
    key2_list = maxi / 2 ** 6
    audio = fix(z / key2_list)  # audio信号下取整
    return audio / audio.max()


# 根据密钥生成第二阶段的噪声,加解密均可复用
def stage_2(image_len):
    seed(1)
    signal_AWGN = noise_generate(image_len)
    signal_interleaved = [[0 for i in range(8)] for j in range(image_len)]
    key2 = input("第2密钥(AWGN):")
    key_check(key2)
    key2_list = list()
    for v in key2:
        key2_list.append(int(v))
    interleaving(image_len, key2_list, signal_interleaved, signal_AWGN)
    return signal_AWGN


def img_red_to_matrix(im_matrix):
    image_len = len(im_matrix)
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
