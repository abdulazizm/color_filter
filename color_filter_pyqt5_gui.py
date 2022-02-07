from asyncio.windows_events import NULL
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap, QColor, QImage
from PyQt5 import QtCore
import sys
import cv2
import numpy as np
from copy import deepcopy

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color filter")
        width = 640
        height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.cv_image = None
        self.qt_image = None
        self.cv_mask = None
        # create text label
        self.modelLabel = QLabel('Model:')
        self.modelEdit = QLineEdit('')
        self.numberLabel = QLabel('No:')
        self.numberEdit = QLineEdit('')
        self.decisionLabel = QLabel('Output:')
        self.outputLabel = QLabel('')

        self.openImgButton = QPushButton('Open image')
        self.openImgButton.clicked.connect(self.get_image)

        self.processButton = QPushButton('Filter red color in image')
        self.processButton.setDisabled(True)
        self.processButton.clicked.connect(self.show_op_image)

        modelHbox = QHBoxLayout()
        modelHbox.addWidget(self.modelLabel)
        modelHbox.addWidget(self.modelEdit)

        numberHbox = QHBoxLayout()
        numberHbox.addWidget(self.numberLabel)
        numberHbox.addWidget(self.numberEdit)

        decisionHbox = QHBoxLayout()
        decisionHbox.addWidget(self.decisionLabel)
        decisionHbox.addWidget(self.outputLabel)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addLayout(modelHbox)
        vbox.addLayout(numberHbox)
        vbox.addLayout(decisionHbox)
        vbox.addWidget(self.processButton)
        vbox.addWidget(self.openImgButton)

        # create a dummy grey pixmap
        grey = QPixmap(width, height)
        grey.fill(QColor('darkGray'))
        self.image_label.setPixmap(grey)

        hbox = QHBoxLayout()
        hbox.addWidget(self.image_label)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

    @QtCore.pyqtSlot()
    def show_op_image(self):
        if self.cv_image is not None:
            self.outputLabel.setText(str(self.process_img()))
            try:
                self.qt_image = QImage(self.cv_mask.data, self.cv_mask.shape[1], self.cv_mask.shape[0],QImage.Format_Indexed8)
                self.image_label.setPixmap(QPixmap(self.qt_image))
            except:
                print("Mask load error")
            self.processButton.setDisabled(True)

    @QtCore.pyqtSlot()
    def get_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','',"Image files (*.jpg *.gif *.png)")
        imagePath = fname[0]
        if imagePath: #https://stackoverflow.com/a/9573259
            self.cv_image = cv2.imread(imagePath)
            self.qt_image = QImage(cv2.resize(self.cv_image, (640,480), interpolation = cv2.INTER_AREA).data, 640, 480, 3*640, QImage.Format_RGB888).rgbSwapped()
            self.image_label.setPixmap(QPixmap(self.qt_image))
            self.processButton.setDisabled(False)

    def process_img(self):
        img = deepcopy(self.cv_image)
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # color space conversion - basic need for color filter
        lower_red_limit = np.array([150,150,0]) # adjust values if required
        upper_red_limit = np.array([180,255,255]) # adjust values if required

        mask = cv2.inRange(img_hsv, lower_red_limit, upper_red_limit) # prepare mask - shows occurence of red color in the image
        
        # do application specific things - check if red color is in more than 10000 pixels
        unique, counts = np.unique(mask, return_counts=True)
        mask_dict = dict(zip(unique, counts))
        self.cv_mask = cv2.resize(deepcopy(mask), (640,480), interpolation = cv2.INTER_AREA)
        # self.cv_mask = deepcopy(mask)

        if len(mask_dict) > 1 and mask_dict[255] > 10000: # fix this magic number (10000) as per need - this says "if mask_dict[255] is in 10000 pixels/dots in the image"
            return True
        else:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
