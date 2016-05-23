# MAXLINEDEV - Finds max deviation from a line in an edge contour.
#
# Function finds the point of maximum deviation from a line joining the
# endpoints of an edge contour.
#
# Usage: maxlinedev(x, y)
#
#
# Arguments:
#          x, y   - arrays of x,y  (col, row) indicies of connected pixels
#                   on the contour.
# Returns:
#          maxdev = Maximum deviation of contour point from the line
#                     joining the end points of the contour (pixels).
#

# Pseudo-code. Not tested to work.
# Issues: function takes in one value for each argument, yet MATLAB code has it so that it will be run from array index 0 to length - 1.
# num_pts is one instance, where it uses the length of x, as if for all x.


import math
import numpy as np


def maxlinedev(x, y):
    # Number of points is the size of the input array.
    num_pts = x.size()

    # Check whether array has enough points to form a contour.
    if(num_pts == 1 or num_pts == 0):
        print "error: contour length 0 or 1."
        maxdev = 0
        dist_contour = 1

    # Bounds of the array.
    num_pts -= 1

    # Distance formula for finding the endpoint distance.
    endpt_dist = math.sqrt(np.power(x[0] - x[num_pts], 2) + np.power(y[0] - y[num_pts], 2))

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
        C = y[num_pts] * x[0] - y[0] * x[num_pts]

        dist_contour = abs(x * y1my2 + y * x2mx1 + C) / endpt_dist
    else:
        # Endpoint distances are coincident, so calculate distances from first point.
        dist_contour = math.sqrt(np.power(x - x[0], 2) + np.power(y - y[0], 2))

    # Set endpoint distance to 1 so that normalized error can be used.
    endpt_dist = 1

    maxdev = dist_contour

    # Also find which index the maxdev occurs so that the line can be stopped there.
    return maxdev
