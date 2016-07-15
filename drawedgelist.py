# -------------------------------------------------------------------------------
# Name:        drawedgelist
# Purpose:     Alternate version of lineseg. Forms straight line segments
#              from an edge list.
# -------------------------------------------------------------------------------
# Usage:    handles = drawedgelist(edgelist, rowscols, lw,


import numpy as np
import cv2
import colorsys
import random

def gen_color():
    # use golden ratio
    golden_ratio_conjugate = 0.618033988749895
    h = random.randint(0, 32)  # use random start value
    print h

    h += golden_ratio_conjugate
    h %= 1
    return colorsys.hsv_to_rgb(h, 0.5, 0.95)


def drawedgelist(edgelist, rowscols):
    # edges = edgelist.shape[0]
    # handles = np.zeros((edges, 1))

    blank_image = np.zeros((rowscols[0], rowscols[1], 3), np.uint8)
    # Set up the edge colors.

    # list = [[10, 20], [50, 20], [10, 50], [50, 50], [100, 200], [90, 120]]
    # list2 = np.asarray(list, np.int32)

    # Convert BGR to HSV
    # hsv = cv2.cvtColor(blank_image, cv2.COLOR_BGR2HSV)

    colors = [[0,255,255], [255,0,0], [0,255,0], [194,154,244], [201,153,203],
              [207,198,174], [119,190,119], [181,158,179], [71,179,255]]
    # len = edgelist.shape[0]
    # for i in xrange(0, len):
    #     cv2.polylines(blank_image, [edgelist[i]], False, (colors[i]))

    cv2.polylines(blank_image, [edgelist], False, (0, 255, 255))
    # cv2.drawContours(blank_image, [edgelist], -1, (0, 255, 255), 3)
    # cv2.line(blank_image, , [50, 60], color=(0, 255, 0), thickness=2)
    # print edgelist.item(1)
    # for i in xrange(3, edgelist.shape[0]):
        # cv2.line(blank_image, edgelist[i-1, 0], edgelist[i, 0], color=(0, 255, 0), thickness=2)
        # cv2.line(blank_image, (edgelist.item(i-3), edgelist.item(i-2)), (edgelist.item(i-1), edgelist.item(i)), color=(0, 255, 0), thickness=2)
    cv2.imshow("window", blank_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


