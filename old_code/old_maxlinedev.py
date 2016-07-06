# -------------------------------------------------------------------------------
# Name:         maxlinedev
# Purpose:      Finds maximum deviation of a point from a line
#               joining the endpoints of an edge contour.
# -------------------------------------------------------------------------------
#
# Usage:    (maxdev, index) = maxlinedev(x, y)
#
# Arguments:
#           x, y    - arrays of x, y (row, col) that are indicies of connected pixels
#                     on the contour.
#
# Returns:
#           maxdev  - Maximum deviation of contour point from the line joining the
#                     joining the end point pixels of the contour.
#           index   - Index of the point having maximum deviation.
#
# See also: LINESEG
#
# Author: Jordan Zhu
#
# May 2016 - Original version.


import numpy as np
import sys
import math

def maxlinedev(x, y):

    num_pts = len(x) - 1

    # Base cases.
    if num_pts == 0 or num_pts == 1:
        print 'Warning: input has too few points to form a contour.'
        maxdev = 0
        index = 0
        endpt_dist = 0
        # Letting us know that there's an error in the input.
        return -1
    # end-base case

    # Find distance between endpoints using distance formula.
    # (Dist. formula: sqrt((x1 - x0)^2 + (y1 - y0)^2)
    endpt_dist = math.sqrt((x[0] - x[num_pts])**2 + (y[1] - y[num_pts])**2)

    # Continue if the distance is of significance.
    # Otherwise, the contour and line are identical.
    if endpt_dist > sys.float_info.epsilon:
        # Do some math stuff.
        # Equation of line joining end points (x1, y1) and (x2, y2)
        # can be parameterized by:
        #
        #    x * (y1 - y2) + y * (x2 - x1) + y2 * x1 - y1 * x2 = 0
        #
        # (See Jain, Rangachar and Schunck, "Machine Vision", McGraw - Hill
        # 1996. pp 194 - 196)

        y1my2 = y[0] - y[num_pts]
        x2mx1 = x[num_pts] - x[0]
        contour = y[num_pts] * x[0] - y[1] * x[num_pts]

        # Calculate distance from this line segment to each point on the contour.
        dist_contour = abs(x * y1my2 + y * x2mx1 + contour) / endpt_dist
    # end-if

    # Endpoints are coincident, so simply calculate distance
    # from the first point.
    else:
        dist_contour = math.sqrt((x - x[0])**2 + (y - y[0])**2)
    # end-else

    # Reset so that error checking can be used.
    endpt_dist = 1

    # Return index where max deviation occurs in the contour.
    # argmax returns the index of the first occurence of max.
    # amax returns the maximum of the array.
    index_max = np.argmax(dist_contour)
    maxdev = np.amax(dist_contour)

    # Return index and max dev as a list of tuples.
    # Unpack with: maxdev, index = foo()
    return (maxdev, index_max)
# end-maxlinedev


