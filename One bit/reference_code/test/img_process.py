import numpy as np
from PIL import Image


def convert_to_byte_array(image_path: str, threshold: int, invert: bool):
  """
  Inputs:

  - image_path: a string that is the path to the desired image
  - threshold: an integer value from 0 to 255 indicating at what threshold the
    bits should be turn to 0 or 1

  Outputs:
  - a byte array of the orignal image (np)
  """

  img = Image.open(image_path)
  img = img.resize((256, 256))
  grayscale_image = img.convert('L')

  gray_img_array = np.asarray(grayscale_image)

  # Uncomment to display grayscale image
  # PIL_gray = Image.fromarray(np.uint8(gray_img_array)).convert('L')
  # PIL_gray.show()

  if invert:
    inverted_array = np.invert(gray_img_array)
    filtered_image = np.where(inverted_array > threshold, 1, 0)
  else:
    filtered_image = np.where(gray_img_array > threshold, 1, 0)

  # Uncomment to display one-bit filtered image
  # one_bit = Image.fromarray(np.uint8(filtered_image)).convert('L')
  # one_bit.show()

  byte_array = np.packbits(filtered_image.flatten(), axis = -1)

  return byte_array

#! needs to be verified
def compare_byte_arrays(barray1, barray2) -> bool:
  """
  Takes in two byte arrays as input (np array) and returns how many mismatches
  there are between them
  """
  unpacked1 = np.unpackbits(barray1)
  unpacked2 = np.unpackbits(barray2)

  matches = (unpacked1 == unpacked2)
  num_mismatches = np.count_nonzero(~matches)

  return num_mismatches


def save_bytearray_to_img(data_in, file_name):
  # display original image
    data_in_unpack = np.unpackbits(data_in)
    data_in_unpack = np.reshape(data_in_unpack, (256, 256))
    data_in_unpack = np.where(data_in_unpack == 1, 255, 0)
    # display image
    data_in_img = Image.fromarray(np.uint8(data_in_unpack)).convert('L')
    data_in_img.save(file_name)


def byte_compare(data_in, data_out):
  for i in range(len(data_out)):
        if data_in[i] != data_out[i]:
            print(f'Error: \ncontainer: {data_in[i]} \nread out: {data_out[i]}')
            print(f'index: {i}')
            break
        