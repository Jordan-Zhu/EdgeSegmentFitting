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
# See also: Lseg_to_Lfeat_v2
#           LabelLineCurveFeature_v2
#
#
# July 2016 - Original version.


import math
import numpy as np


def merge_lines(inputline, listpt, thresh, imgsize):
    # Merge lines.
    line_new = inputline
    newmergedline = []
    for i in inputline.shape[0]:
        newmergedline[i] = i

    # temp = inputline[:, 9:10]
    # Index 9 and 10 are the start and end points of a line in this array.
    unique_pts = np.unique(inputline[8:10])
    unique_pts = np.sort(unique_pts)

    for i in unique_pts:
        ptx = unique_pts[i]
        # Find line segments with the same point.
        line_indices = [i for i, x in enumerate(line_new) if x == ptx]
        # Number of lines with the same point.
        coincident_pts = len(line_indices)

        # If there is more than one such line segment,
        # then we can determine which lines are able to be merged.
        if coincident_pts > 1:
            line_indices.sort()

            # Find possible combinations of these lines.
            temp = []
            combinations = []
            for i in xrange(0, len(line_indices) - 1):
                pt1 = line_indices[i]
                for j in xrange(i + 1, len(line_indices)):
                    pt2 = line_indices[j]
                    temp.append([pt1, pt2])
                    combinations.append(temp)

            k = 0
            while k < len(combinations):
                # See if the angles are different.
                angle1 = line_new[combinations[k][0]][6]
                angle2 = line_new[combinations[k][1]][6]
                delta_slope = abs(angle1 - angle2)

                if delta_slope < thresh:
                    line1 = [line_new[combinations[k][0]][8], line_new[combinations[k][0]][9]]
                    line2 = [line_new[combinations[k][1]][8], line_new[combinations[k][1]][9]]

                    # If there exists more than one place the lines intersect,
                    # it means they are not exactly the same.
                    if len(set(line1).intersection(line2)) < 2:
                        # Use set difference to get the start and end points of new line.
                        ptx = set(ptx)
                        setdiff = [x for x in [line1, line2] if x not in ptx]
                        setdiff = np.unique(setdiff)

                        line1 = line_new[combinations[k][0]][:]
                        line2 = line_new[combinations[k][0]][:]
                        ind1 = setdiff[0]
                        ind2 = setdiff[1]
                        [y1, x1] = np.unravel_index(imgsize, ind1)
                        [y2, x2] = np.unravel_index(imgsize, ind2)

                        # Slope of the new line.
                        m = (y2 - y1) / (x2 - x1)
                        # Length of the new line.
                        newlen = np.sqrt(np.power((x2 - x1), 2) + np.power((y2 - y1), 2))
                        # Angle of the new line.
                        newang = math.atan2(-m)
                        newang = math.degrees(newang)

                        # New angle's intersection point lies between the two lines
                        if newang >= min(angle1, angle2) and max(angle1, angle2) >= newang:
                            # Remove from the line feature list those lines we merged.
                            del line_new[max(combinations[k][0], combinations[k][0])]
                            del line_new[min(combinations[k][0], combinations[k][0])]


                        else:
                            k += 1
                            continue



                    else:
                        k += 1
                        continue

                else:
                    k += 1
                    continue



