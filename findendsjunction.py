# -------------------------------------------------------------------------------
# Name:        findendsjunction
# Purpose:     Finds junctions and endings in a line/edge image.
# -------------------------------------------------------------------------------

import cv2
import numpy as np
from matplotlib import pyplot as plt
import scipy.ndimage as ndimage


def findendsjunctions(img, disp=None):
    if disp is None:
        disp = 0

    # Create a look up table to find junctions.
    # lut = ndimage.grey_erosion(junction(img), size=(3,3))
    junctions = ndimage.grey_erosion(img, size=(3, 3))
    # Row and column coordinates of junction points in the image.
    rjcj = np.where(junctions)

    ends = ndimage.grey_erosion(img, size=(3, 3))
    # Row and column coordinates of end points in the image.
    rece = np.where(ends)

    # Display image with the junctions and endings marked.
    if disp:
        plt.imshow(img)
        # Code to display image

# Function to test whether the center pixel in a 3x3 neighborhood is a junction.
# Center pixel must be set and pixels between 0 and 1 as one traverses the
# perimeter of the 3x3 region must be 6 or 8.
# Pixels in the 3x3 region are numbered as follows
#
#       1 4 7
#       2 5 8
#       3 6 9


def junction(x):
    a = [x[1], x[2], x[3], x[6], x[9], x[8], x[7], x[4]]
    b = [x[2], x[3], x[6], x[9], x[8], x[7], x[4], x[1]]
    crossings = sum(abs(np.subtract(a, b)))

    b = x[5] and crossings >= 6  # does this return the greater of two values
    return b

# Function to test whether the center pixel within a 3x3 neighborhood is an ending.
# Center pixel must be set and number of transitions or crossings between 0 and 1
# as one traverses the perimeter of the 3x3 region must be 2.
# Pixels in the 3x3 region are numbered as follows:
#
#       1 4 7
#       2 5 8
#       3 6 9


def ending(x):
    a = [x[1], x[2], x[3], x[6], x[9], x[8], x[7], x[4]]
    b = [x[2], x[3], x[6], x[9], x[8], x[7], x[4], x[1]]
    crossings = sum(abs(np.subtract(a, b)))

    b = x[5] and crossings == 2
    return b
