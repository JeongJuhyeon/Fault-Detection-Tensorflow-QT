# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test_stage.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import cv2
import numpy
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt

import os
from src import image_process, predict, inputBox, config, roi_unit


class Ui_MainWindow(object):
    def __init__(self, _mainUI = None):
        self.absPath = './../res/'
        self.deviceName = 'device'
        self.sideName = 'side'
        self.sideNum = 1
        self.sideBox = inputBox.App("Enter the Side name")
        self.deviceBox = inputBox.App("Enter the Device Name")
        self.img = numpy.ndarray
        self.imgview = QImage
        self.mainUI = _mainUI
        self.cameraNum = 0
        self.model = None
        self.ROI = None
        self.smallImages = {}

    def setupUi(self, _mainwindow):
        css = """QPushButton { background-color: white;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 15px;    
                        border-color: black;
                        padding: 4px;
                    }"""
        font = QFont('D2Coding', 25, QFont.Light)
        font2 = QFont('D2Coding', 12, QFont.Light)
        self.MainWindow = _mainwindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 600)
        pal = self.MainWindow.palette()
        pal.setColor(self.MainWindow.backgroundRole(), Qt.white)
        self.MainWindow.setPalette(pal)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font3 = QFont('D2Coding', 25, QFont.Light)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 781, 41))

        self.label.setFont(font3)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        # Home Button
        self.home = QtWidgets.QPushButton(self.centralwidget)
        self.home.setGeometry(QtCore.QRect(730, 10, 50, 50))
        self.home.clicked.connect(self.do_Home)
        self.home.setStyleSheet(css)
        self.home.setFont(font2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 60, 781, 491))
        self.widget.setObjectName("widget")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(20, 50, 341, 421))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 260, 321, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_start_test = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy.setHeightForWidth(self.button_start_test.sizePolicy().hasHeightForWidth())

        #Start Button
        self.button_start_test.setSizePolicy(sizePolicy)
        self.button_start_test.setFont(font)
        self.button_start_test.setObjectName("button_start_test")
        self.button_start_test.clicked.connect(self.do_startTest)
        self.button_start_test.setStyleSheet(css)
        self.button_start_test.setFont(font)
        self.verticalLayout.addWidget(self.button_start_test)

        self.button_show_result = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_show_result.sizePolicy().hasHeightForWidth())
        #Show Button
        self.button_show_result.setSizePolicy(sizePolicy)
        self.button_show_result.setObjectName("button_show_result")
        self.button_show_result.setFont(font)
        self.button_show_result.setStyleSheet(css)
        self.button_show_result.clicked.connect(self.show_Result)
        self.verticalLayout.addWidget(self.button_show_result)

        #Capture button
        self.button_capture = QtWidgets.QPushButton(self.frame)
        self.button_capture.setGeometry(QtCore.QRect(10, 80, 321, 61))
        self.button_capture.setFont(font)
        self.button_capture.setObjectName("button_capture")
        self.button_capture.setStyleSheet(css)
        # connect the image capture method
        self.button_capture.clicked.connect(self.img_capture)

        #Next Button
        self.button_capture_next = QtWidgets.QPushButton(self.frame)
        self.button_capture_next.setGeometry(QtCore.QRect(170, 150, 161, 30))
        self.button_capture_next.setObjectName("button_capture_next")
        self.button_capture_next.clicked.connect(self.do_Nextbutton)
        self.button_capture_next.setFont(font2)
        self.button_capture_next.setStyleSheet(css)

        #Set Device Number
        self.button_device_number = QtWidgets.QPushButton(self.frame)
        self.button_device_number.setGeometry(QtCore.QRect(10, 10, 321, 61))
        self.button_device_number.setObjectName("button_device_number")
        self.button_device_number.clicked.connect(self.setDeviceNum)
        self.button_device_number.setStyleSheet(css)
        self.button_device_number.setFont(font)

        self.graphicsView = QtWidgets.QLabel(self.widget)
        self.graphicsView.setGeometry(QtCore.QRect(370, 60, 401, 391))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setText("Cannot load the image Please Capture button")
        self.graphicsView.setAlignment(QtCore.Qt.AlignCenter)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Test Stage"))
        self.button_start_test.setText(_translate("MainWindow", "Start Test"))
        self.button_show_result.setText(_translate("MainWindow", "Show Result"))
        self.button_capture.setText(_translate("MainWindow", "Capture"))
        self.button_capture_next.setText(_translate("MainWindow", "Next"))
        self.button_device_number.setText(_translate("MainWindow", "Device #"))
        self.home.setText(_translate("MainWindow", "Home"))

    def do_Home(self):
        print("##-Return Home Stage")
        self.mainUI.show()
        self.MainWindow.close()

    def setDeviceNum(self):
        self.deviceBox.do_UI()
        self.deviceName = self.deviceBox.getValue()
        self.sideBox.do_UI()
        self.sideName = self.sideBox.getValue()
        path = self.absPath + self.deviceName + '/' + self.sideName
        print('##-PATH : ' + path)

    def img_capture(self):
        print('##-CAPTURE BUTTON PRESSED')
        self.ROI = roi_unit.readROI(self.absPath + self.deviceName + '/locationInfo.txt',
                                    config.WINDOW_RATIO)

        predictPath = self.absPath + self.deviceName + '/predict'; config.makeDir(predictPath)
        pOImagePath= self.absPath + self.deviceName + '/predict/images'; config.makeDir(pOImagePath)
        pCImagePath = self.absPath + self.deviceName + '/predict/imagesCanny'; config.makeDir(pCImagePath)

        side = self.sideName + str(self.sideNum)
        print(self.ROI[side])
        self.img = image_process.test_image_capture(self.ROI[side], pOImagePath, pCImagePath, self.cameraNum)
        cv2.imwrite(predictPath + '/' + side +'.jpg', self.img)
        self.imgview = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.graphicsView.setPixmap(QPixmap.fromImage(self.imgview))

    def do_Nextbutton(self):
        print("##-NEXT BUTTON CLICKED")
        self.sideNum += 1
        self.cameraNum = (self.cameraNum + 1) % config.CAMERA_NUMBER

    def do_startTest(self):
        print("##-TEST BUTTON CLICKED")
        ## You write the To-do method here
        path = self.absPath + self.deviceName
        img_list = os.listdir(path + '/predict')
        classes = os.listdir(path + '/t_images')

        incor_class = {}
        for label in classes :
            if label.split('_')[-1] == 'incor' :
                value = label.split('_')[1]
                if value in incor_class : incor_class[value].append(label)
                else : incor_class[value] = [label]

        self.smallImages = {}
        for image in img_list :
            if not os.path.isdir(path + '/predict/' + image) :
                self.smallImages[image.split('.')[0]] = cv2.imread(path + '/predict/' + image)

        img_list = os.listdir(path + '/predict/imagesCanny')
        print('images to predict:', img_list)

        imageDir = path + '/predict/images'
        modelFullPath = path + '/model/retrained_graph.pb'
        labelsFullPath = path + '/model/retrained_labels.txt'
        tensorName = self.deviceName
        print('#Predicting')
        results = predict.run_inference_on_image(modelFullPath, labelsFullPath, imageDir, tensorName)

        for result in results :
            image = result['imageName']
            print('#Predict Result[{}]'.format(image))
            matchRates = result['results']
            isSuit = getResult(image, matchRates)

            print('result:', isSuit, end='\n')

            start, end, side = self.getArea(image)

            if isSuit == 'CORRECT':
                cv2.rectangle(self.smallImages[side], start, end, config.GREEN, 2)
            elif isSuit == 'CHECK' :
                cv2.rectangle(self.smallImages[side], start, end, config.BLUE, 2)
            else :
                cv2.rectangle(self.smallImages[side], start, end, config.RED, 2)

    def show_Result(self):
        print("##-SHOW RESULT BUTTON CLICKED")
        ## You write the To-do method here and Set result
        self.graphicsView.setText("RESULT DATA")
        keys = self.smallImages.keys()
        result_path = self.absPath + self.deviceName + '/result'
        config.makeDir(result_path)
        print('Sides:',keys)
        for key in keys :
            cv2.imwrite(result_path + '/' + key + '.jpg', self.smallImages[key])

    def getArea(self, imageName):
        temp = imageName.split('.')[-2].split('_')
        side = temp[0]
        cur = None
        for roi in self.ROI[side]:
            if roi.side == side and roi.element == temp[1] and roi.number == temp[2] :
                cur = roi

        st, end = cur.getArea()
        return st, end, side

def getResult(imageName, result_arr):
    temp = imageName.split('_')
    currect_class = temp[0] + '_' + temp[1] + '_' + 'cor'
    temp = result_arr[0][0].decode('ascii').split(' ')
    current_class = temp[0] + '_' + temp[1] + '_' + temp[3]
    print(current_class, currect_class)

    if result_arr[0][1] > 0.7 and current_class == currect_class : return 'CORRECT'
    else : return 'INCORRECT'

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())