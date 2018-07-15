import sys, os
from PyQt5.QtWidgets import QLabel, QApplication, QFormLayout, QLineEdit, QPushButton, QDialogButtonBox, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QPixmap

class resultImagesWidget(QWidget):
    def __init__(self):
        super(resultImagesWidget, self).__init__()
        #self.initUI()

    def initUI(self):
        self.curImg = 1
        self.curDevName = "dev1"
        self.resultspath_relative = "./res" + "/" + self.curDevName + "/results"
        self.resultspath_absolute = os.path.dirname(sys.argv[0]) + self.resultspath_relative[1:]

        self.image_names = os.listdir(self.resultspath_relative)
        self.nrOfImages = len(self.image_names)

        # "left" button
        self.button_left = QPushButton(self)
        self.button_left.move(10, 10)
        self.button_left.clicked.connect(self.onLeft)
        self.button_left.setDisabled(True)
        self.button_left.setText("Left")

        # "right" button
        self.button_right = QPushButton(self)
        self.button_right.move(190, 10)
        self.button_right.clicked.connect(self.onRight)
        if self.nrOfImages == 1:
            self.button_right.setDisabled(True)
        self.button_right.setText("Right")

        #Label that shows cur/max image number
        self.imageNoLabel = QLabel(self)
        self.imageNoLabel.setText("1/" + str(self.nrOfImages))
        self.imageNoLabel.move(140, 15)

        #Pixmap that will show the image
        self.pixmap = QPixmap(self.resultspath_absolute + "/" + self.image_names[self.curImg - 1])

        # Label that will contain the pixmap to show the image
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(QRect(370, 60, 401, 391))
        self.imageLabel.setPixmap(self.pixmap)

        # Resize window
        self.resize(self.pixmap.width() + 200, self.pixmap.height() + 200)
        self.show()

    def onLeft(self):
        self.curImg -= 1
        self.imageLabel.setPixmap(self.pixmap)
        if not self.button_right.isEnabled():
            self.button_right.setEnabled(True)
        if self.curImg == 1:
            self.button_left.setDisabled(True)
        self.pixmap = QPixmap(self.resultspath_absolute + "/" + self.image_names[self.curImg - 1])
        self.imageNoLabel.setText(str(self.curImg) + "/" + str(self.nrOfImages))

    def onRight(self):
        self.curImg += 1
        self.imageLabel.setPixmap(self.pixmap)
        if not self.button_left.isEnabled():
            self.button_left.setEnabled(True)
        if self.curImg == self.nrOfImages:
            self.button_right.setDisabled(True)
        self.pixmap = QPixmap(self.resultspath_absolute + "/" + self.image_names[self.curImg - 1])
        self.imageNoLabel.setText(str(self.curImg) + "/" + str(self.nrOfImages))

if __name__ == '__main__':
    import random
    app = QApplication(sys.argv)
    print('sys.argv[0] =', sys.argv[0])
    pathname = os.path.dirname(sys.argv[0])
    print('path =', pathname)
    print('full path =', os.path.abspath(pathname))
    window = resultImagesWidget()
    # dialog.curDevName = "dev1"
    # a = dialog.show()
    sys.exit(app.exec_())