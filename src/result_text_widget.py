import sys, os
from PyQt5.QtWidgets import QLabel, QApplication, QFormLayout, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QObject, pyqtSignal, QRect, Qt
from PyQt5.QtGui import QIcon, QPixmap

class resultTextWidget(QWidget):
    def __init__(self, correct):
        super(resultTextWidget, self).__init__()
        self.curDevName = ""
        self.correctList = correct
        #self.initUI()

    def initUI(self):
        self.resultspath_relative = "./res" + "/" + self.curDevName + "/results"
        self.resultspath_absolute = os.path.dirname(sys.argv[0]) + self.resultspath_relative[1:]

        self.image_names = os.listdir(self.resultspath_relative)
        self.nrOfImages = len(self.image_names)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.camera_names = ["left1", "right1", "above", "left2", "right2"]

        # "Correct", "Incorrect"
        self.grid.addWidget(QLabel("Correct"), 0, 1)
        self.grid.addWidget(QLabel("Incorrect"), 0, 2)

        # Per-camera rows
        self.dynamic_labels = []
        for row, camera in enumerate(self.camera_names):
            self.grid.addWidget(QLabel(camera), row + 1, 0)
            self.dynamic_labels.append((QLabel("0"), QLabel("0")))
            self.grid.addWidget(self.dynamic_labels[row][0], row + 1, 1)
            self.grid.addWidget(self.dynamic_labels[row][1], row + 1, 2)

        # Total row
        self.grid.addWidget(QLabel("total"), 6, 0)
        self.dynamic_labels.append((QLabel("0"), QLabel("0")))
        self.grid.addWidget(self.dynamic_labels[5][0], 6, 1)
        self.grid.addWidget(self.dynamic_labels[5][1], 6, 2)

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


        self.setLayout(self.grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Result Statistics')

        self.set_label_numbers()
        self.show()

    def set_label_numbers(self):
        totalCorrect = 0
        totalIncorrect = 0
        for i in range(5):
            self.dynamic_labels[i][0].setText(str(self.correctList[i][0]))
            totalCorrect += self.correctList[i][0]
            self.dynamic_labels[i][1].setText(str(self.correctList[i][1]))
            totalIncorrect += self.correctList[i][1]
        self.dynamic_labels[5][0].setText(str(totalCorrect))
        self.dynamic_labels[5][1].setText(str(totalIncorrect))


if __name__ == '__main__':
    import random
    app = QApplication(sys.argv)
    print('sys.argv[0] =', sys.argv[0])
    pathname = os.path.dirname(sys.argv[0])
    print('path =', pathname)
    print('full path =', os.path.abspath(pathname))
    window = resultTextWidget()
    window.curDevName = "dev1"
    window.initUI()
    sys.exit(app.exec_())