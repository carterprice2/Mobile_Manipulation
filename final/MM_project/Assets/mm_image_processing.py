# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 22:28:14 2020

function for grabbing the center pixel of the lettuce

@author: Carter and Gerry
"""

#computer vision piece of project 

import cv2
import numpy as np
import imutils


def show_pic(im):
    cv2.imshow("original", im)
    cv2.waitKey()
    cv2.destroyAllWindows()


def get_center_width_height(im, show = False):
    '''
    input: BGR image from read using openCV
    output: centroid of green contour and width and heigh of bounding box 
    cX, cY, w, h
    '''
    #convert to HSV
    hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    
    #color threshold
    #correct HSV
    #green = np.uint8([[[0,255,0]]])
    #hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([50,50,50])
    upper_green = np.array ([70,255,255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    #run a contour detection on the masked image 
    cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = cnts[0]
    for cnt in cnts:
        if len(cnt) > len(c):
            c = cnt
    
    #find contour centroid 
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"]/ M["m00"]) 
    
    #find diameter of contour
    x,y,w,h = cv2.boundingRect(c)
    #print("width ", w, " height ", h)
    
    if show:
        #visualize the center
        cv2.drawContours(im,[c], -1, (0,255,0),2)
        cv2.circle(im, (cX,cY), 7, (255,255,255), -1)
        cv2.putText(im, "center", (cX -20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        #visualize bounding box
        cv2.rectangle(im,(x,y),(x+w,y+h), (255,0,0), 2)
        
        show_pic(im)
        show_pic(mask)
        
    return cX,cY,w,h

if __name__ == '__main__':
    path = "../../images/9.png"
    im = cv2.imread(path,1)
    show_pic(im)
    print(im.shape)
    print(get_center_width_height(im, show=True))