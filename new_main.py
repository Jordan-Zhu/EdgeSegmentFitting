# -------------------------------------------------------------------------------
# Name:        new_main
# Purpose:     Calculating image gradient direction and detecting contours
# -------------------------------------------------------------------------------

import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology
# from scipy import weave
# from skimage.color.colorlabel import label2rgb


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


def grad_dir(img):
    # compute x and y derivatives
    # OpenCV's Sobel operator gives better results than numpy gradient
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=-1)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=-1)

    # calculate gradient direction angles
    # phase needs 64-bit input
    angle = cv2.phase(sobelx, sobely)

    # truncates number
    l2 = np.fix(180 + angle)

    return l2


def edge_detect(depth, color):
    # Get the gradient direction from the depth image
    graddir = grad_dir(depth)
    # plt.imshow(graddir)
    # plt.show()

    # kernel for dilation
    kernel = np.ones((5, 5), np.uint8)

    # Threshold the image so it is in the RGB color space
    bw2 = (((graddir - graddir.min()) / (graddir.max() - graddir.min())) * 255.9).astype(np.uint8)

    # removes the salt and pepper noise
    # by replacing pixels with
    # the median value of the area
    median = cv2.medianBlur(bw2, 9)

    # find edges with the canny edge detector
    bw2 = auto_canny(median)
    dilation2 = cv2.dilate(bw2, kernel, iterations=1)
    skel2 = morphology.skeletonize(dilation2 > 0)

    # Now run canny edge detector on the colour image
    # create a CLAHE object (Arguments are optional).
    # this does adaptive histogram equalization on the image
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(color)
    # median = cv2.medianBlur(bw2,5)
    # bw1 = cv2.GaussianBlur(cl1, (3,3), 0)

    # Perform canny edge detection on colour image, twice
    # 1. Detect outlines and fill with close function
    # 2. Detect outlines of now filled contoured image
    bw1 = auto_canny(cl1)
    closing = cv2.morphologyEx(bw1, cv2.MORPH_CLOSE, kernel, iterations=6)
    # dilation1 = cv2.dilate(bw1,kernel,iterations = 1)
    # skel1 = morphology.skeletonize(dilation1 > 0)
    bw1 = auto_canny(closing)

    # combine the edges from the color image and the depth image
    orop = (np.logical_or(bw1, skel2)).astype('uint8')

    # display results
    plt.subplot(1, 2, 1), plt.imshow(graddir, cmap='jet')
    plt.title('gradient dir'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 2, 2), plt.imshow(median, cmap='gray')
    plt.title('blurred image'), plt.xticks([]), plt.yticks([])
    plt.show()

    # dilate and skeletonize on combined image
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(orop, kernel, iterations=1)
    img_out = morphology.skeletonize(dilation > 0)

    return img_out


def skel(img):
    size = np.size(img)
    skely = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
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


# def _thinningIteration(im, iter):
#     I, M = im, np.zeros(im.shape, np.uint8)
#     expr = """
#     for (int i = 1; i < NI[0]-1; i++) {
#         for (int j = 1; j < NI[1]-1; j++) {
#             int p2 = I2(i-1, j);
#             int p3 = I2(i-1, j+1);
#             int p4 = I2(i, j+1);
#             int p5 = I2(i+1, j+1);
#             int p6 = I2(i+1, j);
#             int p7 = I2(i+1, j-1);
#             int p8 = I2(i, j-1);
#             int p9 = I2(i-1, j-1);
#             int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) +
#                      (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) +
#                      (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
#                      (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
#             int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
#             int m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
#             int m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);
#             if (A == 1 && B >= 2 && B <= 6 && m1 == 0 && m2 == 0) {
#                 M2(i,j) = 1;
#             }
#         }
#     }
#     """
#
#     weave.inline(expr, ["I", "iter", "M"])
#     return I & ~M
#
#
# def thinning(src):
#     dst = src.copy() / 255
#     prev = np.zeros(src.shape[:2], np.uint8)
#     # diff = None
#
#     while True:
#         dst = _thinningIteration(dst, 0)
#         dst = _thinningIteration(dst, 1)
#         diff = np.absolute(dst - prev)
#         prev = dst.copy()
#         if np.sum(diff) == 0:
#             break
#
#     return dst * 255

# main


if __name__ == '__main__':
    # second argument is a flag which specifies the way
    # an image should be read. -1 loads image unchanged with alpha channel
    depthimg = cv2.imread('img/learn17.png', -1)
    colorimg = cv2.imread('img/clearn17.png', 0)

    ed = edge_detect(depthimg, colorimg)

    blank_image = np.zeros((depthimg.shape[0], depthimg.shape[1], 3), np.uint8)
    print blank_image.shape
    mask = np.array(ed * 255, dtype=np.uint8)
    masked = np.ma.masked_where(mask <= 0, mask)

    plt.figure()
    plt.imshow(blank_image, 'gray', interpolation='none')
    plt.imshow(masked, 'gray_r', interpolation='none', alpha=1.0)
    plt.title('canny + morphology')
    plt.savefig('foo.png', bbox_inches='tight')
    plt.show()
