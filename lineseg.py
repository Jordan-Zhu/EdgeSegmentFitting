# -------------------------------------------------------------------------------
# Name:        lineseg
# Purpose:     Form straight line segments from an edge list.
# -------------------------------------------------------------------------------


import cv2
import sys
import numpy as np
import scipy.io as sio
from matplotlib import pyplot as plt
from maxlinedev import maxlinedev


def lineseg(edgelist, tol):
    # Find the length of the largest array dimension.
    num_edges = max(edgelist.shape[0], edgelist.shape[1])
    # Create an array of arrays to store the line segments.
    # In numpy, this is done by creating an array of objects.
    seglist = np.empty((num_edges, 2), dtype = object)


    # Loop through all the 'cells' (arrays of arrays).
    for e in xrange(1, num_edges):
        # (row, col) corresponds to (x, y) in numpy.
        x = edgelist[e, 0]
        y = edgelist[e, 1]

        # Indices of first and last points in edge segment
        # being considered.
        first = 1
        last = len(x)

        pts = 1
        seglist[e][pts, :] = [y[first], x[first]]

        while first < last:
            # Find size and position of maximum deviation.
            (m, i) = maxlinedev(x[first:last], y[first:last])

            while m > tol:
                last = i + first - 1
                (m, i) = maxlinedev(x[first:last], y[first:last])

            pts += 1
            # seglist{e}(Npts, :) = [y(lst) x(lst)];
            # seglist is a cell, an array of arrays
            # like [] [] []
            #      [] [] []
            #      [] [] []
            seglist[e][pts, :] = [y[first], x[first]]

            # Reset first and last for the next iteration.
            first = last
            last = len(x)


    return seglist

    #end - lineseg



