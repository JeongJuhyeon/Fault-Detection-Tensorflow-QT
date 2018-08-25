import sys
import time

import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import camerasetting_dialog
import cameraxy_inputbox
import config
import image_process
import inputBox
import test_stage
import training_stage


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

        # Camera Configuration
        self.button_camera_configuration = QtWidgets.QPushButton("Camera configuration", self.verticalLayoutWidget)
        self.button_camera_configuration.setMinimumSize(QtCore.QSize(1, 100))
        self.button_camera_configuration.setStyleSheet(css)
        self.button_camera_configuration.setFont(font)
        self.button_camera_configuration.clicked.connect(self.select_camera_numbers)
        self.verticalLayout.addWidget(self.button_camera_configuration)


        self.interface.setCentralWidget(self.centralwidget)
        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self.interface)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.interface.setWindowTitle(_translate("Interface", "MainWindow"))
        self.button_training_stage.setText(_translate("Interface", "Training Stage"))
        self.button_test_stage.setText(_translate("Interface", "Test Stage"))

    def go_training_stage(self):
        inputbox = inputBox.App("Enter the device name")
        inputbox.do_UI()
        if inputbox.getValue() is None:
            return

        print("##-RETURN  VALUE : " + inputbox.getValue())

        """ # OBSOLETE?
        # If we already went to the training stage before, and now we want to train a different device
        try:
            if self.training_interface.dirName != inputbox.getValue():
                image_process.reset_global_roi_list()
        except AttributeError as e:
            # First device after starting the program
            pass
        """

        cameraxyinputbox = cameraxy_inputbox.cameraXYInputbox(inputbox.getValue())

        # In training stage, it's fine if it's a new model.
        try:
            cameraxyinputbox.searchDevice()
        except FileNotFoundError:
            pass

        cameraxyinputbox.exec()
        self.initialize_machine(inputBox_lineEdits=cameraxyinputbox.lineEdits)

        self.training_Window = QtWidgets.QMainWindow()
        self.training_interface = training_stage.Ui_MainWindow(self.interface)
        self.training_interface.setupUi(self.training_Window)

        self.training_interface.dirName = inputbox.getValue()
        self.training_interface.setState()
        self.training_Window.show()
        self.interface.close()
        inputbox.close()
        print("##-STAGE CHANGED(Training Stage)")

    def go_test_stage(self):
        inputbox = inputBox.App("Enter the device name")
        inputbox.do_UI()
        if inputbox.getValue() is None:
            return

        print("##RETURN  VALUE : " + inputbox.getValue())

        cameraxyinputbox = cameraxy_inputbox.cameraXYInputbox(inputbox.getValue())

        # In the test stage, we can't have a new model.
        try:
            cameraxyinputbox.searchDevice()
        except FileNotFoundError:
            print("Device named " + inputbox.getValue() + " not found.")
            return

        self.initialize_machine(inputBox_lineEdits=cameraxyinputbox.lineEdits)

        self.test_Window = QtWidgets.QMainWindow()
        self.test_interface = test_stage.Ui_MainWindow(self.interface)
        self.test_interface.setupUi(self.test_Window, inputbox.getValue())

        # self.test_interface.deviceName = inputbox.getValue()
        self.test_Window.show()
        self.interface.close()
        inputbox.close()
        print("##-STAGE CHANGED(Test Stage)")

    def select_camera_numbers(self):
        cameradialog = camerasetting_dialog.CameraSettingDialog()
        camera_order = []
        cameraConfigObject = config.cameraConfig()
        for old_number in range(3):
            img = image_process.get_image_from_camera(old_number + 1, size_conf=config.WINDOW_SIZE)
            cv2.imshow('Camera', img)
            button_pressed = cameradialog.exec()
            if button_pressed == 0x00000800:
                camera_order.append('LEFT')
            elif button_pressed == 0x00800000:
                camera_order.append('CENTER')
            elif button_pressed == 0x00200000:
                camera_order.append('RIGHT')
            cv2.destroyAllWindows()

        for i, camera in enumerate(camera_order):
            cameraConfigObject.set_camera_number(camera, i)


    def create_inputBox(self):
        inputbox = inputBox.App("Enter the device name")
        inputbox.do_UI()
        print("return value : " + self.inputbox.getValue())
        # print(self.inputbox.text)

    def initialize_machine(self, inputBox_lineEdits):
        if config.DEBUG_STAGE_ABSENT:
            return

        print("## INITIALIZE MACHINE")
        print(inputBox_lineEdits[0].text())
        _left_x, _right_x = int(inputBox_lineEdits[0].text()), int(inputBox_lineEdits[1].text())
        _left_y, _right_y = int(inputBox_lineEdits[3].text()), int(inputBox_lineEdits[4].text())
        _center_y = int(inputBox_lineEdits[2].text())

        config.initialize_machine()
        time.sleep(12)
        config.move_camera_with_position(1, 1, _center_y)
        config.move_camera_with_position(2, _left_x, _left_y)
        config.move_camera_with_position(3, _right_x, _right_y)

def main():
    app = QtWidgets.QApplication(sys.argv)
    Interface = QtWidgets.QMainWindow()
    ui = Ui_Interface()
    ui.setupUi(Interface)
    Interface.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
