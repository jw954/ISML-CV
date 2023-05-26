import sl
import glob
import numpy as np
import cv2
import time
folderName = 'Test'
screenID = 1;
projector = sl.Projector(screenID)
projector.display(sl.Projector.WHITESCREEN);

projector.setDelay(0.0)  # second, double, min: 0, max: 66e-3

#Cycle through a bunch of images



for x in glob.glob(folderName + "/*.bmp"):
    print (x)

    a = cv2.imread(x)

    curIm = a.astype(np.int64)
    projector.displayint(curIm)

    time.sleep(5)
#Capture images



