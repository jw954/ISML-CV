import os
import glob

def get_next_image_index(directory='.', prefix='saved_image', suffix='.png', log_file='log.txt'):
    """
    This function retrieves the next image index based on the log file.
    If the log file doesn't exist or is empty, it finds the highest index from existing images.
    """
    if os.path.isfile(log_file):
        with open(log_file, 'r') as f:
            last_index = f.readline().strip()  # read the first line
        if last_index:
            # if the log file is not empty, return the next index
            return int(last_index) + 1

    # if the log file is empty or doesn't exist, find the highest index from existing images
    images = glob.glob(f"{directory}/{prefix}*{suffix}")
    if images:
        # extract the indices from the filenames and find the maximum
        indices = [int(img[len(directory)+len(prefix)+1:-len(suffix)]) for img in images]
        return max(indices) + 1
    else:
        # if no images exist, start from 0
        return 0

def save_image_index(index, log_file='log.txt'):
    """
    This function saves the current image index to the log file.
    """
    with open(log_file, 'w') as f:
        f.write(f"{index:02}")


def clear_log_file(log_file='log.txt'):
    """
    This function clears the log file.
    """
    # open the log file in write mode, which will clear the file
    with open(log_file, 'w') as f:
        pass  # do nothing