import math
import numpy as np
import cv2

from ES_Drawing.maxlinedev import maxlinedev

def find_contours():
    im = cv2.imread('circle.png')
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(im, contours, -1, (0, 255, 0), 3)

    # Display the image.
    # cv2.imshow("window", im)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print contours
    return contours

if __name__ == '__main__':
    edgelist = np.asarray(find_contours())
    # print edgelist[0, :, 0, 1]
    # Input arrays of x, y indices of connected pixels.
    print maxlinedev(edgelist[0, :, 0, 0], edgelist[0, :, 0, 1])

    # Index position 131.
    print edgelist[0, 131, 0, :]

