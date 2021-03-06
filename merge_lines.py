# -------------------------------------------------------------------------------
# Name:        merge_lines
# Purpose:     Finds all the starting and ending points of lines,
#              then forms a connecting point to each line on the list.
# -------------------------------------------------------------------------------
#
# Usage:    merge_lines(inputline, listpt, thresh, imgsize)
#
# Arguments:
#           inputline - 2D array of size m x 10 containing all the lines
#                       in the shape of [x1, y1, x2, y2, length, slope, angle, index, pixel1, pixel2]
#           listpt    - Cell array / array of arrays of size m x 1.
#                       Lists which lines are connected.
#           thresh    - Maximum deviation that the lines can be from standard in order for this to run.
#           imgsize   - m x n of the image.
#
# Returns:
#           [line_new, listpt_new, line_merged_n]
#
# This function merges and links together coordinate pairs to join small line fragments.
# Where line segments are found with the same start or end points,
# it is further processed to see if these multiple lines can be merged into one.
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
    listpt_new = listpt.tolist()
    line_new = inputline.tolist()
    line_merged_n = []
    # Number the merged lines
    for i in xrange(0, inputline.shape[0]):
        line_merged_n.append([i])


    # print 'line new ', line_new.dtype
    print 'line merged n ', line_merged_n[307], 'line merged shape ', len(line_merged_n)
    # temp = inputline[:, 9:10]
    # Index 9 and 10 are the start and end points of a line in this array.
    unique_pts = np.unique(inputline[:, 8:10])

    # unique_pts = np.reshape(unique_pts, (unique_pts.shape[0] * unique_pts.shape[1], 1))
    unique_pts = np.sort(unique_pts)

    # unique pts shape = (18, )
    # TO-DO: loop through the shape part of array (DONE)
    for i, items in enumerate(unique_pts):
        ptx = unique_pts[i]

        # line_indices = [i for i, x in enumerate(line_new) if x == ptx]
        # line_indices = []

        # Find line segments with the same point.
        line_indices = np.where(line_new == ptx)[0]

        # Number of lines with the same point.
        coincident_pts = line_indices.size
        print '========================== '
        print 'coincident points = ', coincident_pts

        # If there is more than one such line segment,
        # then we can determine which combination of lines are able to be merged.
        if coincident_pts > 1:
            line_indices.sort()
            print 'line indices ', line_indices

            # Find possible combinations of these lines.
            combinations = []
            for i in xrange(0, len(line_indices) - 1):
                pt1 = line_indices[i]
                for j in xrange(i + 1, len(line_indices)):
                    pt2 = line_indices[j]
                    combinations.append([pt1, pt2])
            print 'line new curr ', line_new[307]
            print 'combinations ', combinations

            # Loop through each of the line combinations.
            k = 0
            while k < len(combinations):
                print 'k = ', k, ' combo length ', len(combinations)
                combo1 = combinations[k][0]
                combo2 = combinations[k][1]

                # Calculate the change in slope.
                print 'combo ', combo1, ' combo 2 ', combo2
                print 'line new size ', len(line_new)
                print 'angles1 ',  len(line_new[combo1]), ' angle2 ', len(line_new[combo2])

                try:
                    angle1 = line_new[combo1][6]
                except IndexError:
                    angle1 = 0
                try:
                    angle2 = line_new[combo2][6]
                except IndexError:
                    angle2 = 0

                print 'angles ', angle1, ' ', angle2
                delta_slope = abs(angle1 - angle2)

                print 'delta slope ', delta_slope

                # If the change in slope is within the bounds of the threshold,
                # do this. Else, get the next combination to try.
                if delta_slope < thresh:
                    line1 = [line_new[combo1][8], line_new[combo1][9]]
                    line2 = [line_new[combo2][8], line_new[combo2][9]]
                    print 'line1 and line2 ', line1, line2

                    # If there exists more than one place the lines intersect,
                    # it means they are not exactly the same.
                    if len(set(line1).intersection(line2)) < 2:
                        # Use set difference to get the start and end points of new line.
                        setdiff = [x for x in line1 + line2 if x not in {ptx}]
                        setdiff = np.unique(setdiff)
                        print 'setdiff ', setdiff

                        # line1 = line_new[combo1][:]
                        # line2 = line_new[combo2][:]

                        ind1 = int(setdiff[0])
                        ind2 = int(setdiff[1])
                        print 'ind1 and ind2 ', ind1, ind2
                        [y1, x1] = np.unravel_index([ind1], imgsize)
                        [y2, x2] = np.unravel_index([ind2], imgsize)

                        # Slope of the new line.
                        slope = (y2 - y1) / (x2 - x1)
                        # Length of the new line.
                        newlen = np.sqrt(np.power((x2 - x1), 2) + np.power((y2 - y1), 2))
                        # Angle of the new line.
                        newang = math.atan(-slope)
                        newang = math.degrees(newang)

                        # New angle's intersection point lies between the two lines
                        if min(angle1, angle2) <= newang <= max(angle1, angle2):
                            # Remove from the line feature list those lines we merged.
                            # This leaves an empty list at the index location.
                            # del line_new, line_new[max(combo1, combo2)][:]
                            startpt = max(combo1, combo2)
                            endpt = min(combo1, combo2)
                            print 'max ', max(combo1, combo2), ' min ', min(combo1, combo2)
                            # line_new[max(combo1, combo2)][:] = 0
                            # line_new[min(combo1, combo2)][:] = 0
                            # line_new = np.delete(line_new, line_new[startpt], 0)
                            del line_new[startpt][:]
                            del line_new[endpt][:]


                            idx1 = line_merged_n[combo1]
                            idx2 = line_merged_n[combo2]

                            # Start point/end
                            # line_merged_n = np.delete(line_merged_n, line_merged_n[startpt])
                            # line_merged_n = np.delete(line_merged_n, line_merged_n[endpt])
                            line_merged_n.pop(startpt)
                            line_merged_n.pop(endpt)

                            # line_new = np.append(line_new, [x1, y1, x2, y2, newlen, slope, newang, 0, ind1, ind2])
                            # count = len(line_new)
                            count = -1
                            for i, item in enumerate(line_new):
                                # Line here
                                if line_new[i][:]:
                                    count += 1
                                # Empty list.
                                else:
                                    continue
                            print 'count ', count
                            # line_new = line_new.tolist()
                            line_new.append([x1[0], y1[0], x2[0], y2[0], newlen[0], slope[0], newang, 0, ind1, ind2])
                            print 'line new append ', line_new[count]
                            # Extend to include which lines were merged.
                            print 'line_merged_n ', len(line_merged_n)
                            line_merged_n[count].extend([combo1, combo2])
                            # count += 1

                            # Merge the listpoints.
                            lppair1 = listpt_new[combo1]
                            lppair2 = listpt_new[combo2]
                            # print 'lppair1 and lppair2 ', lppair1, lppair2

                            # Find line segments with the same point.
                            # (These are f1, f2, f3, and f4 in matlab code)
                            # startpt1 = [i for i, x in enumerate(lppair1) if x == ind1]
                            # startpt2 = [i for i, x in enumerate(lppair1) if x == ind2]
                            startpt1 = np.where(lppair1 == ind1)[0]
                            startpt2 = np.where(lppair1 == ind2)[0]

                            startpt3 = np.where(lppair2 == ind1)
                            startpt4 = np.where(lppair2 == ind2)

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

                            # del listpt_new[max(combo1, combo2)]
                            # del listpt_new[min(combo1, combo2)]
                            print 'listpt new shape ', len(listpt_new)
                            print 'start pt ', startpt, ' end pt ', endpt
                            # listpt_new = listpt_new.tolist()
                            listpt_new.pop(startpt)
                            listpt_new.pop(endpt)

                            listpt_new[count] = [line_start[0: len(line_start) - 1], line_end]
                            # listpt_new = np.asarray(listpt_new)
                            # print 'listpt_new ', listpt_new

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
                    # Count for next pair
                    k += 1
                    continue

    # m = len(line_new)
    # Find how to get specific column in sublists.
    # line_new = np.asarray(line_new)

    # Labels the line with an index number so we can refer back to it later.
    print 'line_new shape = ', len(line_new), 'listpt_new shape ', len(listpt_new)
    print 'line new 0 = ', line_new[0]
    # line_new[:, 7] = [index for index, item in enumerate(line_new)]
    for index, item in enumerate(line_new):
        # Remove the empty lists
        if not line_new[index][:]:
            line_new.pop(index)
    print 'line_new after pop ', len(line_new)
    for index, item in enumerate(line_new):
        print 'index ', index
        line_new[index][7] = index

    return line_new, listpt_new, line_merged_n
