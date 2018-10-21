import cv2
from matplotlib import pyplot as plt
import numpy as np


## This is my first branch to do Histogram Matching Algorithm with GUI
def HistMake( arg ,row , col , channel):
    HistArray01 = [0] * 256
    HistArray11 = [0] * 256
    HistArray21 = [0] * 256

    for x in range(0, row):
        for y in range(0, col):
            HistArray01[arg[x, y, 0]] = HistArray01[arg[x, y, 0]] + 1

    for x in range(0, row):
        for y in range(0, col):
            HistArray11[arg[x, y, 1]] = HistArray11[arg[x, y, 1]] + 1

    for x in range(0, row):
        for y in range(0, col):
            HistArray21[arg[x, y, 2]] = HistArray21[arg[x, y, 2]] + 1


    return (HistArray01,HistArray11,HistArray21)


img=cv2.imread('color1.png')
img2=cv2.imread('color2.png')
row, col, ch=img.shape
row2, col2, ch2=img.shape
redHist,greenHist,blueHist= HistMake(img,row,col,ch)
redHist2,greenHist2,blueHist2= HistMake(img2,row2,col2,ch2)

plt.subplot(4,2,1)
plt.imshow(img)
plt.subplot(4,2,2)
plt.imshow(img2)

plt.subplot(4,2,3)
plt.xlim([-15,270])
plt.plot(redHist,color='r')

plt.subplot(4,2,4)
plt.xlim([-15,270])
plt.plot(redHist2,color='r')



plt.subplot(4,2,5)
plt.xlim([-15,270])
plt.plot(greenHist,color='g')

plt.subplot(4,2,6)
plt.xlim([-15,270])
plt.plot(greenHist2,color='g')



plt.subplot(4,2,7)
plt.xlim([-15,270])
plt.plot(blueHist,color='b')

plt.subplot(4,2,8)
plt.xlim([-15,270])
plt.plot(blueHist2,color='b')

plt.show()




