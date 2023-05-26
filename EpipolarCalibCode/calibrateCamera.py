 
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
folderName = "checkerboardIms"

#Useful parameters for calibration
numberPose = 30
posesToTry = np.ones((numberPose,1));
#use to prune poses, minus 1 to pose number, cuz python indexing
#posesToTry[[1, 22, 24, 16,7, 19]]= 0;
#width,height = (1563,1043)
width,height = (324,320)
lengths = 24.2
chessH,chessW = (7,10)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100000, 1e-6)


camCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100000, 1e-10)
calibFlags =   cv2.CALIB_RATIONAL_MODEL #False cv2.CALIB_ZERO_TANGENT_DIST + cv2.CALIB_FIX_K1+ cv2.CALIB_FIX_K2+ cv2.CALIB_FIX_K3+ cv2.CALIB_FIX_K4+ cv2.CALIB_FIX_K5+ cv2.CALIB_FIX_K6

objp = np.zeros((chessH*chessW,3), np.float32)
objp[:,:2] = np.mgrid[0:chessH,0:chessW].T.reshape(-1,2)
objp = objp * lengths;



# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
projpoints = []


for folderNo in range(0,numberPose):			
    gray = cv2.imread("%s/%04d.png" % (folderName, folderNo), cv2.IMREAD_GRAYSCALE)
	
    gray = gray[:,324:]
	
	#dst = cv2.undistort(gray, data['cameraMatrix1'], data['distCoeffs1'], None, newcameramtx)
    ret, corners = cv2.findChessboardCorners(gray, (chessH,chessW),flags = cv2.CALIB_CB_ADAPTIVE_THRESH)
	
	
    if (ret == True) & (posesToTry[folderNo] == 1):
        objpoints.append(objp)
		
		
		
        corners2 = cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),criteria)
		
        imgpoints.append(corners2)

	#

print(len(objpoints))
# In[64]:
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None, flags = calibFlags, criteria=camCriteria)

	


print(ret)
print(dist)
sio.savemat("CalibParams_undist.mat", {'cameraMatrix': mtx, 'dist': dist, 'retval': ret} )



