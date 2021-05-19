import cv2
from reusable_funcs import *
import numpy as np
changed_flag=False
im_matrix_origin = np.array(cv2.imread("output.png"))
def de(im_matrix,RGB_pos):
    im_red=im_matrix[:,:,RGB_pos]
    im_red_bin=np.empty([im_matrix.shape[0],im_matrix.shape[1],8], dtype = int, order = 'C')
    global changed_flag
    for i in range(im_red.shape[0]):
        for j in range(im_red.shape[1]):
            bi=bin(im_red[i][j])[2:]
            if(len(bi)<8):
                for x in range(8-len(bi)):
                    bi="0"+bi
            for bilen in range(8):
                im_red_bin[i][j][bilen]=int(bi[bilen])
    for i in range(im_red_bin.shape[0]-1):
        for j in range(im_red_bin.shape[1]-1):
            a=np.sum(im_red_bin[i][j][:-1])
            if(im_red_bin[i][j][7]!=(1 if(a%2==0) else 0)):
                if(changed_flag==False):
                    print("图像已被篡改!")
                    changed_flag = True
                im_matrix[i][j][0]=0
                im_matrix[i][j][1]=0
                im_matrix[i][j][2]=0
            j+=1
    return im_matrix
im_matrix_R=de(im_matrix_origin,0)
im_matrix_G=de(im_matrix_R,1)
im_matrix_B=de(im_matrix_G,2)
cv2.imwrite("tested.png", im_matrix_B)