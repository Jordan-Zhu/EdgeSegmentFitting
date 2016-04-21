# -------------------------------------------------------------------------------
# Name:        maxlinedev
# Purpose:     Find max deviation from a line in an edge contour.
# -------------------------------------------------------------------------------


import cv2
import sys
import numpy as np
import sys
import math
from matplotlib import pyplot as plt


def maxlinedev(x, y):
    pts = len(x)

    if pts == 1:
        print 'Contour of length 1'
        maxdev = 0
        index = 1
        dist = 1
        totaldev = 0
        return
    elif pts == 0:
        print 'Contour of length 0'

    # Distance between end points.
    dist = math.sqrt((x[1] - x[pts])**2 + (y[1] - y[pts])**2)

    if dist > sys.float_info.epsilon:
        y1my2 = y[1] - y[pts]
        x2mx1 = x[pts] - x[1]
        contour = y[pts] * x[1] - y[1] * x[pts]

        # Calculate the distance from line segment for each contour point.
        d = abs(x * y1my2 + y * x2mx1 + contour) / dist

    # End points are coincident, calculate distances from first point.
    else:
        # How to translate this matlab code
        d = math.sqrt((x - x[1])**2 + (y - y[1])**2)

    # Set D(dist) to 1 so that the normalized error can be used.
    dist = 1

    (maxdev, index) = find_max(d)


def find_max(l):
    max_val = max(l)
    max_idx = l.index(max_val)
    return max_val, max_idx




