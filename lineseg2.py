# -------------------------------------------------------------------------------
# Name:        lineseg2
# Purpose:     Alternate version of lineseg. Forms straight line segments
#              from an edge list.
# -------------------------------------------------------------------------------
#
# Usage:    seglist = lineseg(edgelist, tol)
#
# Arguments:
#           edgelist - List of arrays of edgelists where each edgelist
#                      is an Nx2 array of (row, col) coordinates.
#           tol      - Maximum deviation from straight line before a
#                      segment is broken in two (measured in pixels).
#
# Returns:
#           seglist  - A list of arrays where each seglist is a subsampling of
#                      its corresponding edgelist such that straight line
#                      segments points do not deviate from the original points by
#                      more than tol.
#
# See also: MAXLINEDEV
#
# Author: Jordan Zhu
#
# May 2016 - Original version.

import numpy as np
from maxlinedev2 import maxlinedev

def lineseg2(edgelist, edges, tol):
    # num_contours = edgelist.shape[0]
    num_contours = edges
    # Create an empty list to store the resulting arrays of edge segments.
    seglist = []

    for i in xrange(0, num_contours):
        num_edges = len(edgelist[:, 0, 0])

        # Fill in the x and y coordinate matrices.
        x = np.empty(num_edges)
        y = np.empty(num_edges)
        np.copyto(x, edgelist[:, 0, 0])
        np.copyto(y, edgelist[:, 0, 1])

        # Beginning and endpoints in edge segment being considered.
        first = 0
        last = num_edges - 1

        # We can add the first point right away since
        # it's going to be the beginning of any created edge segment.
        seglist.append([x[first], y[first]])
        num_pts = 1

        while first < last:
            # Find the size and index of maximum deviation.
            (maxdev, index) = maxlinedev(x[first:last], y[first:last])

            while maxdev > tol:
                # Shorten the line to point of max deviation.
                last = first + index
                # Double check
                (maxdev, index) = maxlinedev(x[first:last], y[first:last])
            # end - if

            num_pts += 1
            seglist.append([x[last], y[last]])

            first = last
            last = num_edges - 1
            # print 'first = ', first, 'last = ', last
        # end-while
    # end-for
    print 'seglist length = ', len(seglist)
    return seglist
# end-lineseg


#
# Algorithm:
#   Create line segments, given an list of pixel arrays
#   and a tolerance for how close the line segment should be to the edgels.
#
#   Run it for every set of edges in the list.
#   Create an output array to store the created line segments.
#
#   For every edge, assign x = first index, y = second index
#   First = 0, start of the edge array; last = length
#
#   Count the number of points
#   Add the first point to the seg list, since this is guaranteed
#   to be in the edge segment.
#
#   Loop while there are still segments to check.
#   Check every point in this iterations edge array and find point of max deviation.
#   If this point is higher than the tolerance,
#       break the line at this point.
#       Check the remaining points.
#
#   Increment the points counter.
#   Add the current last point to the seg list.
#
#   Make the current last point the new first point
#   And make the last point the length of the edge array.
#
