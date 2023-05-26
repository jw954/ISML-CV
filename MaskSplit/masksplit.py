import cv2
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import keyboard

# Disable Pillow max pixel size
Image.MAX_IMAGE_PIXELS = None

def mask_split(image_path : str, num_segments: int):
    """
    Takes in a filepath to a mask file comprised of rows and splits the rows
    into segments, specified by num segments
    
    Parameters:
    - image_path: string path to the .bmp mask file (only comprised of rows)
    - num_segments: integer number indicating the number of segments to split
                    each row into
    
    Output:
    A saved version of the .bmp file, split up
    """
        # Load the image
    img = cv2.imread(image_path)
    
    # Reshape the image into 3D (number of frames, height, width)
    frame_height = 320
    num_frames = img.shape[0] // frame_height
    segment_size = 320 // num_segments
    img = img.reshape(num_frames, frame_height, -1)

    # Initialize an empty list to hold the result
    result = []

    for i, frame in enumerate(img):
        # Find the rows with non-black lines
        non_black_line_indices = np.where(frame.max(axis=1) > 0)[0]
        
        if len(non_black_line_indices) == 0:
            print(f"No non-black line found in frame {i}.")
            continue

        # Create new frames for each segment
        new_frames = [np.zeros((frame_height, img.shape[2]), dtype=img.dtype) for _ in range(num_segments)]
            
        # Iterate over non-black rows
        for white_line_row in non_black_line_indices:
            # Split the non-black line into segments
            non_black_line = frame[white_line_row]
            segments = np.array_split(non_black_line, num_segments)
            
            # Set all other pixels to black and apply the segments
            for j, segment in enumerate(segments):
                start_col = j * segment_size  # calculate the starting column for the segment
                new_frames[j][white_line_row, start_col:start_col+segment_size] = segment[:segment_size]  # place the segment at the correct position

        result.extend(new_frames)

        # # For debugging purposes, plot the first two original and split frames
        # if i < 2:
        #     plt.figure(figsize=(10, 5))
            
        #     plt.subplot(121)
        #     plt.imshow(frame, cmap='gray')
        #     plt.title(f'Original Frame {i}')
            
        #     for j in range(num_segments):
        #         plt.subplot(122)
        #         plt.imshow(result[i*num_segments+j], cmap='gray')
        #         plt.title(f'Split Frame {i*num_segments+j}')
            
        #     plt.show()

    # Save the result (WRONG OPENCV ONLY OPERATES IN 8 BIT)
    # save_path = os.path.splitext(image_path)[0] + '_split.bmp'
    # result = np.array(result).reshape(-1, img.shape[2])
    # result = cv2.flip(result, 0)
    # cv2.imwrite(save_path, result)     
    
    
    # Save the result
    save_path = os.path.splitext(image_path)[0] + '_split.bmp'
    result = np.array(result).reshape(-1, img.shape[2])
    # result = cv2.flip(result, 0)

    # Convert the result to a PIL image and save as a 1-bit image
    result_pil = Image.fromarray(result)
    result_pil = result_pil.convert('1')
    result_pil.save(save_path)
    
    
    
    
def conden_mask(mask):
    pic = Image.open(mask)
    print(pic.size)
    pix = np.array(pic)

    pix = pix.reshape(-1,320,512)
    dim = np.shape(pix)
    print(dim)

    upload_rows = np.empty((1,dim[2]),dtype=bool) ##New mask

    num_row = 0
    num_row_list = np.zeros(dim[0], dtype=int) ## New number of rows


    for i in range(dim[0]-1, -1 ,-1):
        for j in range(dim[1]-1, -1, -1):
            if(i>0):
                if(not((pix[i-1,j] == pix[i,j]).all())): ## if row changes, upload
                    upload_rows = np.append(upload_rows, [pix[i,j]],axis=0)
                    rowadd = bin(319-j).split('b')[1].zfill(9)
                    rowadd = list(map(int, rowadd))
                    upload_rows[-1,320:329] = rowadd ## add row with address
                    num_row += 1
            else:  ## last subframe, upload all rows
                upload_rows = np.append(upload_rows, [pix[i,j]],axis=0)
                rowadd = bin(319-j).split('b')[1].zfill(9)
                rowadd = list(map(int, rowadd))
                upload_rows[-1,320:329] = rowadd
                num_row += 1
        while(num_row < 2): ## Ensure at least 2 rows per subframe for verilog constraint
            num_row = num_row + 1
            upload_rows = np.append(upload_rows, [pix[i,-1]],axis=0)
            rowadd = bin(0).split('b')[1].zfill(9)
            rowadd = list(map(int, rowadd))
            upload_rows[-1,320:329] = rowadd
        num_row_list[-1-i] = (num_row)
        num_row = 0

    if(sum(num_row_list) % 16 != 0): ## Mask size requires rows to be multiple of 16
        num_row = 16 - (sum(num_row_list) % 16)
        num_row_list[0] = num_row_list[0] + num_row
        upload_rows = np.insert(upload_rows, 1, [[True]*dim[2]]*(num_row), axis=0)
        num_row = 0


    upload_rows = upload_rows[1:]
    upload_rows = upload_rows[::-1,:]

    print(upload_rows)

    maskfilename = 'merge.bmp'
    img = Image.fromarray(upload_rows)
    img = img.convert('1')
    img.save(maskfilename)

    return maskfilename, num_row_list



def frame_viewer():
    image = cv2.imread("wm4_40_ol.bmp")
    num_frames = image.shape[0] // 320
    frame_number = 50
    while True:
        print(frame_number)
        if frame_number < 0:
            frame_number = 0
        if frame_number > num_frames - 1:
            frame_number = num_frames - 1

        cropped_image = image[frame_number * 320 : (frame_number + 1) * 320, 0:512]
        cv2.imshow("frame", cropped_image) 
        
        key = cv2.waitKey(33)
        
        if key == ord('n'): 
            frame_number += 1
        if key == ord('p'):
            frame_number -= 1
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

   





if __name__ == "__main__":
    mask_split("./t6_RS_repeat_1.bmp", 8)
    conden_mask("t6_RS_repeat_1_split.bmp")

    # image = cv2.imread("t6_cats_256.bmp")
    # cropped_image = image[4800:5120, 0:512]
    # cropped_image = image[15360:15680, 0:512]
    # print(cropped_image[0][0])
    
    # cv2.imshow("frame", cropped_image)
    # cv2.imwrite("crop.bmp", cropped_image)
    
    # frame_viewer()

    print("All Done!")

