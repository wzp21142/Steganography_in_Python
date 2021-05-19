### 信息隐藏技术演示脚本

由于目前开源的信息隐藏脚本大多基于Matlab实现的现实，为方便信息隐藏技术和Python的学习需要，本项目使用Python实现了多个信息隐藏领域的常见算法。如有需要可以任意用作二次开发。各工程介绍见下。

##### SSIS

详见Lisa M. Marvel等人的论文*Spread Spectrum Image Steganography*。文中只给出了其技术的基本框架，项目中对其框架进行了具体算法的实现。

**LSB**

最低比特位信息隐藏，代码实现了图像信息的隐藏。输入可以是两幅任意RGB图像，嵌入时将待嵌入图像改为二值图存储到载体的0号通道（可以自行在代码中修改），并扩展加入了较弱的演示用密钥认证的功能。

**LSB_watermark**

最低比特位奇偶校验脆弱水印，对RGB图像中所有通道的最低有效位作了最低比特位奇偶校验嵌入，对图像篡改（如涂抹）后，使用黑色将被涂抹的位置标出。

**DCT_watermark**

将载体形状resize为（512,512）大小后按8\*8大小分块，每块都使用DCT系数矩阵中（5,2）（4,3）的相对大小存储1bit信息（（5,2）>（4,3）为1，（5,2）<（4,3）为0），总共可存储一个64\*64大小的二值图。附带的攻击中attack1为涂抹，2为添加椒盐噪声，3为添加高斯噪声，已打印出了信息的还原率。