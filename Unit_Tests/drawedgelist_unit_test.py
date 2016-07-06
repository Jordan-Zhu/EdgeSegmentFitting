import numpy as np
import cv2

from ES_Drawing.drawedgelist import drawedgelist
from ES_Drawing.lineseg import lineseg

if __name__ == '__main__':
    rowscols = [480, 640]
    # print rowscols[0]
    array = np.array([[50, 100], [100, 200], [10, 20], [50, 90]])
    array2 = np.array([[300, 200], [120, 250], [60, 90], [300, 200]])
    array3 = np.array([[400, 500], [500, 500], [400, 550], [500, 550]])

    side1 = np.array([[360, 346], [360, 325], [234, 278], [234, 250]])
    side2 = np.array([[357, 325], [357, 340], [438, 260], [438, 273]])
    sides = [side1, side2]
    list = np.asarray(sides)
    print array2.shape
    # list = np.append(list, array2)
    print list.shape
    # drawedgelist(array, rowscols)
    drawedgelist(list, rowscols)

    # seglist = np.asarray(lineseg2(edgelist, tol=2), np.int32)
    # seglist = seglist.reshape((-1, 1, 2))

    # draw = drawedgelist(seglist, rowscols=[480, 640])
