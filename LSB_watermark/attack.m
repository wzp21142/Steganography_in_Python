f=imread('output_origin.png');
g=imnoise(f,'gaussian',0.1);             
imwrite(g,'attack3.bmp')
g=imnoise(f,'salt & pepper',0.1);           
imwrite(g,'attack4.bmp')