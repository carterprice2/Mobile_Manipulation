# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:09:18 2020

@author: Carter
"""

#convert .png to .jpg

import cv2
import os
import glob

path = '../../images/'
lis = os.listdir(path)

better_lis = glob.glob(path + "*.png")


pic = cv2.imread(better_lis[0],1)

cv2.imshow("test", pic)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imwrite("SfM_jpgs/" + better_lis[0][13:-4] + ".jpg", pic)

for im in better_lis:
    pic = cv2.imread(im,1)
    cv2.imwrite("SfM_jpgs/" + im[13:-4] + ".jpg", pic)