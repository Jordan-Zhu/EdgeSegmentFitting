import numpy as np
import cv2

from ES_Drawing.lineseg2 import lineseg2

def find_contours():
    im = cv2.imread('circle.png')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print contours
    cv2.drawContours(im, contours, -1, (0, 255, 0), 3)

    # Display the image.
    # cv2.imshow("window", im)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return contours

if __name__ == '__main__':

    edgelist = np.asarray(find_contours())
    num_edges = edgelist.shape[1]

    # seglist = []
    # print edgelist
    # print edgelist[0, 1, 0, 0]
    # print edgelist[0, 0, 0, 0]

    # x = np.empty(num_edges)
    # y = np.empty(num_edges)
    # np.copyto(x, edgelist[0, :, 0, 0])
    # np.copyto(y, edgelist[0, :, 0, 1])
    #
    # z = [1, 2, 3, 4, 5]
    # print len(z)
    # print z.index(5)
    # seglist.append([z[4], z[4]])
    # print seglist

    # seglist.append([x[0:4], y[0:4]])
    # print seglist
    # print 'x coordinates'
    # for i in xrange(0, num_edges):
    #     x[i] = edgelist[0, i, 0, 0]
    #
    # print 'y coordinates'
    # for j in xrange(0, num_edges):
    #     print edgelist[0, j, 0, 1]

    # print 'x = ', x

    # Input cell array of edgelists and tolerance.
    seglist = np.asarray(lineseg2(edgelist, tol = 2))
    print seglist.shape