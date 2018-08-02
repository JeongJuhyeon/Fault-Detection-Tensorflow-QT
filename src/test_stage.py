# -*- coding: utf-8 -*-

import os

# Form implementation generated from reading ui file '.\test_stage.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import cv2
import numpy
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QFont

import config
import image_process
import inputBox
import predict
import result_images_widget_grid
import result_text_widget
import roi_unit


# Contains test stage UI

class Ui_MainWindow(object):
    def __init__(self, _mainUI=None):
        self.absPath = '../res'
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
        self.correctList = [[0, 0] for _ in range(5)]

    def setupUi(self, _mainwindow):
        css = """QPushButton { background-color: white;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 15px;    
                        border-color: black;
                        padding: 4px;
                    }"""
        font = QFont('D2Coding', 22, QFont.Light)
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

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 60, 781, 491))
        self.widget.setObjectName("widget")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(20, 50, 341, 421))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Home Button
        self.home = QtWidgets.QPushButton(self.centralwidget)
        self.home.setGeometry(QtCore.QRect(730, 10, 60, 60))
        self.home.clicked.connect(self.do_Home)
        self.home.setStyleSheet(css)
        self.home.setFont(font2)

        # "Set Device Number" Button
        self.button_device_number = QtWidgets.QPushButton(self.frame)
        self.button_device_number.setGeometry(QtCore.QRect(10, 10, 321, 61))
        self.button_device_number.setObjectName("button_device_number")
        self.button_device_number.clicked.connect(self.setDeviceNum)
        self.button_device_number.setStyleSheet(css)
        self.button_device_number.setFont(font)

        # "Capture" button
        self.button_capture = QtWidgets.QPushButton(self.frame)
        self.button_capture.setGeometry(QtCore.QRect(10, 80, 321, 61))
        self.button_capture.setFont(font)
        self.button_capture.setObjectName("button_capture")
        self.button_capture.setStyleSheet(css)
        # connect the image capture method
        self.button_capture.clicked.connect(self.img_capture)

        # "Camera autofocus" Check Box
        self.autofocus_checkbox = QtWidgets.QCheckBox("Autofocus", self.frame)
        self.autofocus_checkbox.setGeometry(QtCore.QRect(25, 140, 165, 100))
        self.autofocus_checkbox.setObjectName("autofocus_checkbox")
        self.autofocus_checkbox.setStyleSheet(css)
        self.autofocus_checkbox.setFont(font2)
        self.autofocus_checkbox.setChecked(config.AUTO_FOCUS)
        self.autofocus_checkbox.stateChanged.connect(config.change_autofocus)

        # Prev Button
        self.button_capture_prev = QtWidgets.QPushButton(self.frame)
        self.button_capture_prev.setText("<--")
        self.button_capture_prev.setGeometry(QtCore.QRect(140, 160, 50, 50))
        self.button_capture_prev.setStyleSheet(css)
        self.button_capture_prev.setFont(font2)
        self.button_capture_prev.clicked.connect(self.do_PrevSide)

        # "Next" Button
        self.button_capture_next = QtWidgets.QPushButton(self.frame)
        self.button_capture_next.setGeometry(QtCore.QRect(275, 160, 50, 50))
        self.button_capture_next.setObjectName("button_capture_next")
        self.button_capture_next.setStyleSheet(css)
        self.button_capture_next.setFont(font2)
        self.button_capture_next.clicked.connect(self.do_NextSide)

        # Side Label
        self.side_label = QtWidgets.QLabel(self.frame)
        self.side_label.setGeometry(QtCore.QRect(200, 150, 67, 70))
        self.side_label.setText("Side 1:\n" + config.SIDE_NAMES[0])
        self.side_label.setFont(QFont('D2Coding', 13, QFont.DemiBold))
        self.side_label.setStyleSheet("QLabel { border: 2px solid blue } ")

        # Vertical layout for "Start test" and "Show result" buttons
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 321, 180))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # "Start Test" Button
        self.button_start_test = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_start_test.sizePolicy().hasHeightForWidth())
        self.button_start_test.setSizePolicy(sizePolicy)

        self.button_start_test.setFont(font)
        self.button_start_test.setObjectName("button_start_test")
        self.button_start_test.clicked.connect(self.do_startTest)
        self.button_start_test.setStyleSheet(css)
        self.button_start_test.setFont(font)
        self.verticalLayout.addWidget(self.button_start_test)

        # Invisible label
        self.label_invisible = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_invisible.setFixedSize(20, 20)
        self.verticalLayout.addWidget(self.label_invisible)

        # "Show Result" Label
        self.label_show_results = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_show_results.setObjectName("label_show_result")
        self.label_show_results.setFont(QFont('D2Coding', 18))
        self.label_show_results.setStyleSheet(css)
        self.label_show_results.setAlignment(Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label_show_results)

        # Show "Text" Result Button
        self.button_text_result = QtWidgets.QPushButton(self.frame)
        self.button_text_result.setText("Text")
        #self.button_text_result.setGeometry(QtCore.QRect(230, 160, 60, 60))
        self.button_text_result.setFixedSize(150, 50)
        self.button_text_result.setStyleSheet(css)
        self.button_text_result.setFont(font2)
        self.button_text_result.clicked.connect(self.showTextResult)

        # Show "Images" Result Button
        self.button_images_result = QtWidgets.QPushButton(self.frame)
        self.button_images_result.setText("Images")
        self.button_images_result.setFixedSize(150, 50)
        self.button_images_result.setStyleSheet(css)
        self.button_images_result.setFont(font2)
        self.button_images_result.clicked.connect(self.showImagesResult)

        # Hbox for "Text" result and "Images" result buttons
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.button_text_result)
        hbox.addWidget(self.button_images_result)
        # hbox.addStretch(1)

        self.verticalLayout.addLayout(hbox)

        """
        # "Show Result" Button
        self.button_show_result = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_show_result.setObjectName("button_show_result")
        self.button_show_result.setFont(font)
        self.button_show_result.setStyleSheet(css)
        self.button_show_result.clicked.connect(self.show_Result)
        self.verticalLayout.addWidget(self.button_show_result)
        """

        #self.label_show_results.setSizePolicy(sizePolicy)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.label_show_results.sizePolicy().hasHeightForWidth())

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

        if not config.DEBUG_STAGE_ABSENT:
            config.initialize_machine()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Test Stage"))
        self.button_start_test.setText(_translate("MainWindow", "Start Test"))
        self.label_show_results.setText(_translate("MainWindow", "Show Results"))
        self.button_capture.setText(_translate("MainWindow", "Capture"))
        self.button_capture_next.setText(_translate("MainWindow", "-->"))
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

    # "Capture" Button method
    def img_capture(self):
        print('##-CAPTURE BUTTON PRESSED')
        self.ROI = roi_unit.readROI(os.path.join(self.absPath, self.deviceName, 'locationInfo.txt'),
                                    config.WINDOW_RATIO)
        print(self.ROI)
        predictPath = os.path.join(self.absPath, self.deviceName, 'predict')
        config.makeDir(predictPath)
        pOImagePath = os.path.join(predictPath, 'images')
        config.makeDir(pOImagePath)
        pCImagePath = os.path.join(predictPath, 'imagesCanny')
        config.makeDir(pCImagePath)

        side = self.sideName + str(self.sideNum)
        print(self.ROI[side])
        self.img = image_process.test_image_capture(self.ROI[side], pOImagePath, pCImagePath, self.cameraNum)
        cv2.imwrite(predictPath + '/' + side + '.jpg', self.img)
        self.imgview = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.graphicsView.setPixmap(QPixmap.fromImage(self.imgview))

    def do_NextSide(self):
        print("##-NEXT BUTTON CLICKED")
        self.cameraNum = (self.cameraNum + 1) % config.CAMERA_NUMBER  # CAMERA CHANGE
        self.sideNum = (self.sideNum) % 5 + 1
        side = 'side' + str(self.sideNum)
        print("##-CLIKED THE NEXT BUTTON :" + side)
        if not config.DEBUG_STAGE_ABSENT:
            if self.sideNum > 3:
                config.rotate_machine_with_degree(_x_value=450000, _y_value=500000)
            elif self.sideNum < 3: # UNTESTED
                config.rotate_machine_with_degree(_x_value=0, _y_value=0)
        self.side_label.setText("Side " + str(self.sideNum) + ":\n" + config.SIDE_NAMES[self.sideNum - 1])

    def do_PrevSide(self):
        self.cameraNum = (self.cameraNum - 1) % config.CAMERA_NUMBER  # CAMERA CHANGE
        self.sideNum = (self.sideNum - 2) % 5 + 1
        side = 'side' + str(self.sideNum)
        print("##-CLIKED THE NEXT BUTTON :" + side)
        if not config.DEBUG_STAGE_ABSENT:
            if self.sideNum > 3:
                config.rotate_machine_with_degree(_x_value=450000, _y_value=500000)
            elif self.sideNum < 3: # UNTESTED
                config.rotate_machine_with_degree(_x_value=0, _y_value=0)
        self.side_label.setText("Side " + str(self.sideNum) + ":\n" + config.SIDE_NAMES[self.sideNum - 1])


    # "Start Test" button method
    def do_startTest(self):
        print("##-TEST BUTTON CLICKED")

        path = os.path.join(self.absPath, self.deviceName)
        img_list = os.listdir(path + '/predict')
        classes = os.listdir(path + '/t_images')

        incor_class = {}
        for label in classes:
            if label.split('_')[-1] == 'incor':
                value = label.split('_')[1]
                if value in incor_class:
                    incor_class[value].append(label)
                else:
                    incor_class[value] = [label]

        self.smallImages = {}
        for image in img_list:
            if not os.path.isdir(path + '/predict/' + image):
                self.smallImages[image.split('.')[0]] = cv2.imread(path + '/predict/' + image)

        img_list = os.listdir(path + '/predict/imagesCanny')
        print('images to predict:', img_list)

        imageDir = path + '/predict/images'
        modelFullPath = path + '/model/retrained_graph.pb'
        labelsFullPath = path + '/model/retrained_labels.txt'
        tensorName = self.deviceName
        print('#Predicting')
        results = predict.run_inference_on_image(modelFullPath, labelsFullPath, imageDir, tensorName)

        # results is a [{}, {}, ..] list of dictionaries
        for result in results:
            image = result['imageName']
            sideNo = int(result['imageName'][4])
            print('#Predict Result[{}]'.format(image))
            matchRates = result['results']
            isCorrect = getResult(image, matchRates)

            print('result:', isCorrect, end='\n')

            start, end, side = self.getArea(image)

            if isCorrect == 'CORRECT':
                cv2.rectangle(self.smallImages[side], start, end, config.GREEN, 1)
                self.correctList[sideNo - 1][0] += 1
            elif isCorrect == 'CHECK':
                cv2.rectangle(self.smallImages[side], start, end, config.BLUE, 1)
            else:
                self.correctList[sideNo - 1][1] += 1
                cv2.rectangle(self.smallImages[side], start, end, config.RED, 1)

        self.graphicsView.setText("RESULT DATA")
        keys = self.smallImages.keys()
        result_path = os.path.join(self.absPath, self.deviceName, 'result')
        config.makeDir(result_path)
        print('Sides:', keys)
        for key in keys:
            cv2.imwrite(result_path + '/' + key + '.jpg', self.smallImages[key])
        self.showImagesResult()

    def showTextResult(self):
        print("##-SHOW TEXT RESULT BUTTON CLICKED")
        self.resultTextWidget = result_text_widget.resultTextWidget(self.correctList, self.deviceName)

    def showImagesResult(self):
        print("##-SHOW IMAGES RESULT BUTTON CLICKED")
        self.resultImagesWidget = result_images_widget_grid.resultImagesWidget(self.deviceName)

    def getArea(self, imageName):
        temp = imageName.split('.')[-2].split('_')
        side = temp[0]
        cur = None
        for roi in self.ROI[side]:
            if roi.side == side and roi.element == temp[1] and roi.number == temp[2]:
                cur = roi

        st, end = cur.getArea()
        return st, end, side


def getResult(imageName, result_arr):
    temp = imageName.split('_')
    correct_class = temp[0] + '_' + temp[1] + '_' + 'cor'

    print(result_arr)
    result_sum_dict = {}

    for result_pair in result_arr:
        temp = result_pair[0].decode('ascii').split(' ')
        result_class_name = temp[0] + '_' + temp[1] + '_' + temp[3]
        if result_class_name in result_sum_dict:
            result_sum_dict[result_class_name] += result_pair[1]
        else:
            result_sum_dict[result_class_name] = result_pair[1]

    maximum_class = None
    maximum_score = -1.0
    for result_sum_key in result_sum_dict.keys():
        if result_sum_dict[result_sum_key] > maximum_score:
            maximum_score = result_sum_dict[result_sum_key]
            maximum_class = result_sum_key

    print(maximum_class, correct_class)
    if maximum_class == correct_class:
        return 'CORRECT'
    else:
        return 'INCORRECT'

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
