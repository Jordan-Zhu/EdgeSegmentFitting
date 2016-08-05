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
#           [line_new, listpt_new, line_merged_n] - Tuple of lines.
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
    listpt_new = listpt
    line_new = inputline
    line_merged_n = []
    # for i in inputline.shape[0]:
    #     line_merged_n[i] = i

    # temp = inputline[:, 9:10]
    # Index 9 and 10 are the start and end points of a line in this array.
    unique_pts = np.unique(inputline[:, 8:10])

    # unique_pts = np.reshape(unique_pts, (unique_pts.shape[0] * unique_pts.shape[1], 1))
    unique_pts = np.sort(unique_pts)

    # unique pts shape = (18, )
    # TO-DO: loop through the shape part of array
    for i, items in enumerate(unique_pts):
        ptx = unique_pts[i]
        # print 'ptx = ', unique_pts[0]

        # Find line segments with the same point.
        # line_indices = [i for i, x in enumerate(line_new) if x == ptx]
        # line_indices = []

        line_indices = np.where(line_new == ptx)[0]

        # Number of lines with the same point.
        coincident_pts = line_indices.size
        print 'coincident points = ', coincident_pts

        # If there is more than one such line segment,
        # then we can determine which lines are able to be merged.
        if coincident_pts > 1:
            line_indices.sort()
            print 'line indices ', line_indices

            # Find possible combinations of these lines.
            # temp = []
            combinations = []
            for i in xrange(0, len(line_indices) - 1):
                pt1 = line_indices[i]
                for j in xrange(i + 1, len(line_indices)):
                    pt2 = line_indices[j]
                    # temp.append([pt1, pt2])
                    combinations.append([pt1, pt2])
            print 'combinations ', combinations

            k = 0
            while k < len(combinations):
                combo1 = combinations[k][0]
                combo2 = combinations[k][1]
                # See if the angles are different.
                angle1 = line_new[combo1][6]
                angle2 = line_new[combo2][6]
                print 'angles ', angle1, ' ', angle2
                delta_slope = abs(angle1 - angle2)

                print 'delta slope ', delta_slope

                if delta_slope < thresh:
                    line1 = [line_new[combo1][8], line_new[combo1][9]]
                    line2 = [line_new[combo2][8], line_new[combo2][9]]
                    print 'line1 and line2 ', line1, line2

                    # If there exists more than one place the lines intersect,
                    # it means they are not exactly the same.
                    if len(set(line1).intersection(line2)) < 2:
                        # Use set difference to get the start and end points of new line.
                        # Make ptx a set.
                        # ptx = {ptx}
                        setdiff = [x for x in line1 + line2 if x not in {ptx}]
                        setdiff = np.unique(setdiff)
                        print 'setdiff ', setdiff

                        line1 = line_new[combo1][:]
                        line2 = line_new[combo2][:]
                        ind1 = [int(setdiff[0])]
                        ind2 = [int(setdiff[1])]
                        print 'ind1 and ind2 ', ind1, ind2
                        [y1, x1] = np.unravel_index(ind1, imgsize)
                        [y2, x2] = np.unravel_index(ind2, imgsize)

                        # Slope of the new line.
                        slope = (y2 - y1) / (x2 - x1)
                        # Length of the new line.
                        newlen = np.sqrt(np.power((x2 - x1), 2) + np.power((y2 - y1), 2))
                        # Angle of the new line.
                        newang = math.atan(-slope)
                        newang = math.degrees(newang)

                        # New angle's intersection point lies between the two lines
                        if newang >= min(angle1, angle2) and max(angle1, angle2) >= newang:
                            # Remove from the line feature list those lines we merged.
                            # This leaves an empty list at the index location.
                            # del line_new, line_new[max(combo1, combo2)][:]
                            print 'max ', max(combo1, combo2), ' min ', min(combo1, combo2)
                            line_new[max(combo1, combo2)][:] = 0
                            line_new[min(combo1, combo2)][:] = 0
                            # line_new = np.delete(line_new, line_new[max(combo1, combo2)], 0)
                            # line_new = np.delete(line_new, line_new[min(combo1, combo2)], 0)


                            # idx1 = line_merged_n[combo1]
                            # idx2 = line_merged_n[combo2]

                            # Start point/end
                            del line_merged_n[max(combo1, combo2)]
                            del line_merged_n[min(combo1, combo2)]

                            count = 0
                            # Extend to include which lines were merged.
                            line_merged_n[count].extend([combo1, combo2])
                            count += 1

                            # Merge the listpoints.
                            lppair1 = listpt_new[combo1]
                            lppair2 = listpt_new[combo2]
                            # Find line segments with the same point.
                            # (These are f1, f2, f3, and f4 in matlab code)
                            startpt1 = [i for i, x in enumerate(lppair1) if x == ind1]
                            startpt2 = [i for i, x in enumerate(lppair1) if x == ind2]

                            startpt3 = [i for i, x in enumerate(lppair2) if x == ind1]
                            startpt4 = [i for i, x in enumerate(lppair2) if x == ind2]

                            # We find which line contains the starting and ending points.
                            if not startpt1:
                                line_start = lppair2
                                line_end = lppair1

                                if startpt3 > 1:
                                    line_start = list(reversed(line_start))
                                if startpt2 == 1:
                                    line_end = list(reversed(line_end))
                            else:
                                line_start = lppair1
                                line_end = lppair2

                                if startpt1 > 1:
                                    line_start = list(reversed(line_start))
                                if startpt4 == 1:
                                    line_end = list(reversed(line_end))

                            del listpt_new[max(combo1, combo2)]
                            del listpt_new[min(combo1, combo2)]
                            listpt_new[count] = [line_start[0: len(line_start) - 1], line_end]

                            # In case the condition is true,
                            # it doesn't check for the other pairs.
                            k += 1
                        else:
                            k += 1
                            continue


                    else:
                        # Count for the next pair
                        k += 1
                        continue

                else:
                    k += 1
                    continue

    # m = len(line_new)
    # Find how to get specific column in sublists.
    line_new = np.asarray(line_new)
    # Labels the line with an index number so we can refer back to it later.
    print 'line_new shape = ', line_new.shape, 'listpt_new shape ', listpt_new.shape
    line_new[:,7] = [index for index, item in enumerate(line_new)]
    return line_new, listpt_new, line_merged_n
