import numpy as np
import cv2
from matplotlib import pyplot as plt
from UsefulFunctions import *
import scipy.io as sio
import os
import scipy.linalg 
from PIL import Image


a = sio.loadmat("fundamentalmatrix.mat")

F= a["F"]
# Pixel coordinates of both mask and projector
#Read in image, need a path
maskFolder = "undistorted_pats/Py_MaskPatterns"
projFolder = "undistorted_pats/Py_ProjectorPatterns"
maskFolderUnflipped = "undistorted_pats/Py_MaskPatterns_unflipped"
cam_H = 320;
cam_W = 324;

#os.makedirs(maskFolder, exist_ok=True)
#os.makedirs(projFolder, exist_ok=True)
flip = True #True means Horizontal?

    
# Apply graycodes to compute correspondence between camera pixels and
# mask pixels.
dual_y,dual_x = np.mgrid[1:(cam_H+1),1:(cam_W+1)].astype("uint16")

coord_y, coord_x = dmdmeshgrid()



# Compute index for each dual pixel.  Index is constant along an 
# epipolar line.
dual_coord = np.concatenate((dual_x.reshape(-1,1), dual_y.reshape(-1,1), np.ones_like(dual_x).reshape(-1,1)), axis = 1);

tmp = np.matmul(dual_coord, F);
if flip:
    primal_coord = np.stack((np.zeros_like(tmp[:,1]), -tmp[:,2] / tmp[:,1], np.ones_like(tmp[:,1]))).T;
    
               
    dual_ind = primal_coord[:,1].reshape(cam_H, cam_W)
    
    # Compute index for each primal pixel.  Index is constant along an 
    # epipolar line.
    # NOTE: This can probably be simplified, so revisit code/math.
    primal_coord = np.concatenate((coord_x.reshape(-1,1), coord_y.reshape(-1,1), np.ones_like(coord_x).reshape(-1,1)), axis = 1);
    
    
    tmp = np.matmul(primal_coord, F.T)
    
    dual_coord = np.stack((np.zeros_like(tmp[:,1]), -tmp[:,2] / tmp[:,1], np.ones_like(tmp[:,1]))).T;
    
    tmp = np.matmul(dual_coord,F);
    
    primal_coord = np.stack((np.zeros_like(tmp[:,1]), -tmp[:,2] / tmp[:,1], np.ones_like(tmp[:,1]))).T;
                
    primal_ind = primal_coord[:,1].reshape(684,608);

else:
    primal_coord = np.stack((-tmp[:,2] / tmp[:,0], np.zeros_like(tmp[:,1]), np.ones_like(tmp[:,1]))).T;
    
               
    dual_ind = primal_coord[:,0].reshape(cam_H, cam_W)
    
    # Compute index for each primal pixel.  Index is constant along an 
    # epipolar line.
    # NOTE: This can probably be simplified, so revisit code/math.
    primal_coord = np.concatenate((coord_x.reshape(-1,1), coord_y.reshape(-1,1), np.ones_like(coord_x).reshape(-1,1)), axis = 1);
    
    
    tmp = np.matmul(primal_coord, F.T)
    
    dual_coord = np.stack(( -tmp[:,2] / tmp[:,0],np.zeros_like(tmp[:,1]), np.ones_like(tmp[:,1]))).T;
    
    tmp = np.matmul(dual_coord,F);
    
    primal_coord = np.stack(( -tmp[:,2] / tmp[:,0],np.zeros_like(tmp[:,1]), np.ones_like(tmp[:,1]))).T;
                
    primal_ind = primal_coord[:,0].reshape(684,608);

#Recover discrete number M of unique indices
M = 150;

min_ind = np.min((np.min(primal_ind.flatten()),np.min(dual_ind.flatten())));
max_ind = np.max((np.max(primal_ind.flatten()),np.max(dual_ind.flatten())));


primal_ind = (primal_ind - min_ind) /(max_ind - min_ind);
dual_ind   = (dual_ind   - min_ind) /(max_ind - min_ind);

primal_ind = np.round(primal_ind * (M-1) + 1);
dual_ind   = np.round(dual_ind   * (M-1) + 1);


    
iter = 0

randshift = np.random.permutation(3) + 1;

hada = scipy.linalg.hadamard(256);


paddedIm = np.zeros((cam_H,512));
for k in np.arange(1,97):
    primal_val = np.zeros_like(coord_y);
    dual_val   = np.zeros_like(dual_y);
    
    if np.mod(k,2) == 1:
        primal_val = np.ones_like(coord_y);
    
    
    if np.mod(k,6) == 0 : 
        dual_val = np.zeros_like(dual_y);
    
    
    if np.mod(k,6) == 2:
        dual_val = np.zeros_like(dual_y);
    
    
    im = Image.fromarray(255*primal_val.astype("float"))
    im = im.convert("1")
    im.save('%s/%02d_PAT.bmp' % (projFolder, k-1))

    
    paddedIm[0:cam_H, 0: cam_W] = np.rot90(dual_val, 2);
    
    cv2.imwrite('%s/dual_%03d.bmp' % (maskFolder, k-1), 255*paddedIm)


# Use twice as many columns from hadamard matrix since we can use all 96
# patterns for indirect-only
for k in np.arange(1,16):
    for c in range(3):

        val = np.max((hada[:,1], np.zeros_like(hada[:,1])), axis = 0)



        val = cv2.resize(val,(0,0), fx=6, fy=6,interpolation=cv2.INTER_NEAREST);
        val = val[:,0]
        
        
        primal_val = val;
        dual_val = 1 - val;
        
        #primal_val[::6] = 0;
        #primal_val[5::6] = 0;
        primal_val = np.roll(primal_val, 2 *randshift[c], axis = 0);
        dual_val   = np.roll(dual_val, 2 *randshift[c], axis = 0);
        
        #dual_val[::6] = 0;
        a = primal_val[(primal_ind-1).astype("int")]
        
        im = Image.fromarray(255*a)
        im = im.convert("1")
        im.save('%s/%02d_PAT.bmp' % (projFolder, iter))
       
        tempIm = dual_val[(dual_ind-1).astype("int")]
        paddedIm[0:cam_H, 6:318 ] = np.rot90(tempIm[:,4:316], 2);
        
        cv2.imwrite('%s/dual_%03d.bmp' % (maskFolder,iter), 255*paddedIm)
        
        cv2.imwrite('%s/dual_%03d.bmp' % (maskFolderUnflipped,iter), 255*tempIm)
        iter = iter + 1;
        
        
        primal_val = 1 - val;
        dual_val = val;
        
        #primal_val[::6] = 0;
        #primal_val[5::6] = 0;
        primal_val = np.roll(primal_val, 2 *randshift[c], axis = 0);
        dual_val   = np.roll(dual_val, 2 *randshift[c], axis = 0);
        
        a = primal_val[(primal_ind-1).astype("int")]
        im = Image.fromarray(255*a)
        im = im.convert("1")
        im.save('%s/%02d_PAT.bmp' % (projFolder, iter))
        
        tempIm = dual_val[(dual_ind-1).astype("int")]
        paddedIm[0:cam_H, 6:318 ] = np.rot90(tempIm[:,4:316], 2);


        cv2.imwrite('%s/dual_%03d.bmp' % (maskFolder,iter),255*paddedIm)
        cv2.imwrite('%s/dual_%03d.bmp' % (maskFolderUnflipped,iter), 255*tempIm)
        iter = iter + 1;
 

