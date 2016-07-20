# MAXLINEDEV - Finds max deviation from a line in an edge contour.
#
# Function finds the point of maximum deviation from a line joining the
# endpoints of an edge contour.
#
# Usage: maxlinedev(x, y)
#
#
# Arguments:
#          x, y   - lists of x,y  (row, col) indicies of connected pixels
#                   on the contour.
# Returns:
#          maxdev = Maximum deviation of contour point from the line
#                     joining the end points of the contour (pixels).
#


# Issues: blank.


import math
import numpy as np


def maxlinedev(x, y):
    # Number of points is the size of the input array.
    num_pts = len(x)

    # Check whether array has enough points to form a contour.
    if num_pts == 1:
        # print "error: contour of length 1."
        maxdev = 0
        index_max = 1
        dist_contour = 1
        return (maxdev, index_max)
    elif num_pts == 0:
        print "error: contour of length 0."
        return

    # Bounds of the array.
    num_pts -= 1

    # Find the endpoint distance using the distance formula.
    endpt_dist = math.sqrt(np.power(x[0] - x[num_pts], 2) + np.power(y[0] - y[num_pts], 2))

    # If there's a meaningful distance we can proceed.
    eps = np.finfo(float).eps
    if endpt_dist > eps:
        # Eqn of line joining end pts (x1 y1) and (x2 y2) can be parameterised by
        #
        #    x*(y1-y2) + y*(x2-x1) + y2*x1 - y1*x2 = 0
        #
        # (See Jain, Rangachar and Schunck, "Machine Vision", McGraw-Hill
        # 1996. pp 194-196)

        # Compute the parameters.
        y1my2 = y[0] - y[num_pts]
        x2mx1 = x[num_pts] - x[0]
        contour = y[num_pts] * x[0] - y[0] * x[num_pts]

        dist_contour = abs(x * y1my2 + y * x2mx1 + contour) / endpt_dist
    else:
        # Endpoint distances are coincident (they're the same point),
        # so calculate distances from first point.
        dist_contour = np.sqrt(np.power(x - x[0], 2) + np.power(y - y[0], 2))

    # Set endpoint distance to 1 so that normalized error can be used. ???
    endpt_dist = 1

    # Find which index the maxdev occurs so that the line can be stopped there.
    index_max = np.argmax(dist_contour)
    maxdev = np.amax(dist_contour)

    # Return a tuple/list.
    # Unpack it by doing: maxdev, index = foo()
    return (maxdev, index_max)
