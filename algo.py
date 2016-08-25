import cv2
import numpy as np
from matplotlib import pyplot as plt


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


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


def grad_dir(img):
    # compute x and y derivatives
    # OpenCV's Sobel operator gives better results than numpy gradient
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=-1)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=-1)

    # calculate gradient direction angles
    # phase needs 64-bit input
    angle = cv2.phase(sobelx, sobely)

    # truncates number
    gradir = np.fix(180 + angle)

    return gradir


if __name__ == '__main__':
    # second argument is a flag which specifies the way
    # an image should be read. -1 loads image unchanged with alpha channel
    depthimg = cv2.imread('img/learn17.png', -1)
    colorimg = cv2.imread('img/clearn17.png', 0)

    # Normalize depth image
    min, max, minloc, maxloc = cv2.minMaxLoc(depthimg)
    adjmap = np.zeros_like(depthimg)
    dst = cv2.convertScaleAbs(depthimg, adjmap, 255 / (max-min), -min)
    im_color = cv2.applyColorMap(dst, cv2.COLORMAP_JET)
    showimg(im_color)

    # img = cv2.imread('img\clearn5.png', -1)
    #
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

