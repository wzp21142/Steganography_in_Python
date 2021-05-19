import numpy as np
import cv2
def Watermarking_DCT(coverImage, watermarkImage):
    coverImage = cv2.resize(coverImage, (512, 512))
    watermarkImage = cv2.resize(watermarkImage, (64, 64))
    ret, watermarkImage = cv2.threshold(watermarkImage, 128, 255, cv2.THRESH_BINARY)
    cv2.imshow('water', watermarkImage)
    blockSize = 8
    coverImage=np.float32(coverImage)
    for i in range(64):
        for j in range(64):
            block_88=coverImage[blockSize*i:blockSize*i+8,blockSize*j:blockSize*j+8]
            dct_block = cv2.dct(block_88)
            if(watermarkImage[i][j]==255):
                if(dct_block[5,2]<dct_block[4,3]):
                    temp=dct_block[5,2]
                    dct_block[5, 2]=dct_block[4,3]
                    dct_block[4, 3]=temp
            else:
                if (dct_block[5, 2] > dct_block[4, 3]):
                    temp = dct_block[5, 2]
                    dct_block[5, 2] = dct_block[4, 3]
                    dct_block[4, 3] = temp
            coverImage[blockSize*i:blockSize*i+8,blockSize*j:blockSize*j+8] = cv2.idct(dct_block)

    watermarkedImage_8 = np.uint8(coverImage)
    cv2.imshow('watermarked', watermarkedImage_8)
    cv2.imwrite("watermarked.bmp", watermarkedImage_8)

def Extract_DCT(watermarkedImage,x):
    coverImage = cv2.resize(watermarkedImage, (512, 512))
    blockSize = 8
    watermark=np.zeros((64, 64))
    for i in range(64):
        for j in range(64):
            block_88=np.float32(coverImage[blockSize*i:blockSize*i+8,blockSize*j:blockSize*j+8])
            dct_block = cv2.dct(block_88)
            if(dct_block[5,2]<dct_block[4,3]):
                watermark[i,j]=0
            else:
                watermark[i, j] = 255

    watermarkImage = cv2.imread('test.bmp',0)
    watermarkImage = cv2.resize(watermarkImage, (64, 64))
    ret, watermarkImage = cv2.threshold(watermarkImage, 128, 255, cv2.THRESH_BINARY)
    count=0
    for i in range(64):
        for j in range(64):
            if(watermark[i][j]==watermarkImage[i][j]):
                count+=1
    print("attack"+str(x)+":"+str(count/(64*64)))
    cv2.imshow('watermark'+str(x), watermark)

#coverImage = cv2.imread('lenna.bmp',0)
#watermarkImage = cv2.imread('test.bmp',0)
#Watermarking_DCT(coverImage,watermarkImage)
watermarkedImage = cv2.imread('watermarked.bmp',0)
Extract_DCT(watermarkedImage,"norm")
watermarkedImage = cv2.imread('attack1.bmp',0)
Extract_DCT(watermarkedImage,2)
watermarkedImage = cv2.imread('attack2.bmp',0)
Extract_DCT(watermarkedImage,3)
watermarkedImage = cv2.imread('attack3.bmp',0)
Extract_DCT(watermarkedImage,4)
cv2.waitKey(0)
cv2.destroyAllWindows()