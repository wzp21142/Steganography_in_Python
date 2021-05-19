import cv2
from reusable_funcs import *
import numpy as np
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
def get_text():
    text_array=np.empty([8], dtype = int, order = 'C')
    count=0
    count2=0
    word = []
    for i in range(im_red_bin.shape[0]):
        for j in range(im_red_bin.shape[1]):
            word.append(im_red_bin[i][j][7])
            count+=1
            if count==8:
                if count2==3:
                    return text_array[1:,:]
                count2+=1
                text_array=np.row_stack((text_array,np.array(word)))
                count=0
                word = []
text_array=get_text()
key=input("请输入密钥:")
key_check(key)
key_list=[]
for key_single in key:
    key_list.append(int(key_single))
decode_list=[0,0,0,0,0,0,0,0]
for i in range(len(key_list)):
    wordlen=0
    for t in key_list:
        if i==key_list[wordlen]:
            decode_list[i]=wordlen
            break
        wordlen+=1
text_array=np.row_stack((text_array[:2,np.argsort(decode_list)],text_array[2,:]))
result=[]
count=0
true=0
for i in text_array:
    wd=""
    for n in i:
        wd=wd+str(n)
    if count<2:
        result.append(int(wd,2))
    else:
        true=(int(wd,2))
    count+=1
print("水印形状为:"+str(result))
watermark=np.zeros((result[0],result[1]))
for i in range(result[0]):
    for j in range(result[1]):
        if(result[0]!=true):
            if(im_red_bin[i][j+7][5]==1):
                watermark[i][j]=255
        elif(i==0):
            if(im_red_bin[i][j+24][7]==1):
                watermark[i][j]=255
        else:
            if(im_red_bin[i][j][7]==1):
                watermark[i][j]=255
cv2.imshow("watermark",watermark)
cv2.imwrite("watermark_recover.bmp",watermark)
cv2.waitKey(0)
cv2.destroyAllWindows()
