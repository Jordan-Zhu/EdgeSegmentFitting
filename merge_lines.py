# -------------------------------------------------------------------------------
# Name:        merge_lines
# Purpose:     Finds all the starting and ending points of lines,
#              then forms a connecting point to each line on the list.
# -------------------------------------------------------------------------------
#
# Usage:    merge_lines(inputline, listpt, thresh, imgsize)
#
# Arguments:
#           inputline -
#           listpt    -
#           thresh    -
#           imgsize   -
#
# Returns:
#           [newline,newlistpt,newmergedline] - Tuple of lines.
#
# See also: [None]
#
#
# July 2016 - Original version.

import numpy as np

def merge_lines(inputline, listpt, thresh, imgsize):
    # Merge lines.
    newline = inputline
    newmergedline = []
    for i in inputline.shape[0]:
        newmergedline[i] = i

    # temp = inputline[:, 9:10]
    # Index 9 and 10 are the start and end points of a line in this array.
    pts = np.unique(inputline[8:10])
    pts = np.sort(pts)

    for i in pts:
        ptx = pts[i]
        # Find indices of ptx in new line array.
        indices = [i for i, x in enumerate(newline) if x == ptx]
        pt1 = len(indices)

        # If pt1 contains more than 1 value.
        if pt1 > 1:
            

