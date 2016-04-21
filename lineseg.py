# -------------------------------------------------------------------------------
# Name:        lineseg
# Purpose:     Form straight line segments from an edge list.
# -------------------------------------------------------------------------------


import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
from maxlinedev import maxlinedev


def lineseg(edgelist, tol):
    num_edges = max(edgelist.shape[0], edgelist.shape[1])
    seglist = np.zeros((1, num_edges))

    for e in xrange(1, num_edges):
        y = edgelist[e][:, 1]
        x = edgelist[e][:, 2]

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
            # Stuff goes here
            #
            #
            #
            first = last
            last = len(x)



