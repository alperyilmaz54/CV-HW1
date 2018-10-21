import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import cv2
import numpy as np
import random
from copy import copy, deepcopy


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        menu = self.menuBar()
        file = menu.addMenu("File")

        file.addAction("Open Input")
        file.addAction("Open Target")
        file.addAction("Exit")

        file.triggered[QAction].connect(self.operations)

        self.setWindowTitle("Histogram Equalization")
        self.setGeometry(150, 100, 1100, 600)
        button = QPushButton('Histogram Equalizer', self)
        button.clicked.connect(self.equalize)
        button.move(10, 20)
        button.resize(140, 20)

        self.m = PlotCanvas(self)
        self.m.move(10, 40)
        self.m1 = PlotCanvas(self)
        self.m1.move(360, 40)
        self.m2 = PlotCanvas(self)
        self.m2.move(710, 40)

        self.show()

    def equalize(self):

        copiedInputHistogram=deepcopy(self.histOfInput)             #temp hist because main hist can be change
        copiedTargetHistogram = deepcopy(self.histOfTarget)


        plt.plot(self.histOfInput,color='g')


        copiedInputHistogram=self.convertCDF(copiedInputHistogram)
        copiedTargetHistogram = self.convertCDF(copiedTargetHistogram)
        #print(self.row)
        print(copiedInputHistogram)
        LookUpTable=self.LUT(copiedInputHistogram,copiedTargetHistogram)

        equalizedImage=np.zeros((self.row,self.col,self.ch),dtype=np.uint8)
        equalizedImage=self.generateNewImage(LookUpTable,equalizedImage)
        result=self.calc_Hist(equalizedImage)

        title='Result'
        self.m2.plot(equalizedImage, result, title)

    def generateNewImage(self,LookUpTable,equalizedImage):

        for i in range(0, self.row):
            for j in range(0, self.col):
                equalizedImage[i, j, 0] = LookUpTable[0, self.imgInput[i, j, 0]]
                equalizedImage[i, j, 1] = LookUpTable[1, self.imgInput[i, j, 1]]
                equalizedImage[i, j, 2] = LookUpTable[2, self.imgInput[i, j, 2]]
        return equalizedImage


    def LUT(self,input,target):
        tempLookUp = np.zeros((3,256))
        intensityJ=[0]*3
        for intensityI in range(0, 256):
            while target[2, intensityJ[2]] < input[2, intensityI] and intensityJ[2] < 256:
                intensityJ[2]+= 1
            while target[1, intensityJ[1]] < input[1, intensityI] and intensityJ[1] < 256:
                intensityJ[1] += 1
            while target[0, intensityJ[0]] < input[0, intensityI] and intensityJ[0] < 256:
                intensityJ[0] += 1

            tempLookUp[2, intensityI] = intensityJ[2]
            tempLookUp[0, intensityI] = intensityJ[0]
            tempLookUp[1, intensityI] = intensityJ[1]

        return tempLookUp




    def convertCDF(self,hist):

        for i in range(1, 256):
            hist[0, i] = hist[0, i]+hist[0, i - 1]
            hist[1, i] = hist[1, i]+hist[1, i - 1]
            hist[2, i] = hist[2, i]+hist[2, i - 1]

        for k in range(0, 256):
            hist[0, k] = hist[0, k] / (self.row * self.col)
            hist[1, k] = hist[1, k] / (self.row * self.col)
            hist[2, k] = hist[2, k] / (self.row * self.col)

        return hist


    def operations(self,q):
        if(q.text()=="Open Input"):
            filename = QFileDialog.getOpenFileName(self, "Image Select")
            # print(filename[0])
            self.imgInput = cv2.imread(filename[0])
            self.imgInput=cv2.cvtColor( self.imgInput,cv2.COLOR_BGR2RGB)
            self.openInputOperations(self.imgInput)
        elif(q.text()=="Open Target"):
            filename = QFileDialog.getOpenFileName(self, "Image Select")
            # print(filename[0])
            img = cv2.imread(filename[0])
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.openTargetOperations(img)
        else:
            QApplication.exit()

    def openInputOperations(self,img):
        print('a')
        title='Input'
        self.row, self.col, self.ch = img.shape
        self.histOfInput=self.calc_Hist(img)

        self.m.plot(img,self.histOfInput,title)
        self.show()

    def openTargetOperations(self, img):
        title = 'Target'
        self.histOfTarget = self.calc_Hist(img)
        self.m1.plot(img,self.histOfTarget,title)
        self.show()


    def calc_Hist(self,img):

        temphist=np.zeros((3,256))
        for i in range(0, self.row):
            for j in range(0, self.col):
                temphist[0, img[i, j, 0]] += 1
                temphist[1, img[i, j, 1]] += 1
                temphist[2, img[i, j, 2]] += 1

        return temphist

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4.5, height=7, dpi=85):
        fig = Figure(figsize=(width, height), dpi=dpi)


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

    def plot(self,img,hist,title):
        index = [0] * 256
        for i in range(0, 256):
            index[i] = i
        image = self.figure.add_subplot(4,1,1)
        image.imshow(img)
        image.set_title(title)
        fig1 = self.figure.add_subplot(4, 1, 2)
       # fig1.set_size_inches((5,3))

        fig1.bar(index,hist[0],color='r')

        fig2 = self.figure.add_subplot(4, 1, 3)
        #fig2.plot(hist[1], 'g-')
        fig2.bar(index, hist[1], color='g')

        fig3 = self.figure.add_subplot(4, 1, 4)
        #fig3.plot(hist[2], 'b-')
        fig3.bar(index, hist[2], color='b')

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())