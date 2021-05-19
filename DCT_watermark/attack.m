f=imread('watermarked.bmp');
g=imnoise(f,'gaussian',0.2);             
imwrite(g,'attack2.bmp')
g=imnoise(f,'salt & pepper',0.2);           
imwrite(g,'attack3.bmp')