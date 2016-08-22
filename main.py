import cv2
import numpy as np

if __name__ == '__main__':
    depthimg = cv2.imread('img/learn17.png', -1)
    colorimg = cv2.imread('img/clearn17.png', 0)