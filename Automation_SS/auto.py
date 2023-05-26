import os
import time
import subprocess
import pyautogui
import pygetwindow as gw

import sys
import cv2
from t6 import *
from pathlib import Path


def take_photos(pattern_dir: str, 
                bitfile: str, 
                maskfile: str,
                subFrameNum = 161, 
                MaskNum = 161, 
                exposure = 36.05,
                repNum = 1):
    """
    Takes in a path to where the patterns are stored and automatically takes
    a single photo of each of the patters using the T6 camera

    Parameters:
    - pattern_dir: path to the directory with the calibration patterns
    - bitfile: path to the bitfile
    - maskfile: path to the maskfile
    
    Other parameters: camera settings (with default values the user can change)
    """
    # Camera settings the user can change
    l_par = {
        # Camera settings
        "subFrameNum": subFrameNum,
        "MaskNum": MaskNum,     # This mask num is the number of masks we are uploading, should equal to subFrameNum
                            # This is also the number of times the larger maskfile gets chopped up horizontally
        "exposure": exposure,
        "repNum": repNum        # Number of repetition per subframe
    }

    t6 = T6(bitfile) #Initialize T6 class
    t6.UploadMask(maskfile, l_par) #Upload the masks. 
    t6.readout_reset()
    
    pattern_path = Path(pattern_dir)
    pattern_path_list = list(pattern_path.glob("*.bmp"))

    for image_name in pattern_path_list:

        # Open the image with the default image viewer
        process = subprocess.Popen(['start', image_name], shell=True)

        # Wait for the image viewer to open
        time.sleep(2)

        ## Open and Move Window to the Right Screen
        
        # Get window
        # Note: You may need to adjust this depending on the title of the window that's opened
        window = gw.getWindowsWithTitle(image_name)[0]  # adjust the title

        window.restore()
        
        time.sleep(1)
        
        # Move to second monitor (assuming 1920x1080 resolution for primary)
        window.moveTo(4000, 0)

        # Maximize (fullscreen might not work depending on the application)
        window.maximize()

        ## MOUSE + KEYBOARD CONTROL ##
        
        # Get screen size
        screenWidth, screenHeight = pyautogui.size()

        # Move the mouse to the second monitor (assuming it's to the right of primary)
        # You may need to adjust the values depending on the actual screen layout
        pyautogui.moveTo(screenWidth + 500, screenHeight // 3)

        time.sleep(1)

        # Click to activate the window
        pyautogui.click()

        # Press 'f11' key to switch to full screen
        # This depends on the image viewer supporting 'f11' as the fullscreen hotkey
        pyautogui.press('f11')

        time.sleep(5)

        # Begin the camera operation now, the operation is goes on a continuous loop
        cv2.namedWindow("C2B") #Create a new window so the user can see image

        while True:
            # Creating the image window
            raw_img = t6.arrange_raw(t6.imread())
            img = t6.process_Img(raw_img, black=True, gain=True, max_scale = 1000)
            t6.img_show(window_name = "C2B", img = img, l_par = l_par)
            
            # Maximize on the C2B Window
            c2bwindow = gw.getWindowsWithTitle("C2B")
            c2bwindow.maximize()
            # Assume the C2B window is in the center of the screen and mouse click
            pyautogui.move(screenWidth // 2, screenHeight // 2)
            pyautogui.click()
            # Screenshot
            pyautogui.click('s')
            # Wait and then close the window
            time.sleep(2)
            pyautogui.click('esc')

sys.path.insert(0, "./api")

if __name__ == "__main__":

    # Set bit and maskfile
    bitfile     = "bitfile/Reveal_Top_t6_characterization_14.3.bit"
    maskfile    = "maskfile/t6_RS_repeat_1.bmp' #The maskfile is one large file 512 wide and height a multiple of 320."
    pattern_dir = .....

    # Auto take the photos
    take_photos(pattern_dir, bitfile, maskfile)



    