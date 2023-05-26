
# coding: utf-8

# In[5]:


from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
import scipy.io as sio
from matplotlib import pyplot as plt
import shutil
import glob
folderName = "CalibFolder/calibrationPose1"
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
try:
    shutil.rmtree(outputFolderName)
    os.makedirs(outputFolderName)
except:
    os.makedirs(outputFolderName)
    

a = sio.loadmat("CalibParams_undist.mat")

mtx = a['cameraMatrix']
dist = a['dist']
ret = a['retval']  

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width,height), 0, (width,height))


for x in glob.glob('%s/*.%s' % (folderName, formatName)):
    curIm = cv2.imread(x, cv2.IMREAD_GRAYSCALE)
    
    bucket1 = curIm[:,:width]
    bucket2 = curIm[:,width:]
    newImage1 = cv2.undistort(bucket1, mtx, dist, None, newcameramtx)
    newImage2 = cv2.undistort(bucket2, mtx, dist, None, newcameramtx)

    cv2.imwrite(x.replace(folderName, outputFolderName), np.concatenate((newImage1, newImage2), axis=1))
            
            
    