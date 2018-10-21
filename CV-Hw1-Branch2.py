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
        self.setGeometry(100, 100, 800, 500)
        button = QPushButton('Histogram Equalizer', self)
        button.clicked.connect(self.equalize)
        button.move(10, 20)
        button.resize(140, 20)

        self.m = PlotCanvas(self)
        self.m.move(10, 40)
        self.m1 = PlotCanvas(self)
        self.m1.move(360, 40)


        self.show()

    def equalize(self):


        copiedInputHistogram=deepcopy(self.histOfInput)             #temp hist because main hist can be change
        copiedTargetHistogram = deepcopy(self.histOfTarget)

        print(copiedInputHistogram)


    def operations(self,q):
        if(q.text()=="Open Input"):
            filename = QFileDialog.getOpenFileName(self, "Image Select")
            # print(filename[0])
            img= cv2.imread(filename[0])
            img=cv2.cvtColor( img,cv2.COLOR_BGR2RGB)
            self.openInputOperations(img)
        elif(q.text()=="Open Target"):
            filename = QFileDialog.getOpenFileName(self, "Image Select")
            # print(filename[0])
            img = cv2.imread(filename[0])
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.openTargetOperations(img)
        else:
            QApplication.exit()

    def openInputOperations(self,img):
        #print('a')
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
        fig = Figure(figsize=(4.5, 7), dpi=85)


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
        fig1.plot(hist[0], 'r-')
        fig2 = self.figure.add_subplot(4, 1, 3)
        fig2.plot(hist[1], 'g-')


        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())