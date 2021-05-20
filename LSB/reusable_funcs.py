import re
from random import seed, gauss
from numpy import *


def key_check(__key):
    if (len(__key) != 8) or (not re.findall('^[0-7]+$', __key)):
        print("密钥格式有误!")
        exit(1)
    for i in __key:
        for j in __key[__key.index(i) + 1:]:
            if j == i:
                print("密钥格式有误!")
                exit(1)
    else:
        return