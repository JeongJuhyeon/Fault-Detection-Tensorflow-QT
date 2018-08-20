# Contains the functions and logic used  after clicking on "Correct Capture" in training stage

import copy
import os
import pathlib

import cv2
from PyQt5.QtWidgets import QMessageBox

import config
import correctincorrect_dialog
import crop_image
import roiactiondialog
import roiobjectinputdialog
from config import cameraConfig

img_path_list = []
selected_rois = []


def readfile():
    f = open("./../data.txt", 'r')
    lines = f.readlines()
    f.close()
    dic = {};
    for line in lines:
        left, right = line.split(':')
        temp = list(right.split(','))
        for i in range(len(temp)):
            temp[i] = temp[i].strip()
        dic[left] = temp
    return dic


def get_image_from_camera(sideNum, size_conf):
    cameraConfigObject = cameraConfig()
    if sideNum == 1 or sideNum == 4:
        cameraNum = cameraConfigObject.get_camera_number('LEFT')
    elif sideNum == 2 or sideNum == 5:
        cameraNum = cameraConfigObject.get_camera_number('RIGHT')
    else:
        cameraNum = cameraConfigObject.get_camera_number('CENTER')

    cap = cv2.VideoCapture(cameraNum)
    cap.set(3, int(size_conf['width']))
    cap.set(4, int(size_conf['height']))

    if config.AUTO_FOCUS:
        while True:
            ret, img = cap.read()
            cv2.imshow('Video', img)
            if cv2.waitKey(10) & 0xFF == 27:
                break
    else:
        ret, img = cap.read()

    cap.release()
    cv2.destroyAllWindows()
    print('# GET IMAGE FROM CAMERA#{}, AUTO_FOCUS: {}'.format(cameraNum, config.AUTO_FOCUS))
    return img


def convert_coord(coord, size_conf):
    widthRatio = size_conf['width_ratio']
    heightRatio = size_conf['height_ratio']
    newCoord = (int(coord[0] * widthRatio),
                int(coord[1] * heightRatio),
                int((coord[0] + coord[2]) * widthRatio),
                int((coord[1] + coord[3]) * heightRatio))
    return newCoord


def recapture_image(device_dir_path, current_side, sideNum):
    print("INTO RECAPTURE")
    side_dir_path = device_dir_path + '/' + current_side

    # Creating dialog objects used when saving
    savedialog = QMessageBox()
    savedialog.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Close)
    savedialog.setDefaultButton(QMessageBox.Save)
    savedialog.setText("Save recapture, Discard recapture, Quit?")

    correctdialog = correctincorrect_dialog.correctIncorrectDialog()

    # Reading locations of existing ROI's used when matching with selected rectangle
    correct_locs = []
    file = open(device_dir_path + '/' + 'locationInfo.txt', "r")
    locationInfolines = []
    for line in file:
        correct_locs.append([int(x) for x in line.split("_")[0:4]])
        locationInfolines.append(line)

    # Original picture is later cropped according to ROI
    original_image = get_image_from_camera(sideNum, size_conf=config.WINDOW_SIZE)
    cv2.imwrite(device_dir_path + "/Origin.jpg", original_image)
    origin_path = device_dir_path + "/Origin.jpg"

    # Image used to select ROI's on
    img = get_image_from_camera(sideNum, size_conf=config.TESTWINDOW_SIZE)

    # Apparently needed
    fromCenter = False

    # Creating frequency dict used for file names when making new images
    image_folder_names = os.listdir(side_dir_path)
    print(image_folder_names)
    class_correct_incorrect_dict = {}
    for folder in image_folder_names:
        class_and_is_correct = folder.split('_')[1] + folder.split('_')[-1]
        if class_and_is_correct in class_correct_incorrect_dict:
            class_correct_incorrect_dict[class_and_is_correct] += 1
        else:
            class_correct_incorrect_dict[class_and_is_correct] = 1

    print("##-RECAPTURE SETUP COMPLETE")
    while True:
        # Drawing ROI's
        if len(selected_rois) > 0:
            for rect in selected_rois:
                if rect[5] == current_side:
                    if rect[4]:
                        cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
                    else:
                        cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 1)

        # Get ROI
        selected_roi = cv2.selectROI("Select ROI", img, fromCenter)

        # Set ROI to closest existing ROI
        closest_dist = 99999999
        closest_idx = -1
        for i, rect in enumerate(correct_locs):
            dist = abs(rect[0] - selected_roi[0]) + abs(rect[1] - selected_roi[1])
            if dist < closest_dist:
                closest_dist = dist
                closest_rect = rect
                closest_idx = i

        selected_roi = list(closest_rect)

        # Asking what the user wants to do
        button_pressed = savedialog.exec()

        # If save:
        if button_pressed == QMessageBox.Save:
            class_name = locationInfolines[closest_idx].split("_")[-2]
            side_and_class_prefix = current_side + "_" + class_name

            # Create file names, paths based on correct/incorrect
            isIncorrect = correctdialog.exec()
            # Correct
            if isIncorrect == 0:
                unique_object_name = side_and_class_prefix + '_' + str(class_correct_incorrect_dict[class_name + 'cor'])
                class_correct_incorrect_dict[class_name + 'cor'] += 1
                file_dir = side_dir_path + '/' + unique_object_name + '_cor'
                file_path_including_name = file_dir + '/' + unique_object_name
            # Incorrect
            else:
                unique_object_name = side_and_class_prefix + '_' + str(
                    class_correct_incorrect_dict[class_name + 'incor'])
                class_correct_incorrect_dict[class_name + 'incor'] += 1
                file_dir = side_dir_path + '/' + unique_object_name + '_incor'
                file_path_including_name = file_dir + '/' + unique_object_name

            x, y, w, h = closest_rect[0], closest_rect[1], closest_rect[2], closest_rect[3]

            # Create directory and image
            coord = convert_coord(closest_rect, size_conf=config.WINDOW_RATIO)
            config.makeDir(file_dir)
            crop_image.reduce_and_save_image(origin_image=origin_path,
                                             crop_coords=coord,
                                             saved_base_path=file_path_including_name)
        # Else if close:
        elif button_pressed == QMessageBox.Close:
            cv2.destroyAllWindows()
            file.close()
            return selected_rois


# Used in training stage
def image_capture(dir_path, current_side, sideNum, correct_ROIs):
    if correct_ROIs:
        file = open(dir_path + '/' + 'locationInfo.txt', "a+")
    else:
        correct_locs = []
        file = open(dir_path + '/' + 'locationInfo.txt', "r")
        for line in file:
            correct_locs.append([int(x) for x in line.split("_")[0:4]])

    # Creating dialog objects for later use
    actiondialog = roiactiondialog.ROIActionDialog()
    objectinputbox = roiobjectinputdialog.ROIobjectInputDialog()

    # Original picture is later cropped according to ROI
    original_image = get_image_from_camera(sideNum, size_conf=config.WINDOW_SIZE)
    cv2.imwrite(dir_path + "/Origin.jpg", original_image)
    origin_path = dir_path + "/Origin.jpg"

    # Image used to select ROI's on
    img = get_image_from_camera(sideNum, size_conf=config.TESTWINDOW_SIZE)
    fromCenter = False
    dirPath = dir_path + '/' + current_side
    obj_name_frequencies = {}
    first_img = copy.copy(img)
    file_name_idx = 1

    """
    selected_img is a list of rectangles
    r is the currently selected region

    Logic:

    1. Draw everything
    2. Take rectangle, wait until enter (cv2.selectROI only ends when you've pressed enter)
    3. Selection box pops up (after the enter) 
    """

    while True:
        # Drawing ROI's
        if len(selected_rois) > 0:
            for rect in selected_rois:
                if rect[5] == current_side:
                    if rect[4]:
                        cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
                    else:
                        cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 1)

        # Get ROI
        r = cv2.selectROI("Select ROI", img, fromCenter)

        # If incorrect, set ROI to closest correct ROI
        if not correct_ROIs and config.SELECT_CLOSEST_CORRECT_ROI_WHEN_SELECTING_INCORRECT_ROI:
            closest_dist = 99999999
            for rect in correct_locs:
                dist = abs(rect[0] - r[0]) + abs(rect[1] - r[1])
                if dist < closest_dist:
                    closest_dist = dist
                    closest_rect = rect
            r = list(closest_rect)




        # Asking what the user wants to do
        button_pressed = actiondialog.exec()

        # imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

        # Giving a name to the ROI and saving it
        if button_pressed == 0x00000800:
            obj_name = objectinputbox.itemNames[objectinputbox.exec()]
            if obj_name in obj_name_frequencies:
                obj_name_frequencies[obj_name] += 1
            else:
                obj_name_frequencies[obj_name] = 0
            x, y, w, h = r[0], r[1], r[2], r[3]
            dir_name = current_side + '_' + obj_name + '_' + str(obj_name_frequencies[obj_name])
            if correct_ROIs:
                dir_name += '_cor'
            else:
                dir_name += '_incor'
            temp_path = dirPath + '/' + dir_name
            file_name = temp_path + '/' + current_side + '_' + obj_name

            config.makeDir(temp_path)
            # cv2.imwrite(temp_path + '/' + filename, imCrop)
            coord = convert_coord(r, size_conf=config.WINDOW_RATIO)
            crop_image.reduce_and_save_image(origin_image=origin_path,
                                             crop_coords=coord,
                                             saved_base_path=file_name + '_' + str(obj_name_frequencies[obj_name]))
            img_path_list.append(temp_path)
            selected_rois.append([x, y, w, h, correct_ROIs, current_side])
            if correct_ROIs:
                file.write(
                    "%s_%s_%s_%s_%s_%s_%s\n" % (x, y, w, h, current_side, obj_name, obj_name_frequencies[obj_name]))
                file.flush()
                print("##-COMPLETE SAVE FILE : " + obj_name)
        # Deleting last ROI
        elif button_pressed == 0x00800000:
            _size = len(img_path_list)
            if _size > 0:
                print("##-IMAGE DELETE")
                _path = img_path_list.pop()
                print(_path)
                config.delete_folder(pathlib.Path(_path))
                # os.remove()
                selected_rois.pop()
                img = copy.copy(first_img)  # before img
                file_name_idx -= 1
            else:
                print("##-IMAGE DELETE - FAILED(No File)")
        # Exiting
        elif button_pressed == 0x00200000:
            print("##-IMAGE PROCESS COMPLETE")
            cv2.destroyAllWindows()
            file.close()
            return selected_rois

# Used in test stage
def test_image_capture(infos, O_path, C_path, sideNum):
    print('## Test image capture:', O_path, C_path)
    img = get_image_from_camera(sideNum, config.WINDOW_SIZE)
    number = 0

    noise_min = config.NOISE_TEST['min']
    noise_max = config.NOISE_TEST['max']

    for info in infos:
        cropped = img[info.startY:info.endY, info.startX:info.endX]
        image_path = O_path + '/' + info.side + '_' + info.element + '_' + info.number + '_' + str(number) + '.jpg'
        cv2.imwrite(image_path, cropped)
        canny = cv2.Canny(cropped, noise_min, noise_max)
        image_path = C_path + '/' + info.side + '_' + info.element + '_' + info.number + '_' + str(number) + '.jpg'
        cv2.imwrite(image_path, canny)
        number += 1

    return cv2.resize(img, (config.TESTWINDOW_SIZE['width'], config.TESTWINDOW_SIZE['height']))


def checkclicked(checkbox, dirPath, imCrop, x1, x2, y1, y2, file, side):
    while True:
        if (checkbox.flag):
            break
    print(checkbox.getValue())
    objName = checkbox.getValue()
    filename = objName + ".jpg"
    temppath = dirPath + '/' + objName
    if not os.path.isdir(temppath):
        print('##-DIRECTORY CREATE : ' + temppath)
        os.mkdir(temppath)
    cv2.imwrite(temppath + '/' + filename, imCrop)
    # img_path_list.append(temppath+'/'+filename)
    # selected_img.append([x1,y1,x2,y2])
    file.write("%s_%s_%s_%s_%s_%s\n" % (x1, y1, x2, y2, side, objName))
    file.flush()
    print("##-COMPLETE SAVE FILE : " + objName)


def showROI(selectROI, current_side):
    sideNum = int(current_side[-1])
    cameraConfigObject = cameraConfig()
    if sideNum == 1 or sideNum == 4:
        cameraNum = cameraConfigObject.get_camera_number('LEFT')
    elif sideNum == 2 or sideNum == 5:
        cameraNum = cameraConfigObject.get_camera_number('RIGHT')
    else:
        cameraNum = cameraConfigObject.get_camera_number('CENTER')

    capture = cv2.VideoCapture(cameraNum)
    capture.set(3, int(config.TESTWINDOW_SIZE['width']))
    capture.set(4, int(config.TESTWINDOW_SIZE['height']))
    while True:
        ret, frame = capture.read()
        if len(selected_rois) > 0:
            for rect in (selected_rois):
                if rect[5] == current_side:
                    if (rect[4]):
                        cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
                    else:
                        cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 1)
        if not ret:
            return

        cv2.imshow('Show ROI', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break;

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image_capture()
