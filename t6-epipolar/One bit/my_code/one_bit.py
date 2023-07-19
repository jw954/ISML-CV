import numpy as np
import cv2
import time


# Image file path
input_image_path = 'D:\Engineering Science\ISML\Computer Vision\Lenna.png'
output_image_path = "D:\Engineering Science\ISML\Computer Vision\Lenna_crunched.png"
output_image_path_inverted = "D:\Engineering Science\ISML\Computer Vision\Lenna_crunched_inverted.png"
 

def convert_to_byte_array(image_path : str, threshold : int, invert : bool):
    """
    Inputs:

    - image_str: path to image file

    Outputs:
    - a one dimensional byte array of the orignal image
    """

    # Load an image using OpenCV
    image = cv2.imread(image_path)
    image = cv2.resize(image, (256, 256))
    # image_inverted = np.invert(image)

    # Convert the image to grayscale
    if not invert:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else :
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = np.invert(gray_image)
    # gray_image_inverted = np.invert(gray_image)
    #    cv2.imwrite(output_image_path, gray_image)

    # Can also use mean of grayscale use it as a threshold
    # threshold = np.mean(image)

    #   # Threshold the grayscale image to createa binary image
    _, binary_image = cv2.threshold(gray_image, threshold, 1, cv2.THRESH_BINARY)
    # _, binary_image_inverted = cv2.threshold(gray_image_inverted, threshold, 1, cv2.THRESH_BINARY)

    # Pack the binary array into a unit8 byte array
    byte_array = np.packbits(binary_image.flatten(), axis = -1)
    # byte_array_inverted = np.packbits(binary_image_inverted.flatten(), axis = -1)
    
    return byte_array

    # Save to output
    # cv2.imwrite(output_image_path, binary_image)
    # cv2.imwrite(output_image_path_inverted, binary_image_inverted)
    
    # print(count_different_bits(byte_array, byte_array_inverted))

  
def count_different_bits(byte_array1, byte_array2):
    # Check if the two byte_array are the same size
    assert len(byte_array1) == len(byte_array2)
    total_different_bits = 0

    bin_1 = np.unpackbits(byte_array1, axis = -1)
    bin_2 = np.unpackbits(byte_array2, axis = -1)

    for row1, row2 in zip(bin_1, bin_2):
        xor = np.logical_xor(row1, row2)
        for elem in xor:
            if elem == True:
                total_different_bits += 1

    return total_different_bits


def byte_compare(data_in, data_out):
  for i in range(len(data_out)):
        if data_in[i] != data_out[i]:
            print(f'Error: \ncontainer: {data_in[i]} \nread out: {data_out[i]}')
            print(f'index: {i}')
            break

def save_bytearray_to_img(data_in, file_name):
  # display original image
    data_in_unpack = np.unpackbits(data_in)
    data_in_unpack = np.reshape(data_in_unpack, (256, 256))
    data_in_unpack = np.where(data_in_unpack == 1, 255, 0)
    # display image
    cv2.imwrite(file_name, data_in_unpack)
    # data_in_img = Image.fromarray(np.uint8(data_in_unpack)).convert('L')
    # data_in_img.save(file_name)

# if __name__ == "__main__":

#     # Convert the image to a byte array     
#     threshold = 128
#     byte_array = convert_to_byte_array(input_image_path, threshold)
