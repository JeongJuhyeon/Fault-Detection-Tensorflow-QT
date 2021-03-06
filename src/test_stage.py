# -*- coding: utf-8 -*-

import datetime
import json
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

import cameraxy_inputbox
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
        self.curDeviceNo = 1
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
        self.startEndTimes = []
        self.result_directories = []

    def setupUi(self, _mainwindow, curDeviceName):
        self.deviceName = curDeviceName
        self.curDeviceNo = self.get_device_number()
        self.resultsDeviceNo = self.curDeviceNo - 1

        css = """QPushButton { background-color: white;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 15px;    
                        border-color: black;
                        padding: 4px;
                    }"""
        font = QFont('D2Coding', 22, QFont.Light)
        font2 = QFont('D2Coding', 12, QFont.Light)
        font3 = QFont('D2Coding', 25, QFont.Light)

        self.MainWindow = _mainwindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 600)
        pal = self.MainWindow.palette()
        pal.setColor(self.MainWindow.backgroundRole(), Qt.white)
        self.MainWindow.setPalette(pal)

        # Central widget on MainWindow. This has the 'Test Stage' label, Device name label, and Home Button on it.
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Widget on central widget. This has the graphics view on it.
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 60, 781, 491))
        self.widget.setObjectName("widget")

        # Frame on Widget. This has all the buttons on it.
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setGeometry(QtCore.QRect(20, 50, 341, 421))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # 'Test Stage' Label
        self.label_test_stage = QtWidgets.QLabel(self.centralwidget)
        self.label_test_stage.setGeometry(QtCore.QRect(35, 20, 140, 41))
        self.label_test_stage.setFont(font)
        # self.label_test_stage.setAlignment(QtCore.Qt.AlignCenter)
        self.label_test_stage.setObjectName("label")

        # Device name label
        self.label_device_name = QtWidgets.QLabel(self.centralwidget)
        self.label_device_name.setText(self.deviceName)
        self.label_device_name.setGeometry(QtCore.QRect(230, 20, round(len(self.deviceName) * 9.3 + 20), 41))
        self.label_device_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_device_name.setFont(QFont('D2Coding', 13, QFont.DemiBold))
        self.label_device_name.setStyleSheet("QLabel { border: 2px solid black } ")

        # Home Button
        self.home = QtWidgets.QPushButton(self.centralwidget)
        self.home.setGeometry(QtCore.QRect(730, 10, 60, 60))
        self.home.clicked.connect(self.do_Home)
        self.home.setStyleSheet(css)
        self.home.setFont(font2)

        # "Set Device Number" Button
        """
        self.button_device_number = QtWidgets.QPushButton(self.frame)
        self.button_device_number.setGeometry(QtCore.QRect(10, 10, 321, 61))
        self.button_device_number.setObjectName("button_device_number")
        self.button_device_number.setText("Device #")
        self.button_device_number.clicked.connect(self.setDeviceNum)
        self.button_device_number.setStyleSheet(css)
        self.button_device_number.setFont(font)
        """

        # "검사할 시료" label
        self.label_device_to_test = QtWidgets.QLabel("검사할 시료:", self.frame)
        self.label_device_to_test.setGeometry(10, 15, 321, 60)
        self.label_device_to_test.setFont(QFont('Malgun Gothic', 16, QFont.Medium))
        self.label_device_to_test.setStyleSheet(css)


        # Current device number label
        self.label_device_number = QtWidgets.QLabel(self.frame)
        self.label_device_number.setGeometry(10, 20, 321, 50)
        self.label_device_number.setFont(font)
        self.label_device_number.setAlignment(QtCore.Qt.AlignCenter)
        self.label_device_number.setStyleSheet(css)

        # "Capture" button
        self.button_capture = QtWidgets.QPushButton(self.frame)
        self.button_capture.setGeometry(QtCore.QRect(10, 70, 321, 50))  # x, y, w, h
        self.button_capture.setFont(font)
        self.button_capture.setObjectName("button_capture")
        self.button_capture.setStyleSheet(css)
        # connect the image capture method
        self.button_capture.clicked.connect(self.img_capture)

        # "Camera autofocus" Check Box
        self.autofocus_checkbox = QtWidgets.QCheckBox("Autofocus", self.frame)
        self.autofocus_checkbox.setGeometry(QtCore.QRect(20, 125, 165, 100))
        self.autofocus_checkbox.setObjectName("autofocus_checkbox")
        self.autofocus_checkbox.setStyleSheet(css)
        self.autofocus_checkbox.setFont(font2)
        self.autofocus_checkbox.setChecked(config.AUTO_FOCUS)
        self.autofocus_checkbox.stateChanged.connect(config.change_autofocus)


        # "Prev" Button
        self.button_capture_prev = QtWidgets.QPushButton(self.frame)
        self.button_capture_prev.setText("<--")
        self.button_capture_prev.setGeometry(QtCore.QRect(130, 150, 50, 50))
        self.button_capture_prev.setStyleSheet(css)
        self.button_capture_prev.setFont(QFont('D2Coding', 14, QFont.Bold))
        self.button_capture_prev.clicked.connect(self.do_PrevSide)

        # "Next" Button
        self.button_capture_next = QtWidgets.QPushButton(self.frame)
        self.button_capture_next.setGeometry(QtCore.QRect(290, 150, 50, 50))
        self.button_capture_next.setObjectName("button_capture_next")
        self.button_capture_next.setStyleSheet(css)
        self.button_capture_next.setFont(QFont('D2Coding', 14, QFont.Bold))
        self.button_capture_next.clicked.connect(self.do_NextSide)

        # Side Label
        self.side_label = QtWidgets.QLabel(self.frame)
        self.side_label.setGeometry(QtCore.QRect(190, 140, 90, 70))
        self.side_label.setText("Side 1:\n" + config.SIDE_NAMES[0])
        self.side_label.setFont(QFont('D2Coding', 13, QFont.DemiBold))
        self.side_label.setStyleSheet("QLabel { border: 2px solid blue } ")
        self.side_label.setAlignment(QtCore.Qt.AlignCenter)

        # Vertical layout widget for "Start test" and 2 hboxes containing result button lines
        # Also contains 2 horizontal
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 331, 160))  # x, y, w, h
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
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

        """
        # Invisible label
        self.label_invisible = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_invisible.setFixedSize(20, 20)
        self.verticalLayout.addWidget(self.label_invisible)
        """

        # "Show Result" Label
        # self.label_show_results = QtWidgets.QLabel("Show Results", self.verticalLayoutWidget)
        self.label_show_results = QtWidgets.QLabel("이전 결과:", self.frame)
        self.label_show_results.setObjectName("label_show_result")
        self.label_show_results.setFont(QFont('Malgun Gothic', 14))
        self.label_show_results.setStyleSheet(css)
        # self.verticalLayout.addWidget(self.label_show_results)

        # Results device number label
        self.label_results_device_number = QtWidgets.QLabel(self.frame)
        self.label_results_device_number.setAlignment(QtCore.Qt.AlignCenter)
        self.label_results_device_number.setFont(QFont('D2Coding', 11, QFont.DemiBold))
        self.label_results_device_number.setStyleSheet("QLabel { border: 1px solid black } ")

        # Prev result button
        self.button_prev_result = QtWidgets.QPushButton("<--", self.frame)
        self.button_prev_result.setStyleSheet(css)
        self.button_prev_result.setFont(QFont('D2Coding', 13, QFont.Bold))
        self.button_prev_result.clicked.connect(self.do_PrevResults)

        # Change result device number button
        self.button_change_device_number = QtWidgets.QPushButton("Change", self.frame)
        self.button_change_device_number.setStyleSheet(css)
        self.button_change_device_number.setFont(font2)
        self.button_change_device_number.clicked.connect(self.change_device_number)

        # Next result button
        self.button_next_result = QtWidgets.QPushButton("-->", self.frame)
        self.button_next_result.setStyleSheet(css)
        self.button_next_result.setFont(QFont('D2Coding', 13, QFont.Bold))
        self.button_next_result.clicked.connect(self.do_NextResults)

        # Hbox for "Results" label, devno label, change devno buttons
        hbox_devno_results = QtWidgets.QHBoxLayout()
        hbox_devno_results.addWidget(self.label_show_results)
        hbox_devno_results.addWidget(self.label_results_device_number)
        hbox_devno_results.addWidget(self.button_prev_result)
        hbox_devno_results.addWidget(self.button_change_device_number)
        hbox_devno_results.addWidget(self.button_next_result)
        hbox_devno_results.setSpacing(8)

        self.verticalLayout.addLayout(hbox_devno_results)

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
        hbox_text_image_result_buttons = QtWidgets.QHBoxLayout()
        hbox_text_image_result_buttons.addWidget(self.button_text_result)
        hbox_text_image_result_buttons.addWidget(self.button_images_result)
        # hbox.addStretch(1)

        self.verticalLayout.addLayout(hbox_text_image_result_buttons)

        #self.label_show_results.setSizePolicy(sizePolicy)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.label_show_results.sizePolicy().hasHeightForWidth())

        self.graphicsView = QtWidgets.QLabel(self.widget)
        self.graphicsView.setGeometry(QtCore.QRect(370, 60, 401, 391))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setText("Cannot load the image, press the Capture button")
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
        self.update_buttons_and_labels()

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        #if not config.DEBUG_STAGE_ABSENT:
            #config.initialize_machine()

    def update_buttons_and_labels(self):
        if self.resultsDeviceNo <= 1:
            self.button_prev_result.setDisabled(True)
        else:
            self.button_prev_result.setEnabled(True)

        if self.resultsDeviceNo >= self.curDeviceNo - 1:
            self.button_next_result.setDisabled(True)
        else:
            self.button_next_result.setEnabled(True)

        self.label_results_device_number.setText('{:04}'.format(self.resultsDeviceNo))
        self.label_device_number.setText('{:04}'.format(self.curDeviceNo))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_test_stage.setText(_translate("MainWindow", "Test Stage"))
        self.button_start_test.setText(_translate("MainWindow", "Start Test"))
        self.button_capture.setText(_translate("MainWindow", "Capture"))
        self.button_capture_next.setText(_translate("MainWindow", "-->"))
        self.home.setText(_translate("MainWindow", "Home"))

    def do_Home(self):
        print("##-Return Home Stage")
        self.mainUI.show()
        self.MainWindow.close()

    def get_device_number(self):
        resultspath_relative = "../res" + "/" + self.deviceName + "/result"
        try:
            self.result_directories = os.listdir(resultspath_relative)
        except:
            return 1
        return int(self.result_directories[-1].split('_')[0]) + 1

    """
    def setDeviceNum(self):
        self.deviceBox.do_UI()
        self.deviceName = self.deviceBox.getValue()
        self.sideBox.do_UI()
        self.sideName = self.sideBox.getValue()
        path = self.absPath + self.deviceName + '/' + self.sideName
        print('##-PATH : ' + path)
        """

    # "Capture" Button method
    def img_capture(self):
        print('##-CAPTURE BUTTON PRESSED')

        self.ROI = roi_unit.readROI(os.path.join(self.absPath, self.deviceName, 'locationInfo.txt'),
                                    config.WINDOW_RATIO)
        side = 'side' + str(self.sideNum)
        if side not in self.ROI:
            print("No screws on " + side)
            return
        print(self.ROI)

        predictPath = os.path.join(self.absPath, self.deviceName, 'predict')
        config.makeDir(predictPath)
        pOImagePath = os.path.join(predictPath, 'images')
        config.makeDir(pOImagePath)
        pCImagePath = os.path.join(predictPath, 'imagesCanny')
        config.makeDir(pCImagePath)

        print(self.ROI[side])
        self.img = image_process.test_image_capture(self.ROI[side], pOImagePath, pCImagePath, self.sideNum)
        cv2.imwrite(predictPath + '/' + side + '.jpg', self.img)
        self.imgview = QImage(self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.graphicsView.setPixmap(QPixmap.fromImage(self.imgview))

    def do_NextSide(self):
        self.cameraxyinputbox = cameraxy_inputbox.cameraXYInputbox(self.deviceName)
        self.cameraxyinputbox.searchDevice()

        print("##-NEXT BUTTON CLICKED")
        self.cameraNum = (self.cameraNum + 1) % config.CAMERA_NUMBER  # CAMERA CHANGE
        self.sideNum = (self.sideNum) % 5 + 1
        side = 'side' + str(self.sideNum)
        print("##-CLIKED THE NEXT BUTTON :" + side)
        if not config.DEBUG_STAGE_ABSENT:
            if self.sideNum == 4:
                config.rotate_machine_with_degree(_x_value=450000, _y_value=int(self.cameraxyinputbox.lineEdits[2].text()))
            elif self.sideNum == 1:
                config.rotate_machine_with_degree(_x_value=1,
                                                  _y_value=int(self.cameraxyinputbox.lineEdits[2].text()))
           # elif self.sideNum < 3: # UNTESTED
           #     config.rotate_machine_with_degree(_x_value=1, _y_value=1)
        self.side_label.setText("Side " + str(self.sideNum) + ":\n" + config.SIDE_NAMES[self.sideNum - 1])

    def do_PrevSide(self):
        self.cameraxyinputbox = cameraxy_inputbox.cameraXYInputbox(self.deviceName)
        self.cameraxyinputbox.searchDevice()

        self.cameraNum = (self.cameraNum - 1) % config.CAMERA_NUMBER  # CAMERA CHANGE
        self.sideNum = (self.sideNum - 2) % 5 + 1
        side = 'side' + str(self.sideNum)
        print("##-CLIKED THE NEXT BUTTON :" + side)
        if not config.DEBUG_STAGE_ABSENT:
            if self.sideNum == 3:
                config.rotate_machine_with_degree(_x_value=1, _y_value=int(self.cameraxyinputbox.lineEdits[2].text()))
            elif self.sideNum == 5:
                config.rotate_machine_with_degree(_x_value=450000,
                                                  _y_value=int(self.cameraxyinputbox.lineEdits[2].text()))
        self.side_label.setText("Side " + str(self.sideNum) + ":\n" + config.SIDE_NAMES[self.sideNum - 1])

    def do_PrevResults(self):
        self.resultsDeviceNo -= 1
        self.update_buttons_and_labels()

    def do_NextResults(self):
        self.resultsDeviceNo += 1
        self.update_buttons_and_labels()

    def change_device_number(self):
        b = QtWidgets.QInputDialog.getText(self.MainWindow, "Device Number", "Enter device number:")
        try:
            t = int(b[0])
            if 1 <= t <= self.curDeviceNo - 1:
                self.resultsDeviceNo = t
                self.update_buttons_and_labels()
            else:
                print("Incorrect number entered!")
        except:
            print("Incorrect number entered!")


    # "Start Test" button method
    def do_startTest(self):
        print("##-TEST BUTTON CLICKED")
        startTime = datetime.datetime.now()
        print(startTime)
        self.startEndTimes = [startTime]

        path = os.path.join(self.absPath, self.deviceName)
        img_list = os.listdir(path + '/predict')
        classes = os.listdir(path + '/t_images')
        self.correctList = [[0, 0] for _ in range(5)]

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

        summary_of_result = {'total': {'CORRECT': 0, 'INCORRECT': 0}}
        dict_of_result_values = []

        for result in results:
            image = result['imageName']
            sideNo = int(result['imageName'][4])
            print('#Predict Result[{}]'.format(image))
            matchRates = result['results']
            try:
                camera_position, origin_class, predicted_class, maxmimum_score, isCorrect = getResult(image, matchRates)
            except Exception as e:
                print(e)

            dict_of_result_values.append({
                'image name': image,
                'camera position': camera_position,
                'class': origin_class,
                'predicted': predicted_class,
                'maximum score': str(maxmimum_score),
                'result': isCorrect
            })

            print('result:', isCorrect, end='\n')

            if camera_position not in summary_of_result:
                summary_of_result[camera_position] = {'CORRECT': 0, 'INCORRECT': 0}
            if origin_class not in summary_of_result['total']:
                summary_of_result['total'][origin_class] = {'CORRECT': 0, 'INCORRECT': 0}

            summary_of_result[camera_position][isCorrect] += 1
            summary_of_result['total'][isCorrect] += 1
            summary_of_result['total'][origin_class][isCorrect] += 1
            start, end, side = self.getArea(image)

            if isCorrect == 'CORRECT':
                cv2.rectangle(self.smallImages[side], start, end, config.GREEN, 1)
            else:
                cv2.rectangle(self.smallImages[side], start, end, config.RED, 1)

        print("Test finished")
        endTime = datetime.datetime.now()
        print(endTime)
        self.startEndTimes.append(endTime)

        self.graphicsView.setText("RESULT DATA")
        keys = self.smallImages.keys()
        result_path = os.path.join(self.absPath, self.deviceName, 'result')
        config.makeDir(result_path)

        '''
        print('Sides:', keys)
        for key in keys:
            cv2.imwrite(result_path + '/' + key + '.jpg', self.smallImages[key])
        '''

        self.record_result_data_on_json(startTime=str(startTime),
                                        endTime=str(endTime),
                                        result_dict_values=dict_of_result_values,
                                        summary_of_result=summary_of_result,
                                        result_path=result_path)

        self.curDeviceNo += 1
        self.resultsDeviceNo = self.curDeviceNo - 1

        self.update_buttons_and_labels()
        self.showImagesResult()

    def record_result_data_on_json(self, startTime, endTime, result_dict_values, summary_of_result, result_path):
        # Create result file path
        num_of_dirs = len(os.listdir(result_path)) + 1
        created_date = datetime.datetime.now().date()
        created_time = datetime.datetime.now().time()

        dir_path_to_write_result = os.path.join(result_path, '{:0>4}_RESULT_{}_{:0>2}-{:0>2}-{:0>2}'.format(num_of_dirs,
                                                                                                            created_date,
                                                                                                            created_time.hour,
                                                                                                            created_time.minute,
                                                                                                            created_time.second))
        config.makeDir(dir_path_to_write_result)
        self.result_directories.append(dir_path_to_write_result.split('\\')[-1])

        # Write result image files
        keys = self.smallImages.keys()
        for key in keys:
            cv2.imwrite(dir_path_to_write_result + '/' + key + '.jpg', self.smallImages[key])

        # Fill result data
        data = {
            'START': startTime,
            'END': endTime,
            'SUMMARY': summary_of_result,
            'VALUES': result_dict_values
        }
        print('#FILE WRITE', data)
        json_file_path_to_write_result = os.path.join(dir_path_to_write_result, 'RESULT.json')

        with open(json_file_path_to_write_result, 'w') as outfile:
            json.dump(data, outfile, indent=4, separators=(',', ': '))

    def showTextResult(self):
        print("##-SHOW TEXT RESULT BUTTON CLICKED")
        self.resultTextWidget = result_text_widget.resultTextWidget(self.deviceName,
                                                                    self.result_directories[self.resultsDeviceNo - 1])

    def showImagesResult(self):
        print("##-SHOW IMAGES RESULT BUTTON CLICKED")
        self.resultImagesWidget = result_images_widget_grid.resultImagesWidget(self.deviceName, self.result_directories[
            self.resultsDeviceNo - 1])

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
    image_class = temp[1]

    camera_position = config.SIDE_NAMES[int(temp[0][-1]) - 1]
    correct_class = temp[1] + '_' + 'cor'

    print(result_arr)
    result_sum_dict = {}

    for result_pair in result_arr:
        # temp = result_pair[0].decode('ascii').split(' ')
        temp = result_pair[0].split(' ')
        result_class_name = temp[0] + '_' + temp[1]
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
        return camera_position, image_class, maximum_class, maximum_score, 'CORRECT'
    else:
        return camera_position, image_class, maximum_class, maximum_score, 'INCORRECT'


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, "escrow")
    MainWindow.show()
    sys.exit(app.exec_())
