
# coding: utf-8

# In[5]:




import numpy as np
import cv2
from matplotlib import pyplot as plt
from UsefulFunctions import *
import scipy.io as sio

mainFolder = "CalibFolder"

folderNameLB = "calibrationPose1_undistorted"
folderNameUB = "calibrationPose2_undistorted"
    
H = 320
W = 324


def computeError(F, pts1,pts2):
    
    projectedLine_in1 = np.matmul(pts2, F.T)
    projectedLine_in1 = projectedLine_in1 / np.tile(np.linalg.norm(projectedLine_in1[:,:2], axis = 1).reshape(-1,1), 3)
    
    alldist_1 = np.sum(projectedLine_in1 * pts1, axis = 1);
    
    alldist_1 = np.mean(np.abs(alldist_1))
    
    projectedLine_in2 = np.matmul(pts1, F)
    projectedLine_in2 = projectedLine_in2 / np.tile(np.linalg.norm(projectedLine_in2[:,:2], axis = 1).reshape(-1,1), 3)
        
    alldist_2 = np.sum(projectedLine_in2 * pts2, axis = 1);
    
    alldist_2 = np.mean(np.abs(alldist_2))
    
    
    curErr = np.max((alldist_2, alldist_1))
    
    
    return curErr
    
    
    
dual_y,dual_x= np.mgrid[1:(H+1),1:(W+1)].astype("uint16")


primal1_x,primal1_y = graycode("%s/%s" % (mainFolder, folderNameLB), "FirstPos", verbose = True)


primal2_x,primal2_y = graycode("%s/%s" % (mainFolder,folderNameUB), "FirstPos", verbose = True)

#TRANSCRIBE THIS AS MATLAB

gradientIm = np.stack((dual_x, primal1_x, primal2_x), axis = 2).astype("float") / (2**16-1);
plt.imshow(64 *gradientIm);
#Click 3 times
#plt.show()
#x = plt.ginput(2, show_clicks = True)
x = [[75,75], [250,250]]
print(x)
#plt.show()

print(x[1][1])
N = 100

input_x = np.linspace(np.min((x[0][0], x[1][0])), np.max((x[0][0], x[1][0])), N).astype("int");
input_y = np.linspace(np.min((x[0][1], x[1][1])), np.max((x[0][1], x[1][1])), N).astype("int");

ind_y, ind_x = np.meshgrid(input_y -1, input_x - 1)

primal_coordinates = [];
dual_coordinates   = [];

tmp_x = primal1_x[ind_y,ind_x];
tmp_y = primal1_y[ind_y,ind_x];

primal_coordinates1 = np.concatenate((tmp_x.reshape(N**2,-1), tmp_y.reshape(N**2,-1)), axis = 1)

tmp_x = primal2_x[ind_y,ind_x];
tmp_y = primal2_y[ind_y,ind_x];

primal_coordinates2 = np.concatenate((tmp_x.reshape(N**2,-1), tmp_y.reshape(N**2,-1)), axis = 1)

primal_coordinates = np.concatenate((primal_coordinates1,primal_coordinates2), axis = 0)

tmp_x = dual_x[ind_y,ind_x];
tmp_y = dual_y[ind_y,ind_x];

dual_coordinates1 = np.concatenate((tmp_x.reshape(N**2,-1), tmp_y.reshape(N**2,-1)), axis = 1)
dual_coordinates= np.concatenate((dual_coordinates1,dual_coordinates1), axis = 0)



F, mask = cv2.findFundamentalMat(primal_coordinates,dual_coordinates,cv2.FM_RANSAC,0.5, 0.99999)

pts1 = np.concatenate((dual_coordinates, np.ones((2*N**2, 1))), axis = 1).astype("float")
pts2 = np.concatenate((primal_coordinates, np.ones((2*N**2, 1))), axis = 1).astype("float")

matValues = np.matmul(np.matmul(pts1, F), pts2.T)

err1 = computeError(F,pts1,pts2)
print(err1)
F2, mask = cv2.findFundamentalMat(primal_coordinates,dual_coordinates,cv2.FM_8POINT)

err2 = computeError(F2,pts1,pts2)
print(err2)

if err1  < err2:
    F = F2
#np.mean(diag([dual_coordinates ones(size(dual_coordinates,1),1)]*...
#      F*[primal_coordinates ones(size(primal_coordinates,1),1)]'))


sio.savemat("fundamentalmatrix.mat",{"F" : F})





