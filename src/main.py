import sys

from src import test_stage, inputBox, training_stage, devname_cameraxy_inputbox

from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt


class Ui_Interface(object):
    def setupUi(self, _interface):
        self.interface = _interface
        self.interface.setObjectName("Interface")
        self.interface.resize(800, 600)
        # Set Backgroud
        self.interface.setAutoFillBackground(False)
        pal = self.interface.palette()
        # pal.setColor(self.interface.backgroundRole(), QColor(int('1E',16),int('90',16),int('FF',16)))
        pal.setColor(self.interface.backgroundRole(), Qt.white)
        self.interface.setPalette(pal)

        self.centralwidget = QtWidgets.QWidget(self.interface)
        self.centralwidget.setMinimumSize(QtCore.QSize(200, 200))
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 741, 571))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        css = """QPushButton { background-color: white;
                border-style: outset;
                border-width: 2px;
                border-radius: 15px;    
                border-color: black;
                padding: 4px;
            }
        
            """
        # Training Stage Button
        self.button_training_stage = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_training_stage.setEnabled(True)
        self.button_training_stage.setMinimumSize(QtCore.QSize(1, 100))
        self.button_training_stage.setObjectName("button_training_stage")
        font = QFont('D2Coding', 25, QFont.Light)
        self.button_training_stage.setFont(font)
        self.button_training_stage.setStyleSheet(css)
        self.button_training_stage.clicked.connect(self.go_training_stage)
        self.verticalLayout.addWidget(self.button_training_stage)

        # Test Stage Button
        self.button_test_stage = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_test_stage.setMinimumSize(QtCore.QSize(1, 100))
        self.button_test_stage.setObjectName("button_test_stage")
        self.button_test_stage.clicked.connect(self.go_test_stage)
        self.button_test_stage.setStyleSheet(css)
        self.button_test_stage.setFont(font)
        self.verticalLayout.addWidget(self.button_test_stage)

        # Statistics Button
        self.button_statistic_stage = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_statistic_stage.setMinimumSize(QtCore.QSize(1, 100))
        self.button_statistic_stage.setObjectName("button_statistic_stage")
        self.button_statistic_stage.setStyleSheet(css)
        self.button_statistic_stage.setFont(font)
        # self.button_statistic_stage.clicked.connect(self.create_inputBox)
        self.verticalLayout.addWidget(self.button_statistic_stage)

        self.interface.setCentralWidget(self.centralwidget)
        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self.interface)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.interface.setWindowTitle(_translate("Interface", "MainWindow"))
        self.button_training_stage.setText(_translate("Interface", "Training Stage"))
        self.button_test_stage.setText(_translate("Interface", "Test Stage"))
        self.button_statistic_stage.setText(_translate("Interface", "Statistic & Result"))

    def go_test_stage(self):
        inputbox = inputBox.App("Enter the device name")
        inputbox.do_UI()
        print("##RETURN  VALUE : " + inputbox.getValue())
        self.test_Window = QtWidgets.QMainWindow()
        self.test_interface = test_stage.Ui_MainWindow(self.interface)
        self.test_interface.setupUi(self.test_Window)

        self.test_interface.deviceName = inputbox.getValue()
        self.test_Window.show()
        self.interface.close()
        inputbox.close()
        print("##-STAGE CHANGED(Test Stage)")

    def go_training_stage(self):
        cameraxyinputbox = devname_cameraxy_inputbox.devnameCameraXYInputbox()

        inputbox = inputBox.App("Enter the device name")
        inputbox.do_UI()
        print("##-RETURN  VALUE : " + inputbox.getValue())
        cameraxyinputbox.curDevName = inputbox.getValue()
        cameraxyinputbox.searchDevice()
        cameraxyinputbox.exec()

        self.training_Window = QtWidgets.QMainWindow()
        self.training_interface = training_stage.Ui_MainWindow(self.interface)
        self.training_interface.setupUi(self.training_Window)

        self.training_interface.dirName = inputbox.getValue()
        self.training_interface.setState()
        self.training_Window.show()
        self.interface.close()
        inputbox.close()
        print("##-STAGE CHANGED(Training Stage)")

    def create_inputBox(self):
        inputbox = inputBox.App("Enter the device name")
        inputbox.do_UI()
        print("return value : " + self.inputbox.getValue())
        # print(self.inputbox.text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    Interface = QtWidgets.QMainWindow()
    ui = Ui_Interface()
    ui.setupUi(Interface)
    Interface.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
