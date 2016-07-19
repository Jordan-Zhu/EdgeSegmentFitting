import cv2
import numpy as np

from lineseg import lineseg
from drawedgelist import drawedgelist


def find_contours(im):
    # im = cv2.imread('circle.png')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.RETR_EXTERNAL cv2.RETR_CCOMP
    # show contours
    print contours
    print hierarchy
    # Just consider the contours that don't have a child
    # that is hierarchy[i][2] < 0

    # print hierarchy[0][1, 2]
    print contours[0]
    newcontours = []
    for i in xrange(len(contours)):
        print hierarchy[0][i, 2]
        if hierarchy[0][i, 2] < 0:
            print hierarchy[0][i, 2]
            newcontours.append(contours[i])

    cv2.drawContours(im, newcontours, -1, (0, 255, 0), 1)
    contours = newcontours

    # Display the image.
    cv2.imshow("window", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return contours


if __name__ == '__main__':
    img = cv2.imread('test.png')

    data = np.asarray(find_contours(img))
    # print 'data shape ', data.shape[0]

    seglist = lineseg(data, tol=2)
    # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    # print seglist

    # for index, item in enumerate(seglist):
    #     print index

    drawedgelist(seglist, rowscols=[480, 640])

    # for i in seglist[0][:, 0]:
    #     x.append(seglist[0][i, 0])
    # x = seglist[1][:, 0]
    # y = seglist[1][:, 1]
    # print 'x ', x[0]
    # print 'y ', seglist[0][:, 1]


    # for n in range(x.shape[0] - 1):
    #     cv2.line(img, (x[n], y[n]), (x[n + 1], y[n + 1]), (0, 255, 255), thickness=2)
    #     plt.plot(x[n], y[n])
    #     plt.hold('on')
    # plt.show()
    # cv2.imshow("window", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # reshape array
    # temp = []
    # for i in xrange(data.shape[0]):
    #     arr = np.squeeze(data[i])
    #     temp.append(arr)

    # temp = np.asarray(temp)
    # print 'x ', temp[0][:, 0]
    # print 'y ', temp[0][:, 1]

    # rebuilt = np.concatenate((data[0], data[1]), axis=0)
    # print 'new shape ', rebuilt.shape
    # y = len(test)
    # test = np.resize(test, (lent, y, 1, 2))
    # print data

    # Input cell array of edgelists and tolerance.
    # seglist = lineseg(data, len, tol=2)
    # print seglist.dtype

    # colon indicates to go through all the elements in this dimension.
    # x = seglist[0, :, 0]
    # y = seglist[0, :, 1]
    # print 'x ', data.shape
    # print 'y ', y
    # print y.shape[0]

    # pts = np.asarray([x, y], dtype=np.int32)
    # print pts.dtype

    # cv2.polylines(img, [x, y], False, (0, 255, 255))

    # list = np.asarray(seglist[0], dtype=np.int32)
    # print list.shape

    # print seglist[0]
    # seglist = seglist.reshape((-1, 1, 2))
    # print 'seglist: ', seglist.shape[0]
    # print 'seglist shape: ', type(seglist[0])

    # draw = drawedgelist(list, rowscols=[480, 640])

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