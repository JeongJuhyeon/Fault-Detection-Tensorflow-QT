import sys, os
from PyQt5.QtWidgets import QLabel, QApplication, QFormLayout, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QObject, pyqtSignal, QRect, Qt
from PyQt5.QtGui import QIcon, QPixmap

class resultImagesWidget(QWidget):
    def __init__(self, curDevName):
        super(resultImagesWidget, self).__init__()
        self.curDevName = curDevName
        self.initUI()

    def initUI(self):
        self.curImg = 1
        self.resultspath_relative = "./res" + "/" + self.curDevName + "/results"
        self.resultspath_absolute = os.path.dirname(sys.argv[0]) + self.resultspath_relative[1:]

        self.image_names = os.listdir(self.resultspath_relative)
        self.nrOfImages = len(self.image_names)

        # "previous" button
        self.button_previous = QPushButton("Previous")
        #self.button_previous.move(10, 10)
        self.button_previous.clicked.connect(self.onPrevious)
        self.button_previous.setDisabled(True)
        #self.button_previous.setText("Previous")

        # "next" button
        self.button_next = QPushButton("Next")
        #self.button_next.move(190, 10)
        self.button_next.clicked.connect(self.onNext)
        if self.nrOfImages == 1:
            self.button_next.setDisabled(True)
        #self.button_next.setText("Next")


        """# Horizontal box for the buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_previous)
        hbox.addWidget(self.button_next)
        hbox.addStretch(1)
        """

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

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
        #self.resize(self.pixmap.width() + 200, self.pixmap.height() + 200)

        """
        # Vertical box to add everything to
        vbox = QVBoxLayout()
        vbox.addWidget(self.imageNoLabel)
        vbox.addWidget(self.imageLabel)
        vbox.addLayout(hbox)
        vbox.setAlignment(Qt.AlignVCenter)
        self.setLayout(vbox)
        """

        self.grid.addWidget(self.imageNoLabel, 1, 6)
        self.grid.addWidget(self.imageLabel, 2, 1, 5, 10)
        self.grid.addWidget(self.button_previous, 8, 5)
        self.grid.addWidget(self.button_next, 8, 6)


        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Result Images')
        self.show()

    def onPrevious(self):
        self.curImg -= 1
        self.pixmap = QPixmap(self.resultspath_absolute + "/" + self.image_names[self.curImg - 1])
        self.imageLabel.setPixmap(self.pixmap)
        if not self.button_next.isEnabled():
            self.button_next.setEnabled(True)
        if self.curImg == 1:
            self.button_previous.setDisabled(True)
        self.imageNoLabel.setText(str(self.curImg) + "/" + str(self.nrOfImages))

    def onNext(self):
        self.curImg += 1
        self.pixmap = QPixmap(self.resultspath_absolute + "/" + self.image_names[self.curImg - 1])
        self.imageLabel.setPixmap(self.pixmap)
        if not self.button_previous.isEnabled():
            self.button_previous.setEnabled(True)
        if self.curImg == self.nrOfImages:
            self.button_next.setDisabled(True)
        self.imageNoLabel.setText(str(self.curImg) + "/" + str(self.nrOfImages))

if __name__ == '__main__':
    import random
    app = QApplication(sys.argv)
    print('sys.argv[0] =', sys.argv[0])
    pathname = os.path.dirname(sys.argv[0])
    print('path =', pathname)
    print('full path =', os.path.abspath(pathname))
    window = resultImagesWidget()
    window.curDevName = "dev1"
    window.initUI()
    sys.exit(app.exec_())