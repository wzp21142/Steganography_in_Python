import cv2
from SSIS.reusable_funcs import *

info = input("请输入待隐藏信息: ")
print("请注意:后续所有密钥请将0~7进行任意排列后输入,共8位")
info_length = len(info)
info_list = list()
for word in range(info_length):
    info_list.append(0)  # 初始化信息列表
i = 0
for word in info:
    if ord(word) > 255:
        print("输入序列中存在不支持的字符!")
        exit(1)
    info_list[i] = ord(word)
    i += 1
# print(info_list)
# 对应信息的每个字符的ascii值存入list
binary_info_list = [[0 for i in range(8)] for j in range(info_length)]  # 初始化二进制信息矩阵,ascii码上限255,为8列
i = 0
j = 7
# 将信息对应的二进制值存入矩阵中
while i < info_length:
    while j > -1:
        binary_info_list[i][j] = info_list[i] % 2
        info_list[i] = (info_list[i] - binary_info_list[i][j]) // 2
        j -= 1
    i += 1
    j = 7
# print(binary_info_list)
i = 0
j = 0
# 为方便后续操作,与矩阵原有0区分,将所有0值换为2
while j < info_length:
    while i < 8:
        if binary_info_list[j][i] == 0:
            binary_info_list[j][i] = 2
        i += 1
    j += 1
    i = 0
# print(binary_info_list)

# 图像信息读取
im_matrix = cv2.imread("test.png")
# 获取每一img像素对应的R值存入矩阵中,进行LSB加密
image_length = len(im_matrix)
image_pixels = img_red_to_matrix(im_matrix)

if info_length > image_length // 8:
    print("图片大小不足以容纳以上信息!")
    exit(1)
# 转为二进制
image_pixels_binary = [[0 for i in range(8)] for j in range(image_length * 8)]  # 8列(RGB范围0~255)*8*len行(信息最大长度)
i = 7  # 与原矩阵中的列数进行对照(原矩阵1列=binary中8列)
j = 0  # 原矩阵行计数(此处在新矩阵中称为高度更加合适,为方便后续与信息表进行加密,声明为了二维列表)
k = 0  # 原矩阵列计数+新矩阵行计数
while j < image_length:
    while k < 8:
        while i > -1:
            image_pixels_binary[k + (8 * j)][i] = image_pixels[j][k] % 2  # 将十进制矩阵映射到二进制矩阵中
            image_pixels[j][k] = (image_pixels[j][k] - image_pixels_binary[k + (8 * j)][i]) // 2
            i -= 1
        k += 1
        i = 7
    j += 1
    k = 0

# 第一轮,LSB加密
key1 = input("第1密钥(LSB):")
key_check(key1)
LSB_key = list()
# LSB密钥按位初始化到列表中
for i in key1:
    LSB_key.append(int(i))
# print(LSB_key)
i = 0
j = 0
while j < info_length:
    for key_bit in LSB_key:
        if i > 7:
            i = 0
        image_pixels_binary[key_bit + (8 * j)][7] = binary_info_list[j][i]  # 像素矩阵中对应位置的末位改存信息
        i += 1
    j += 1
    i = 0
print("LSB算法执行完毕!")

# 第二轮,伪随机噪声加密
signal_interleaved = stage_2(image_length)
print("已生成噪声信号!")

u = 0
v = 0
img_embedded = [[0 for i in range(8)] for j in range(image_length)]
# 对两个矩阵进行乘法嵌入(embedded)
while u < image_length:
    while v < 8:
        img_embedded[u][v] = image_pixels_binary[u][v] * signal_interleaved[u][v]
        v += 1
    u += 1
    v = 0

# 对噪声矩阵和图像矩阵进行混叠
img_interleaved = [[0 for i in range(8)] for j in range(image_length)]
key3 = input("第3密钥(混叠):")
key_check(key3)
length = len(key3)
key3_list = list()
for v in key3:
    key3_list.append(int(v))

interleaving(image_length, key3_list, img_interleaved, img_embedded)

print("混叠完毕!")

# 处理完毕后,重新将矩阵转回10进制
img_interleaved_decimal = [[0 for i in range(8)] for k in range(image_length)]
k = 0
i = 0
while k < image_length:
    for i in range(8):
        img_interleaved_decimal[k][i] = (img_interleaved[k][i]) * (2 ** 7)
        i += 1
    k += 1
    i = 0

# 写回
for i in range(image_length):
    for j in range(8):
        im_matrix[i, j, 2] = img_interleaved_decimal[i][j]

cv2.imwrite("output.png", im_matrix)
print("OK!")
