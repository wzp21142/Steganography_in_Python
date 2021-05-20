import cv2
from reusable_funcs import *
import numpy as np

two_im_matrix = np.array(cv2.imread("embd.bmp",0))
ret, two_im_matrix = cv2.threshold(two_im_matrix, 128, 255, cv2.THRESH_BINARY)
info_list = np.array(two_im_matrix.shape)
print("请注意:密钥请将0~7进行任意排列后输入,共8位")
key = input("请输入密钥: ")
key_check(key)

i = 0
for word in info_list.shape:
    if word > 255:
        print("输入图片过大!")
        exit(1)
# print(info_list)
# 对应信息的每个字符的ascii值存入list
binary_info_list = [[0 for i in range(8)] for j in range(2)]  # 初始化二进制信息矩阵,ascii码上限255,为8列
i = 0
j = 7
# 将信息对应的二进制值存入矩阵中
info0=info_list[0]
while i < 2:
    while j > -1:
        binary_info_list[i][j] = info_list[i] % 2
        info_list[i] = (info_list[i] - binary_info_list[i][j]) // 2
        j -= 1
    i += 1
    j = 7

binary_info_list = np.array(binary_info_list)
key_list = []
for key_single in key:
    key_list.append(int(key_single))
key_list = np.array(key_list)
binary_info_list = binary_info_list[:, np.argsort(key_list)]
code=[]
for i in range(binary_info_list.shape[1]):
    code.append(info0 % 2)
    info0 = (info0 - code[i]) // 2
code=np.array(code[::-1])
binary_info_list=np.row_stack((binary_info_list,np.array(code)))
# 图像信息读取
im_matrix = np.array(cv2.imread("test.png"))


def imwrite(channel, binary_ino_list, im_matrix_im):
    im_red = im_matrix_im[:, :, channel]
    im_red_bin = np.empty([im_matrix_im.shape[0], im_matrix_im.shape[1], 8], dtype=int, order='C')

    for i in range(im_red.shape[0]):
        for j in range(im_red.shape[1]):
            bi = bin(im_red[i][j])[2:]
            if (len(bi) < 8):
                for x in range(8 - len(bi)):
                    bi = "0" + bi
            for bilen in range(8):
                im_red_bin[i][j][bilen] = int(bi[bilen])
    i = 0
    j = 0
    for n in binary_ino_list:
        for t in n:
            im_red_bin[i][j][7] = t
            j += 1
            if (j == len(im_matrix_im[0])):
                i += 1
                j = 0
    global two_im_matrix
    bucket=np.zeros((8))
    count=0
    for m in range(two_im_matrix.shape[0]):
        countr=0
        for n in range(two_im_matrix.shape[1]):
            bucket[count]=two_im_matrix[m][n]
            count+=1
            if(count==8):
                bucket=bucket[np.argsort(key_list)]
                for x in bucket:
                    if x==0:
                        if(m==0):
                            im_red_bin[m][24+countr][7]=0
                        else:
                            im_red_bin[m][countr][7] = 0
                    else:
                        if(m==0):
                            im_red_bin[m][24+countr][7]=1
                        else:
                            im_red_bin[m][countr][7] = 1
                    countr+=1
                count=0
            if(n==two_im_matrix.shape[1]-24 and m==0):
                break
    for _i in range(two_im_matrix.shape[0]):
        for _j in range(two_im_matrix.shape[1]):
            x = ""
            for t in im_red_bin[_i][_j]:
                x = x + str(t)
            im_matrix_im[_i][_j][channel] = int(x, 2)
    return im_matrix_im
im_matrix1=imwrite(0,binary_info_list,im_matrix)
cv2.imwrite("output.png", im_matrix1)
