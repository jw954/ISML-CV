
# coding: utf-8

# In[5]:

import os
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
import scipy.io as sio
from matplotlib import pyplot as plt
from UsefulFunctions import *
import shutil
import glob

folderName = "../../SLCode"
outputFolder = "undistorted_fullsize"




#Useful parameters for calibration
numberPose = 30
#width,height = (1563,1043)
width,height = (5208,3476)
lengths = 24.2
chessH,chessW = (13,15)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100000, 1e-10)


camCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100000, 1e-10)
calibFlags =   cv2.CALIB_RATIONAL_MODEL 


objp = np.zeros((chessH*chessW,3), np.float32)
objp[:,:2] = np.mgrid[0:chessH,0:chessW].T.reshape(-1,2)
objp = objp * lengths;

#data=np.load('cameraParameters.npz');
#newcameramtx, roi=cv2.getOptimalNewCameraMatrix(data['cameraMatrix1'],data['distCoeffs1'],(width,height),1,(width,height))
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
projpoints = []

imageFolders = ["Col", "Row"]
for folderNo in range(0,numberPose):
	curFolder = "%s/Pose%d" % (folderName, folderNo + 1)
	print(curFolder)
	
	#Reads in two off phase images and get all white
	curValue = 0
	for name in glob.glob("%s/Row/tiff/*.tiff" % curFolder):
		
		tempValue = int(name[-9:-5])
		if tempValue > curValue:
			curValue = tempValue
			
	im_rgb = cv2.imread("%s/Row/tiff/IMG_%04d.tiff" % (curFolder, curValue))
	
	gray = cv2.cvtColor(im_rgb, cv2.COLOR_RGB2GRAY);
	
	#Just incase we want to blur the image
	#gray = cv2.medianBlur(gray,3)

	
	#dst = cv2.undistort(gray, data['cameraMatrix1'], data['distCoeffs1'], None, newcameramtx)
	ret, corners = cv2.findChessboardCorners(gray, (chessH,chessW),flags = cv2.CALIB_CB_ADAPTIVE_THRESH)
	
	
	if ret == True:
		
		objpoints.append(objp)
		
		
		
		corners2 = cv2.cornerSubPix(gray,corners,(10,10),(-1,-1),criteria)
		
		imgpoints.append(corners2)


	#


# In[64]:
ret1, mtx1, dist1, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None,criteria=camCriteria, flags=calibFlags)

print(len(objpoints))
print(ret1)
print(mtx1)
print(dist1)
exit()
np.savez('single_undist.npz', retval=ret1, cameraMatrix1=mtx1, distCoeffs1=dist1);


newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx1,dist1,(width,height),0,(width,height))

print(roi)


try:
	shutil.rmtree(outputFolder)
	os.mkdir(outputFolder)
except:
	os.mkdir(outputFolder)
	
for folderNo in range(0,numberPose):
	newFolderName1 = "%s/Pose%d" % (outputFolder, folderNo + 1)
	try:
		shutil.rmtree(newFolderName1)
		os.mkdir(newFolderName1)
	except:
		os.mkdir(newFolderName1)
		
	for dir in range(0,2):
		curFolder = "%s/Pose%d/%s/tiff" % (folderName, folderNo + 1, imageFolders[dir])
		print(curFolder)
	
		newFolderName2 = "%s/Pose%d/%s" % (outputFolder, folderNo + 1 , imageFolders[dir])
		try:
			shutil.rmtree(newFolderName2)
			os.mkdir(newFolderName2)
		except:
			os.mkdir(newFolderName2)
		
		curOutFolder = "%s/Pose%d/%s/tiff" % (outputFolder, folderNo + 1 , imageFolders[dir])
		
		try:
			shutil.rmtree(curOutFolder)
			os.mkdir(curOutFolder)
		except:
			os.mkdir(curOutFolder)
			
		pathName =    "%s/*.tiff" % curFolder
		print(pathName)
		for name in glob.glob(pathName):
			a = cv2.imread(name)

			newImage = cv2.undistort(a, mtx1, dist1, None, newcameramtx)
			#x,y,w,h = roi
			#newImage = newImage[y:y+h, x:x+w]
			#print(w,h)
			cv2.imwrite(name.replace(curFolder, curOutFolder), newImage)
