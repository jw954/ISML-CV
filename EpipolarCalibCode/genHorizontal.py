#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 22:15:19 2019

@author: mianwei
"""


from UsefulFunctions import graycode, binaryToGray
import numpy as np
import cv2
import os
#u,v = graycode('CalibrationPatterns', 'FirstPos')
#u,v = graycode('Test', 'FirstPos')
folderName = 'Horizontal'

try:
    os.rmdir(folderName)
    os.mkdir(folderName)
except:
    os.mkdir(folderName)

H = 720
W = 1280
xVals = list(range(W))
yVals = list(range(H))
y, x = np.meshgrid(yVals, xVals, sparse=False, indexing='ij')
u = x.astype("uint16")
v = y.astype("uint16")


width = 10;

counter = 0
for k in np.arange(0, H, width):
    curIm = np.zeros((H,W))
    
    curIm[k : k+width,:] = 255;
    
    cv2.imwrite("%s/Hori%02d.bmp" % (folderName, counter), curIm)
    counter = counter + 1
    
