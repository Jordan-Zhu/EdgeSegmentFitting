
import numpy as np
import scipy.io as sio
import math

# from merge_lines import merge_lines
from merge_lines_v3 import merge_lines
from sioloadmat import loadmat

if __name__ == '__main__':
    line_in = loadmat('linefeature.mat')
    listpt = loadmat('listpointc.mat')
    # print 'Line feature shape', line_in.shape, 'list point shape ', listpt.shape
    # print 'List point: ', listpt

    # Possible fix for out of bounds error: instead of deleting lines, fill them with an
    # empty array as a placeholder.
    # merge_lines(line_in, listpt, thresh=10, imgsize=[640, 480])
    #
    [line_new, listpoint_new, line_merged] = merge_lines(line_in, listpt, thresh=10, imgsize=[424, 512])

    # inputline = line_in
    # thresh = 10
    # imgsize = [424, 512]
    #
    #
    #
    # ##### 1    reshape the listpoint
    #
    # listpoint_2 = []
    # for i in listpt:
    #     temp0 = []
    #     for j in i[0]:
    #         temp0 += [int(j[0])]
    #     listpoint_2.append(temp0)
    #
    #
    # # def merge_lines(inputline, listpt, thresh, imgsize):
    #     # Create containers for the new values.
    # listpoint_new = listpoint_2
    # line_new = inputline
    #
    #
    #
    #
    #
    # # Fill the cell array with initial line numbers.
    # line_merged = []
    # for n in xrange(0, inputline.shape[0]):
    #     line_merged.append([n])
    #
    # # Get unique start and end points.
    # unipts = np.unique(inputline[:, 8:10])
    # unique_pts = np.sort(unipts)
    #
    # print 'working'
    # # Find occurrences of specific point in line list.
    # for i, items in enumerate(unique_pts):
    # # for i in range(5):
    # #     print 'i', i
    #     ptx = unique_pts[i]
    #     # print ptx
    #     # Number of lines with the same point.
    #     line_indices = np.where(line_new == ptx)[0]
    #     coincident_pts = line_indices.size
    #
    #     # If there's more than one line with this point,
    #     # we need to test each combination to see which lines we can possibly merge.
    #     if coincident_pts > 1:
    #         line_indices.sort()
    #         # print 'coincident', coincident_pts
    #         # Find possible permutations of these lines.
    #         permutations = []
    #         for i in xrange(0, len(line_indices) - 1):
    #             pt1 = line_indices[i]
    #             for j in xrange(i + 1, len(line_indices)):
    #                 pt2 = line_indices[j]
    #                 permutations.append([pt1, pt2])
    #
    #         count = 0
    #         while count < len(permutations):
    #             # print 'count', count
    #
    #             # Initializing variables to use later.
    #             startpt = permutations[count][0]
    #             endpt = permutations[count][1]
    #             line1 = line_new[startpt]
    #             line1ptx = [line1[8], line1[9]]
    #             angle1 = line1[6]
    #             line2 = line_new[endpt]
    #             line2ptx = [line2[8], line2[9]]
    #             angle2 = line2[6]
    #
    #             # Using the slope, we can find lines that are close enough to merge.
    #             delta_slope = abs(angle1 - angle2)
    #             # print 'delta_slope < thresh', (delta_slope < thresh)
    #             if delta_slope < thresh:
    #                 # print delta_slope
    #                 # The two lines are different.
    #                 # print 'len(set(line1ptx).intersection(line2ptx)) < 2', (len(set(line1ptx).intersection(line2ptx)) < 2)
    #                 if len(set(line1ptx).intersection(line2ptx)) < 2:
    #                     # Get a new line with the common points between them removed.
    #                     sdiff = [x for x in line1ptx + line2ptx if x not in {ptx}]
    #                     setdiff = np.unique(sdiff)
    #
    #                     # Get coordinate pairs from the individual pixels.
    #                     ind1 = int(setdiff[0])
    #                     ind2 = int(setdiff[1])
    #                     [y1, x1] = np.unravel_index([ind1], imgsize, order='F')
    #                     y11 = y1[0] - 1
    #                     x11 = x1[0]
    #                     # y1[0] -= 1
    #                     [y2, x2] = np.unravel_index([ind2], imgsize, order='F')
    #                     y22 = y2[0] - 1
    #                     x22 = x2[0]
    #                     # y2[0] -= 1
    #
    #                     # Using coordinates of the new line, calculate its slope, length, and angle.
    #                     slope = (y22 - y11) / float((x22 - x11))  ## add the 'float' so the slope will be 'inf' if the delta_x is 0
    #                     newlen = np.sqrt(np.power((x2 - x1), 2) + np.power((y2 - y1), 2))
    #                     nang = math.atan(-slope)
    #                     newang = math.degrees(nang)
    #
    #                     # The new line should have an angle between min and max angles of the merged lines.
    #                     # print 'min(angle1, angle2) <= newang <= max(angle1, angle2)', (\
    #                     # min(angle1, angle2) <= newang <= max(angle1, angle2))
    #                     if min(angle1, angle2) <= newang <= max(angle1, angle2):
    #                         # Delete the now merged lines from any lists containing it.
    #                         line_new = np.delete(line_new, [max(startpt,endpt), min(startpt,endpt)], axis=0)
    #                         # print len(line_merged)
    #                         val1 = line_merged[startpt]
    #                         val2 = line_merged[endpt]
    #                         del line_merged[max(startpt,endpt)]
    #                         del line_merged[min(startpt,endpt)]
    #
    #                         # Update both lists to reflect the addition of the merged line.
    #                         line_new = np.append(line_new, [[y11, x11, y22, x22, newlen[0], slope, newang, 0, ind1, ind2]], axis=0)
    #                         # print
    #                         line_merged.append([val1, val2])  # [line_new.shape[0] - 1]
    #
    #                         # Merge the list points. This is probably the same as line merged, this time
    #                         # with the individual pixels.
    #                         lppair1 = np.asarray(listpoint_new[startpt])
    #                         # lppair1 = np.asarray([int(i) for i in lppair1[0]])
    #                         lppair2 = np.asarray(listpoint_new[endpt])
    #                         # lppair2 = np.asarray([int(i) for i in lppair2[0]])
    #
    #                         startpt1 = list(np.where(lppair1 == ind1)[0])     ## reshape and make startpt1 as a list, for check it's empty or not
    #                         startpt2 = list(np.where(lppair1 == ind2)[0])
    #                         startpt3 = list(np.where(lppair2 == ind1)[0])
    #                         startpt4 = list(np.where(lppair2 == ind2)[0])
    #                         # print 'not startpt1', (not startpt1)
    #                         if len(startpt1)==0 :                              #####  change the way to check startpt1 is empty
    #                             line_start = list(lppair2)
    #                             line_end = list(lppair1)
    #
    #                             if startpt3[0] > 0:
    #                                 line_start = list(reversed(line_start))
    #                             if startpt2[0] == 0:
    #                                 line_end = list(reversed(line_end))
    #                         else:
    #                             line_start = list(lppair1)
    #                             line_end = list(lppair2)
    #
    #                             if startpt1[0] > 0:
    #                                 line_start = list(reversed(line_start))
    #                             if startpt4[0] == 0:
    #                                 line_end = list(reversed(line_end))
    #
    #                         # listpoint_new = np.delete(listpoint_new, [startpt, endpt], axis=0)
    #                         listpoint_new.remove(listpoint_new[max(startpt, endpt)])
    #                         listpoint_new.remove(listpoint_new[min(startpt, endpt)])
    #                         # Not sure what this line in matlab does
    #
    #                         # listpoint_new = np.append(listpoint_new, [list(line_start)+list(line_end)])
    #                         # listpoint_new2 = list(listpoint_new)
    #                         # temp = np.asarray(list(line_start) + list(line_end))
    #                         temp = line_start[0:-1] + line_end
    #                         # listpoint_new2.append([temp])
    #                         listpoint_new.append(temp)
    #                         count = len(permutations)+1     ###  as the matlab code, if the condition is ture ,it doesn't check for other pairs
    #                                                         ### otherwise, it will has the list lenth problem
    #                     else:
    #                         count += 1
    #                 else:
    #                     count += 1
    #             else:
    #                 count += 1
    # line_new[:, 7] = range(len(line_new))
    # # line_new = np.insert(line_new, 1, [i for i, items in enumerate(line_new)], axis=1)

    # print line_indices
    print line_new.shape
