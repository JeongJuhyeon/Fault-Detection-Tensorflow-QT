# Contains the functions and logic used  after clicking on "Correct Capture" in training stage

import copy
import os
import pathlib

import cv2
from PyQt5.QtWidgets import QMessageBox
from collections import namedtuple

import config
import correctincorrect_dialog
import crop_image
import roiactiondialog
import roiobjectinputdialog
from config import cameraConfig

img_path_list = []


def readfile():
    f = open("./../data.txt", 'r')
    lines = f.readlines()
    f.close()
    dic = {}
    for line in lines:
        left, right = line.split(':')
        temp = list(right.split(','))
        for i in range(len(temp)):
            temp[i] = temp[i].strip()
        dic[left] = temp
    return dic


def get_rect_list_from_locationinfo(device_dir_path):
    try:
        file = open(device_dir_path + '/' + 'locationInfo.txt', "r")
    except FileNotFoundError:
        return []

    selected_rois_t = []

    for line in file:
        a = []
        for i in line.split('_')[:4]:
            a.append(int(i))
        a.append(True)
        a.append(line.split('_')[4])
        selected_rois_t.append(a)

    file.close()
    return selected_rois_t


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

    # Make list of rois to display
    selected_rois_to_draw = get_rect_list_from_locationinfo(device_dir_path)
    if len(selected_rois_to_draw) == 0:
        print("No existing ROI's found! Nothing to recapture.")
        return

    # Creating dialog objects used when saving
    savedialog = QMessageBox()
    savedialog.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Apply)
    savedialog.setDefaultButton(QMessageBox.Save)
    savedialog.setText("Save recapture, Cancel, Quit?")
    savedialog.button(QMessageBox.Apply).setText("Quit")

    correctdialog = correctincorrect_dialog.correctIncorrectDialog()

    # Reading locations of existing ROI's used when matching with selected rectangle
    correct_locs = []
    file = open(device_dir_path + '/' + 'locationInfo.txt', "r")
    locationInfolines = []
    for line in file:
        if line.split('_')[4] == current_side:
            correct_locs.append([int(x) for x in line.split("_")[0:4]])
            locationInfolines.append(line)
    file.close()

    # Original picture is later cropped according to ROI
    original_image = get_image_from_camera(sideNum, size_conf=config.WINDOW_SIZE)
    cv2.imwrite(device_dir_path + "/Origin.jpg", original_image)
    # Image used to select ROI's on
    img = get_image_from_camera(sideNum, size_conf=config.TESTWINDOW_SIZE)

    # Creating frequency dict used for file names when making new images
    image_folder_names = os.listdir(side_dir_path)
    print(image_folder_names)
    class_correct_incorrect_frequencies = {}
    for folder in image_folder_names:
        class_and_is_correct = folder.split('_')[1] + folder.split('_')[-1]
        if class_and_is_correct in class_correct_incorrect_frequencies:
            class_correct_incorrect_frequencies[class_and_is_correct] += 1
        else:
            class_correct_incorrect_frequencies[class_and_is_correct] = 1

    print("##-RECAPTURE SETUP COMPLETE")

    while True:
        # Drawing ROI's
        if len(selected_rois_to_draw) > 0:
            draw_rois(current_side, img, selected_rois_to_draw)

        # Get ROI
        selected_roi = cv2.selectROI("Select ROI", img, False)

        if selected_roi[2] == 0:
            savedialog.button(QMessageBox.Save).setDisabled(True)
        else:
            savedialog.button(QMessageBox.Save).setEnabled(True)
            savedialog.setDefaultButton(QMessageBox.Save)

        # Set ROI to closest existing ROI
        closest_dist = 99999999
        closest_idx = -1
        for i, rect in enumerate(correct_locs):
            dist = abs(rect[0] - selected_roi[0]) + abs(rect[1] - selected_roi[1])
            if dist < closest_dist:
                closest_dist = dist
                closest_rect = rect
                closest_idx = i

        # Asking what the user wants to do
        button_pressed = savedialog.exec()

        # If save:
        if button_pressed == QMessageBox.Save:
            class_name = locationInfolines[closest_idx].split("_")[-2]
            side_and_class_prefix = current_side + "_" + class_name

            # Create file names, paths, dictionary of existing images
            is_incorrect = correctdialog.exec()

            correctness_string = 'incor' if is_incorrect else 'cor'
            try:
                unique_object_name = side_and_class_prefix + '_' + str(
                    class_correct_incorrect_frequencies[class_name + correctness_string])
            except KeyError:
                unique_object_name = side_and_class_prefix + '_' + '0'
                class_correct_incorrect_frequencies[class_name + correctness_string] = 0
            class_correct_incorrect_frequencies[class_name + correctness_string] += 1
            file_directory = side_dir_path + '/' + unique_object_name + '_' + correctness_string
            file_path_including_name = file_directory + '/' + unique_object_name

            # Create directory and image
            coord = convert_coord(closest_rect, size_conf=config.WINDOW_RATIO)
            config.makeDir(file_directory)
            crop_image.reduce_and_save_image(origin_image=(device_dir_path + "/Origin.jpg"),
                                             crop_coords=coord,
                                             saved_base_path=file_path_including_name)
        # Else if close:
        elif button_pressed == QMessageBox.Apply:
            cv2.destroyAllWindows()
            file.close()
            return


def draw_rois(current_side, img, selected_rois_to_draw):
    for rect in selected_rois_to_draw:
        if rect[5] == current_side:
            if rect[4]:
                cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
            else:
                cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 1)


# Used in training stage
def image_capture(dir_path, current_side, sideNum, correct_ROIs):
    # Correct Capture button pressed
    if correct_ROIs:
        file = open(dir_path + '/' + 'locationInfo.txt', "a+")
    # Incorrect Capture button pressed
    else:
        correct_locs = []
        try:
            file = open(dir_path + '/' + 'locationInfo.txt', "r")
        except FileNotFoundError:
            print("No existing ROI's found! Can't capture incorrect areas.")
            return
        for line in file:
            if line.split('_')[4] == current_side:
                correct_locs.append([int(x) for x in line.split("_")[0:4]])
        file.close()
        if len(correct_locs) == 0:
            print("No existing ROI's found! Can't capture incorrect areas.")
            return

    selected_rois_to_draw = get_rect_list_from_locationinfo(dir_path)

    # Creating dialog objects for later use
    actiondialog = roiactiondialog.ROIActionDialog()
    objectinputbox = roiobjectinputdialog.ROIobjectInputDialog()

    # Original picture is later cropped according to ROI
    original_image = get_image_from_camera(sideNum, size_conf=config.WINDOW_SIZE)
    cv2.imwrite(dir_path + "/Origin.jpg", original_image)
    # Image used to select ROI's on
    img = get_image_from_camera(sideNum, size_conf=config.TESTWINDOW_SIZE)
    # Creating frequency dict used for file names when making new images
    class_frequencies = {}

    image_folder_names = os.listdir(dir_path + '/' + current_side)
    print(image_folder_names)
    for folder in image_folder_names:
        class_name = folder.split('_')[1]
        correct_folder = folder.split('_')[-1] == "cor"
        if correct_ROIs and correct_folder or (not correct_ROIs and not correct_folder):
            if class_name in class_frequencies:
                class_frequencies[class_name] += 1
            else:
                class_frequencies[class_name] = 0

    first_img = copy.copy(img)

    """
    selected_rois_to_draw is a list of rectangles
    r is the currently selected region

    Logic:

    1. Draw everything
    2. Take rectangle, wait until enter (cv2.selectROI only ends when you've pressed enter)
    3. Selection box pops up (after the enter) 
    """

    while True:
        # Drawing ROI's
        if len(selected_rois_to_draw) > 0:
            draw_rois(current_side, img, selected_rois_to_draw)

        # Get ROI
        r = cv2.selectROI("Select ROI", img, False)

        # If correct, if "fixed ROI size" is turned on, set to the given size
        if correct_ROIs and config.ROI_SIZE_FIXED:
            x, y, w, h = r[:4]
            Coords = namedtuple('Coords', 'x y')
            mid_point = Coords(round(x + w / 2), round(y + h / 2))
            x = max(mid_point.x - round(config.ROI_FIXED_WIDTH / 2), 0)
            y = max(mid_point.y - round(config.ROI_FIXED_HEIGHT / 2), 0)
            w = min(config.ROI_FIXED_WIDTH, config.WINDOW_SIZE['width'] - x)
            h = min(config.ROI_FIXED_HEIGHT, config.WINDOW_SIZE['height'] - y)
            r = list(r)
            r[:4] = (x, y, w, h)

        # If incorrect, set ROI to closest correct ROI
        if not correct_ROIs and config.SELECT_CLOSEST_CORRECT_ROI_WHEN_SELECTING_INCORRECT_ROI:
            closest_dist = 99999999
            for rect in correct_locs:
                dist = abs(rect[0] - r[0]) + abs(rect[1] - r[1])
                if dist < closest_dist:
                    closest_dist = dist
                    closest_rect = rect
            r = list(closest_rect)

        # Save button default. If no ROI is selected, disable the save button

        if r[2] == 0:
            actiondialog.button(QMessageBox.Save).setDisabled(True)
        else:
            actiondialog.button(QMessageBox.Save).setEnabled(True)
            actiondialog.setDefaultButton(QMessageBox.Save)

        # Asking what the user wants to do
        button_pressed = actiondialog.exec()

        # imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

        # Giving a name to the ROI and saving it
        if button_pressed == QMessageBox.Save:
            obj_name = objectinputbox.itemNames[objectinputbox.exec()]
            if obj_name in class_frequencies:
                class_frequencies[obj_name] += 1
            else:
                class_frequencies[obj_name] = 0
            x, y, w, h = r[:4]
            dir_name = current_side + '_' + obj_name + '_' + str(class_frequencies[obj_name])
            if correct_ROIs:
                dir_name += '_cor'
            else:
                dir_name += '_incor'
            temp_path = dir_path + '/' + current_side + '/' + dir_name
            file_name = temp_path + '/' + current_side + '_' + obj_name

            config.makeDir(temp_path)
            # cv2.imwrite(temp_path + '/' + filename, imCrop)
            coord = convert_coord(r, size_conf=config.WINDOW_RATIO)
            crop_image.reduce_and_save_image(origin_image=(dir_path + "/Origin.jpg"),
                                             crop_coords=coord,
                                             saved_base_path=file_name + '_' + str(class_frequencies[obj_name]))
            img_path_list.append(temp_path)
            selected_rois_to_draw.append([x, y, w, h, correct_ROIs, current_side])
            if correct_ROIs:
                file.write(
                    "%s_%s_%s_%s_%s_%s_%s\n" % (x, y, w, h, current_side, obj_name, class_frequencies[obj_name]))
                file.flush()
                print("##-COMPLETE SAVE FILE : " + obj_name)
        # Deleting last ROI
        elif button_pressed == QMessageBox.Discard:
            _size = len(img_path_list)
            if correct_ROIs and img_path_list[-1].split('_')[-1] == 'incor':
                print("Last saved incorrect ROI! Can't delete from correct capture mode!")
            elif not correct_ROIs and img_path_list[-1].split('_')[-1] == 'cor':
                print("Last saved correct ROI! Can't delete from incorrect capture mode!")
            elif _size > 0:
                print("##-IMAGE DELETE")
                _path = img_path_list.pop()
                print(_path)
                obj_name = _path.split('_')[-3]
                class_frequencies[obj_name] -= 1
                config.delete_folder(pathlib.Path(_path))
                # os.remove()
                selected_rois_to_draw.pop()
                img = copy.copy(first_img)  # before img
                if correct_ROIs:
                    file.close()
                    delete_last_line_from_roi_text_file(dir_path + '/' + 'locationInfo.txt')
                    file = open(dir_path + '/' + 'locationInfo.txt', "a+")
            else:
                print("##-IMAGE DELETE - FAILED(No File)")
        # Exiting
        elif button_pressed == QMessageBox.Apply:
            print("##-IMAGE PROCESS COMPLETE")
            cv2.destroyAllWindows()
            file.close()
            return selected_rois_to_draw


def delete_last_line_from_roi_text_file(roi_file_path):
    try:
        with open(roi_file_path, 'r+') as file:
            file.seek(0, os.SEEK_END)  # seek to end of file
            file_end = file.tell()  # get number of bytes in file
            i = 13  # A line has at least 13 characters
            while True:
                if file_end - i < 12:  # Only one line in ROI file
                    file.truncate(0)
                    break

                file.seek(file_end - i, os.SEEK_SET)  # go to end - i bytes
                c = file.read(1)
                if c == '\n':  # End of last line found
                    file.truncate(file_end - i + 1)
                    break
                i += 1
    except FileNotFoundError:
        print("ROI File not found, can't delete any lines.")


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


def showROI(device_dir_path, current_side):
    selected_rois_to_draw = get_rect_list_from_locationinfo(device_dir_path)
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
        if len(selected_rois_to_draw) > 0:
            for rect in selected_rois_to_draw:
                if rect[5] == current_side:
                    if rect[4]:
                        cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)
                    else:
                        cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 1)
        if not ret:
            return

        cv2.imshow('Show ROI', frame)

        try:
            k = chr(cv2.waitKey(25))
            break
        except:
            pass

        #if (cv2.waitKey(25) & 0xFF) == ord('q'):
        #    break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    g = 1
    # image_capture([], 'side1', )
