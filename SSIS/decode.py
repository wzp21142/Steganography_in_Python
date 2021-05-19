import cv2
from SSIS.reusable_funcs import *

im_matrix = cv2.imread("output.png")
img_length = len(im_matrix)
img_red = img_red_to_matrix(im_matrix);

# 将对应信息位转为二进制取到list中
info_matrix = [[0 for i in range(8)] for k in range(img_length)]
k = 0
i = 0
while k < img_length:
    for i in range(8):
        # if i == 0:
        # img_red[k][i] = -1 * (256 - img_red[k][i])
        info_matrix[k][i] = (img_red[k][i]) / (2 ** 7)
        i += 1
    k += 1
    i = 0

# 重新产生相同的混叠矩阵
img_before_interleaving = [[0 for i in range(8)] for j in range(img_length)]
key3 = input("第3密钥(混叠):")
key_check(key3)
key3_list = list()
for v in key3:
    key3_list.append(int(v))

# 反向使用interleave
j = 0
while j < img_length:
    i = 0
    for pw in key3_list:
        if i > 7:
            i = 0
        else:
            img_before_interleaving[j][pw] = info_matrix[j][i]
        i += 1
        pw += 1
    j += 1

print("已解开混叠加密!")

signal = stage_2(img_length)
print("噪声信号已重建!")

# 还原矩阵噪声乘法嵌入处理
p = 0
o = 0
img_matrix_after_LSB = [[0 for i in range(8)] for j in range(img_length)]
while o < img_length:
    while p < 8:
        if signal[o][p] != 0:
            img_matrix_after_LSB[o][p] = int(img_before_interleaving[o][p] // signal[o][p])
        p += 1
    o += 1
    p = 0
print("矩阵嵌入已解开!")

# 还原LSB
key1 = input("第1密钥(LSB):")
key_check(key1)
key1_list = list()
for i in key1:
    key1_list.append(int(i))
img_before_LSB = [[0 for i in range(8)] for j in range(img_length // 8)]
j = 0
while j < img_length // 8:
    i = 0
    for pw in key1_list:
        if i > 7:
            i = 0
        if j >= 0:
            img_before_LSB[j][i] = img_matrix_after_LSB[pw + (8 * j)][7]
        i += 1
    j += 1
print("LSB已还原!")

word_num = 0
while 1:
    if 0 in img_before_LSB[word_num]:
        break
    else:
        word_num += 1  # 从含0行开始就不再存储信息

# 加密时将0全转化为了-1,解密时应当解开
i = 0
j = 0
while j < word_num:
    while i < 8:
        if img_before_LSB[j][i] == 2:
            img_before_LSB[j][i] = 0
        else:
            img_before_LSB[j][i] = 1
        i += 1
    j += 1
    i = 0

img_demical = [0 for i in range(img_length // 8)]

i = 7
j = 0
# 从二进制转回十进制
while j < word_num:
    word_asc = 0
    while i > -1:
        word_asc += img_before_LSB[j][i] * (2 ** (7 - i))
        i -= 1
    img_demical[j] = word_asc
    j += 1
    i = 7
i = 0
j = 0

result_list=""
for i in range(word_num):
    if img_demical[i] == 92:
        break
    else:
        result_list += (chr(img_demical[i]))
print("解密结果:"+result_list)