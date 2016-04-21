# -------------------------------------------------------------------------------
# Name:        edgelist2image
# Purpose:     Transfers edgelist data back into a 2D image array.
# -------------------------------------------------------------------------------


import cv2
import numpy as np
from matplotlib import pyplot as plt

def edgelist2image(edgelist, rowscols=None):
    if rowscols is None:
        rowscols = [1, 1]

    num_edges = max(edgelist.shape[0], edgelist.shape[1])

    # Establish bounds of image.
    minx = 1
    miny = 1
    maxx = rowscols[2]
    maxy = rowscols[1]

    for i in xrange(1, num_edges):
        minx = min(min(edgelist[i][:, 2]), minx)
        miny = min(min(edgelist[i][:, 1]), miny)
        maxx = max(max(edgelist[i][:, 2]), maxx)
        maxy = max(max(edgelist[i][: , 1]), maxy)

    # Draw the edgelist data into an image array.
    im = np.zeros(maxy, maxx)

    for i in xrange(1, num_edges):
        ind = np.ravel_multi_index([maxy, maxx], (edgelist[i][:, 1], edgelist[i][:, 2]), order='F')
        im[ind] = 1


