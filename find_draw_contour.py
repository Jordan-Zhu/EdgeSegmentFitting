import numpy as np
import cv2
import matplotlib.pyplot as plt


im = cv2.imread('C:\Users\zding.RESEARCH\Desktop\python\learn0c.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(imgray,100,80)
#ret,thresh = cv2.threshold(imgray,127,255,0)
c, hierarchy = cv2.findContours(edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im, c, -1, (0,255,0), 1)
cv2.imshow('1',im)

###reshape date from fingdcontour
csize = len(c)
nl = []
#for i in range(csize-1):
#    if c[i].ndim!=2:
#        nl.append(i)
for i in range(csize):
    d = []
    l = len(c[i])
    for j in range(l):
        d.append((c[i][j][0][:]).tolist())
    nl.append(d)
###


###  draw contours
yy = []
xx = []
for i in range(csize):
    x = []
    y = []
    l = len(nl[i])
    for j in range(l):
        y.append(nl[i][j][0])
        x.append(nl[i][j][1])
    xx.append(x)
    yy.append(y)

#plt.plot(xx,yy)
#plt.show()
#for n in range(len(xx)):
for n in range(len(xx)):
    plt.plot(xx[n],yy[n])
    plt.hold('on') 
plt.show()

