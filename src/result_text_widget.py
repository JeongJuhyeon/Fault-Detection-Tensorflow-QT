import config
import os
import sys

from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QGridLayout


class resultTextWidget(QWidget):
    def __init__(self, curDevname, correct, times):
        super(resultTextWidget, self).__init__()
        self.curDevName = curDevname
        self.correctList = correct
        self.times = times
        self.initUI()

    def initUI(self):
        self.resultspath_relative = "../res" + "/" + self.curDevName + "/result"
        self.resultspath_absolute = os.path.dirname(sys.argv[0])[0:-4] + self.resultspath_relative.split('.')[-1]

        self.image_names = os.listdir(self.resultspath_relative)
        self.nrOfImages = len(self.image_names)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.camera_names = config.SIDE_NAMES

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

        # Set correct label numbers
        self.set_correct_label_numbers()

        # Invisible empty row
        self.grid.addWidget(QLabel(""), 7, 0)

        # Start, end, per-inspection rows
        self.grid.addWidget(QLabel("start time"), 8, 0)
        self.grid.addWidget(
            QLabel(" " + str(datetime.time(times[0].hour, times[0].minute, times[0].second, times[0].microsecond))),
            8, 1, 1, 2)

        self.grid.addWidget(QLabel("end time"), 9, 0)
        self.grid.addWidget(
            QLabel(" " + str(datetime.time(times[1].hour, times[1].minute, times[1].second, times[1].microsecond))),
            9, 1, 1, 2)

        self.grid.addWidget(QLabel("time per inspected part"), 10, 0, 1, 1)
        diff = times[1] - times[0]
        diff_per_part = diff / (self.totalCorrect + self.totalIncorrect)
        self.grid.addWidget(QLabel("   " + str(diff_per_part)), 10, 1, 1, 2)

        # Resize window
        # self.resize(self.pixmap.width() + 200, self.pixmap.height() + 200)

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

        self.show()

    def set_correct_label_numbers(self):
        self.totalCorrect = 0
        self.totalIncorrect = 0
        for i in range(5):
            self.dynamic_labels[i][0].setText(str(self.correctList[i][0]))
            self.totalCorrect += self.correctList[i][0]
            self.dynamic_labels[i][1].setText(str(self.correctList[i][1]))
            self.totalIncorrect += self.correctList[i][1]
        self.dynamic_labels[5][0].setText(str(self.totalCorrect))
        self.dynamic_labels[5][1].setText(str(self.totalIncorrect))


if __name__ == '__main__':
    import datetime

    app = QApplication(sys.argv)
    print('sys.argv[0] =', sys.argv[0])
    pathname = os.path.dirname(sys.argv[0])
    print('path =', pathname)
    print('full path =', os.path.abspath(pathname))

    correctlist = [[1, 0] for _ in range(5)]
    curDevName = "dev1"
    times = [datetime.datetime.now(), datetime.datetime(2018, datetime.datetime.now().month,
                                                        datetime.datetime.now().day, datetime.datetime.now().hour + 1,
                                                        10, 9, 8)]

    window = resultTextWidget(curDevName, correctlist, times)
    window.initUI()
    sys.exit(app.exec_())
