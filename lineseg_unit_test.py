import numpy as np
import cv2

from ES_Drawing.lineseg2 import lineseg2
from ES_Drawing.drawedgelist import drawedgelist



def find_contours(im):
    # im = cv2.imread('circle.png')
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
    img = cv2.imread('test.png')

    tes = find_contours(img)
    lent = len(tes)
    test = np.asarray(find_contours(img))
    print tes
    test = np.concatenate(test, axis=0)
    # y = len(test)
    # test = np.resize(test, (lent, y, 1, 2))
    print test.shape

    # Input cell array of edgelists and tolerance.
    seglist = np.asarray(lineseg2(test, lent, tol=10), np.int32)
    seglist = seglist.reshape((-1, 1, 2))
    print 'seglist: ', seglist
    print 'seglist shape: ', seglist.shape[0]

    draw = drawedgelist(seglist, rowscols=[480, 640])

    # edgelist = np.reshape(edgelist, (edgelist.shape[0], -1, 1, 2))
    # num_edges = edgelist.shape[1]
    # print 'edgelist shape', edgelist.shape, ' length ', num_edges
    # edgelist = np.expand_dims(edgelist, axis = 1)
    # print 'length = ', edgelist.shape[0]
    # print 'edgelist shape = ', edgelist.shape
    # edgelist = find_contours()

    # edgelist = np.asarray(find_contours(img))
    # y = np.concatenate(edgelist, axis=0)
    # y = np.expand_dims(y, axis=0)
    # edgelist = np.reshape(edgelist, (-1, 1, 2))
    # print 'shape = ', y
    # print y[:, 0, 1]
    # shape (num arrays, length of array in total, num rows = 1, num cols = 2)

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