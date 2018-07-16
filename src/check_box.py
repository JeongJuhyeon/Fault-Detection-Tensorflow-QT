import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
import image_process


class MyWindow(QWidget):
    def __init__(self, dic, devicename):
        super().__init__()
        self.dic = dic
        self.devicename = devicename
        self.setupUI()
        self.flag = False

    def setupUI(self):
        self.setWindowTitle('Choose')
        self.setGeometry(800, 200, 300, 300)
        groupBox = QGroupBox("시간 단위", self)
        groupBox.move(10, 10)
        self.radios = []
        y = 20
        for attr in self.dic[self.devicename]:
            radio = QRadioButton(attr, self)
            radio.move(20, y)
            radio.setChecked(True)
            radio.clicked.connect(self.radioButtonClicked)
            y += 20
            self.radios.append(radio)

        groupBox.resize(280, y)

        _translate = QtCore.QCoreApplication.translate
        self.button = QtWidgets.QPushButton(self)
        self.button.move(100, y + 20)
        self.button.setEnabled(True)
        self.button.setMinimumSize(QtCore.QSize(1, 25))
        self.button.setObjectName("select")
        self.button.setText(_translate("Interface", "select"))
        self.button.clicked.connect(self.confirm)

    def do_UI(self):
        self.show()

    def confirm(self):
        self.flag = True
        self.hide()

    def radioButtonClicked(self):
        for i in range(len(self.radios)):
            if (self.radios[i].isChecked()):
                self.radio_value = self.dic[self.devicename][i]

    def getValue(self):
        self.flag = False
        return self.radio_value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dic = image_process.readfile()
    mywindow = MyWindow(dic, 'device2')
    mywindow.do_UI()
    sys.exit(app.exec_())