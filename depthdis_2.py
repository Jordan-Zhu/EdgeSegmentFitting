import cv2
import numpy as np
import scipy.io as sio

#
data = sio.loadmat('Id.mat')        # load depth image from .mat file
Id = data['Id']

# Id = cv2.imread('learn0.png',-1)   #  load the png depth file

###   compress the depth image range to make edge detector work
Id2 = Id/float(Id.max())*255
Id2 = Id2.astype(np.uint8)
cv2.imshow('o',Id2)
cv2.waitKey(0)
cv2.destroyAllWindows()
###

# ### use the  'astype(np.uint8)'  to make canny edge detector work
# Id2 = Id.astype(np.uint8)
# cv2.imshow('o',Id2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# ###

edge = cv2.Canny(Id2, 30, 30)
cv2.imshow('e', edge)
cv2.waitKey(0)
cv2.destroyAllWindows()


#
# img2 = img.astype(np.int8)
#
# cv2.imshow("window", depth)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# depth = cv2.Canny(img,80,80)