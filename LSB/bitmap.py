import numpy as np
import cv2
im_matrix = np.array(cv2.imread("output.png"))
im_red=im_matrix[:,:,0]
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
im_red_bin[im_red_bin == 1] = 255
for i in range(8):
    cv2.imwrite("bitmap"+str(i)+".bmp", im_red_bin[:,:,i])
