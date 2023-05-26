#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 22:15:19 2019

@author: mianwei
"""


from UsefulFunctions import graycode, binaryToGray
import numpy as np
import cv2
#u,v = graycode('CalibrationPatterns', 'FirstPos')
#u,v = graycode('Test', 'FirstPos')
folderName = 'Test'

H = 720
W = 1280
xVals = list(range(W))
yVals = list(range(H))
y, x = np.meshgrid(yVals, xVals, sparse=False, indexing='ij')
u = x.astype("uint16")
v = y.astype("uint16")


for k in range(2):
    counter= k + 1;
    if k == 0:
        curVal = binaryToGray(v)
    else:
        curVal = binaryToGray(u)


    
    curVal = curVal.reshape(-1,1)     


    cur_large = np.floor(curVal / 256); 

    cur_small = np.mod(curVal, 256);

    left_val = np.unpackbits(cur_large.astype('uint8'), axis = 1);
    right_val = np.unpackbits(cur_small.astype('uint8'), axis=1);
    

    for i in range(3):
        curIm = left_val[:,5+i].reshape(H,W)
        
        cv2.imwrite("%s/FirstPosPositive%02d.bmp" % (folderName, counter), curIm * 255)
        
        cv2.imwrite("%s/FirstPosNegative%02d.bmp" % (folderName, counter), (1-curIm) * 255)
        
        
        counter = counter + 2
        
        
    for i in range(8):
        curIm = right_val[:,i].reshape(H,W)
        
        cv2.imwrite("%s/FirstPosPositive%02d.bmp" % (folderName, counter), curIm * 255)
        
        cv2.imwrite("%s/FirstPosNegative%02d.bmp" % (folderName, counter), (1-curIm) * 255)
        
        counter = counter + 2

