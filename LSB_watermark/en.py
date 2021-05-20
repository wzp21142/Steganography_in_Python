import cv2
import numpy as np

# 图像信息读取
im_matrix_origin = np.array(cv2.imread("test.png"))
def en(im_matrix,RGB_pos):
    im_red=im_matrix[:,:,RGB_pos]
    im_red_bin=np.empty([im_matrix.shape[0],im_matrix.shape[1],8], dtype = int, order = 'C')
    image_length = len(im_matrix)
    for i in range(im_red.shape[0]):
        for j in range(im_red.shape[1]):
            bi=bin(im_red[i][j])[2:]
            if(len(bi)<8):
                for x in range(8-len(bi)):
                    bi="0"+bi
            for bilen in range(8):
                im_red_bin[i][j][bilen]=int(bi[bilen])
    i=0
    j=0
    for i in range(im_red_bin.shape[0]-1):
        for j in range(im_red_bin.shape[1]-1):
            a=np.sum(im_red_bin[i][j][:-1])
            im_red_bin[i][j][7]=(1 if(a%2==0) else 0)
            j+=1
    for _i in range(i+1):
        if(_i==i+1):
            break
        for _j in range(j):
            x=""
            for t in im_red_bin[_i][_j]:
                x=x+str(t)
            im_matrix[_i][_j][RGB_pos]=int(x,2)
    return im_matrix
im_matrix_R=en(im_matrix_origin,0)
im_matrix_G=en(im_matrix_R,1)
im_matrix_B=en(im_matrix_G,2)
cv2.imwrite("output.png", im_matrix_B)