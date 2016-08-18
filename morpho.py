import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology


def showimg(img, type='cv', write=False, imagename='img.png'):
    if type == 'plt':
        plt.figure()
        plt.imshow(img, 'gray', interpolation='nearest', aspect='auto')
        # plt.imshow(img, 'gray', interpolation='none')
        plt.title('morphology')
        plt.show()

        if write:
            plt.savefig(imagename, bbox_inches='tight')
    elif type == 'cv':
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if write:
            cv2.imwrite("../../images/%s", imagename, img)


def skel(img):
    size = np.size(img)
    skely = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    done = False

    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skely = cv2.bitwise_or(skely, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

    return skely


def clean_up(img):
    img_bw = (((img - img.min()) / (img.max() - img.min())) * 255.9)  # .astype(np.uint8)
    # 255*(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > 5).astype(np.uint8)

    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    imgmask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
    imgmask = cv2.morphologyEx(imgmask, cv2.MORPH_OPEN, se2)

    # mask = np.dstack([mask, mask, mask]) / 255
    out = img * imgmask

    return out


if __name__ == '__main__':
    img = cv2.imread('Unit_Tests/testimg1.png', 0)

    # dilate and skeletonize on combined image
    kernel = np.ones((3, 3), np.uint8)
    # dilation = cv2.dilate(img, kernel, iterations=1)
    # erosion = cv2.erode(dilation, kernel, iterations=1)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(closing, kernel, iterations=1)
    # skely = skel(dilation)
    skely = morphology.skeletonize(dilation > 0)

    showimg(skely, 'plt')

    # TO-DO: Make one all-encompassing function that does these:
    #   - Calculates gradient on depth image
    #   - Does canny on gradient and discontinuity and combines both
    #   - Gets contours from edgelink / findContours
    #   - Finds the line features from contours
    #   - Merges lines where possible
    #   - Something else happens.
