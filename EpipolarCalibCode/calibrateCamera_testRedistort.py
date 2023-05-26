
# coding: utf-8

# In[5]:


import os
from os import listdir, makedirs
from os.path import isfile, join
import numpy as np
import cv2
import scipy.io as sio
from matplotlib import pyplot as plt
import shutil
import glob
from opencv_distort import *

folderName = "checkerboardIms"
formatName = 'png'
#Useful parameters for calibration
numberPose = 50
posesToTry = np.ones((numberPose,1));
#use to prune poses, minus 1 to pose number, cuz python indexing
#posesToTry[[1, 22, 24, 16,7, 19]]= 0;
#width,height = (1563,1043)
width,height = (324,320)
lengths = 24.2
chessH,chessW = (7,10)

outputFolderName = '%s_undistorted' % folderName
outputFolderName2 = '%s_redistorted' % folderName
try:
    shutil.rmtree(outputFolderName)
    os.makedirs(outputFolderName)
    shutil.rmtree(outputFolderName2)
    os.makedirs(outputFolderName2)
except:
    os.makedirs(outputFolderName)
    os.makedirs(outputFolderName2)
    

a = sio.loadmat("CalibParams_undist.mat")

mtx = a['cameraMatrix']
dist = a['dist']
ret = a['retval']  

u,v = cv2.initUndistortRectifyMap(mtx,None,None, mtx,(width,height), cv2.CV_32FC1)

for x in glob.glob('%s/*.%s' % (folderName, formatName)):
    curIm = cv2.imread(x, cv2.IMREAD_GRAYSCALE)
    
    bucket1 = curIm[:,:width]
    bucket2 = curIm[:,width:]
    newImage1 = cv2.undistort(bucket1, mtx, dist, None, mtx)
    newImage2 = cv2.undistort(bucket2, mtx, dist, None, mtx)
    image2_redistorted = distortimage(newImage2, mtx, dist)
    
    cv2.imwrite(x.replace(folderName, outputFolderName), np.concatenate((newImage1, newImage2), axis=1))
    cv2.imwrite(x.replace(folderName, outputFolderName2), np.concatenate((bucket1, image2_redistorted), axis=1))

            
    
