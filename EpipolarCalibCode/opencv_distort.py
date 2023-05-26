import numpy as np
import cv2

def distortimage(image, mtx, dist, interpolation = cv2.INTER_AREA):

    height,width = image.shape[:2];
    u,v = cv2.initUndistortRectifyMap(mtx,None,None, mtx,(width,height), cv2.CV_32FC1)
    
    
    points = np.concatenate((u.reshape(-1,1), v.reshape(-1,1)), axis = 1)
    points = np.array(points).reshape(-1,1,2).astype(np.float32)
    res = cv2.undistortPoints(points, mtx, dist);
    
    
    u_dist = res[:,0,0].reshape(height,width) * mtx[0,0] + mtx[0,2];
    v_dist = res[:,0,1].reshape(height,width) * mtx[1,1] + mtx[1,2];
    
    
    image_distorted = cv2.remap(image,u_dist,v_dist, interpolation = interpolation)

    return image_distorted