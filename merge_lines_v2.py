import math
import numpy as np


def merge_lines(inputline, listpt, thresh, imgsize):
    # Create containers for the new values.
    listpoint_new = listpt
    line_new = inputline

    # Fill the cell array with initial line numbers.
    line_merged = []
    for n in xrange(0, inputline.shape[0]):
        line_merged.append([n])

    # Get unique start and end points.
    unipts = np.unique(inputline[:, 8:10])
    unique_pts = np.sort(unipts)

    print 'working'
    # Find occurrences of specific point in line list.
    for i, items in enumerate(unique_pts):
        ptx = unique_pts[i]

        # Number of lines with the same point.
        line_indices = np.where(line_new == ptx)[0]
        coincident_pts = line_indices.size

        # If there's more than one line with this point,
        # we need to test each combination to see which lines we can possibly merge.
        if coincident_pts > 1:
            line_indices.sort()

            # Find possible permutations of these lines.
            permutations = []
            for i in xrange(0, len(line_indices) - 1):
                pt1 = line_indices[i]
                for j in xrange(i + 1, len(line_indices)):
                    pt2 = line_indices[j]
                    permutations.append([pt1, pt2])

            count = 0
            while count < len(permutations):
                # Initializing variables to use later.
                startpt = permutations[count][0]
                endpt = permutations[count][1]
                line1 = line_new[startpt]
                line1ptx = [line1[8], line1[9]]
                angle1 = line1[6]
                line2 = line_new[endpt]
                line2ptx = [line2[8], line2[9]]
                angle2 = line2[6]

                # Using the slope, we can find lines that are close enough to merge.
                delta_slope = abs(angle1 - angle2)
                if delta_slope < thresh:
                    # The two lines are different.
                    if len(set(line1ptx).intersection(line2ptx)) < 2:
                        # Get a new line with the common points between them removed.
                        sdiff = [x for x in line1ptx + line2ptx if x not in {ptx}]
                        setdiff = np.unique(sdiff)

                        # Get coordinate pairs from the individual pixels.
                        ind1 = int(setdiff[0])
                        ind2 = int(setdiff[1])
                        [y1, x1] = np.unravel_index([ind1], imgsize)
                        [y2, x2] = np.unravel_index([ind2], imgsize)

                        # Using coordinates of the new line, calculate its slope, length, and angle.
                        slope = (y2 - y1) / (x2 - x1)
                        newlen = np.sqrt(np.power((x2 - x1), 2) + np.power((y2 - y1), 2))
                        nang = math.atan(-slope)
                        newang = math.degrees(nang)

                        # The new line should have an angle between min and max angles of the merged lines.
                        if min(angle1, angle2) <= newang <= max(angle1, angle2):
                            # Delete the now merged lines from any lists containing it.
                            line_new = np.delete(line_new, [startpt, endpt], axis=0)
                            val1 = line_merged[startpt]
                            val2 = line_merged[endpt]
                            del line_merged[startpt]
                            del line_merged[endpt]

                            # Update both lists to reflect the addition of the merged line.
                            line_new = np.append(line_new, [
                                [y1[0], x1[0], y2[0], x2[0], newlen[0], slope[0], newang, 0, ind1, ind2]], axis=0)
                            line_merged[line_new.shape[0] - 1].extend([val1, val2])

                            # Merge the list points. This is probably the same as line merged, this time
                            # with the individual pixels.
                            lppair1 = listpoint_new[startpt]
                            lppair2 = listpoint_new[endpt]

                            startpt1 = np.where(lppair1 == ind1)[0]
                            startpt2 = np.where(lppair1 == ind2)[0]
                            startpt3 = np.where(lppair2 == ind1)[0]
                            startpt4 = np.where(lppair2 == ind2)[0]

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

                            listpoint_new = np.delete(listpoint_new, [startpt, endpt], axis=0)
                            # Not sure what this line in matlab does
                            # ListPoint_new{c0+1} = [L_start(1:end-1) ; L_end] ;

                            count += 1
                    else:
                        count += 1
                else:
                    count += 1

    line_new = np.insert(line_new, 1, [i for i, items in enumerate(line_new)], axis=1)
    return [line_new, listpoint_new, line_merged]
