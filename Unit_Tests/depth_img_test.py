import cv2
import numpy as np

if __name__ == '__main__':
    img = cv2.imread('learn7.png', 0)

    # bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    equ = cv2.equalizeHist(img)
    res = np.hstack((img, equ))  # stacking images side-by-side

    # create a CLAHE object (Arguments are optional).
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # cl1 = clahe.apply(img)

    # Display the image.
    cv2.imshow("window", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()