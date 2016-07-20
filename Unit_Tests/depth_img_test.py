import cv2

if __name__ == '__main__':
    im = cv2.imread('learn7.png', 0)

    # Display the image.
    cv2.imshow("window", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()