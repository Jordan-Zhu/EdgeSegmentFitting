# -------------------------------------------------------------------------------
# Name:        edgelink
# Purpose:     Link edge points in an image into lists.
# -------------------------------------------------------------------------------

import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import scipy.ndimage as ndimaged
from findendsjunction import findendsjunctions


def edgelink(im, minlength, location):
    # Set up some global variables to avoid copying of arguments.
    global EDGEIM
    global ROWS
    global COLS
    global JUNCT

    # minlength defaults to 1 if omitted.
    if not sys.argv[1]:
        minlength = 1

