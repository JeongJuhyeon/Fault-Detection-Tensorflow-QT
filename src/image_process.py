import cv2, os, pathlib
from src import crop_image, inputBox, config
import copy

img_path_list = []
selected_img = []

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

def get_image_from_camera(cameraNum, size_conf) :
    cap = cv2.VideoCapture(cameraNum)
    cap.set(3, int(size_conf['width']))
    cap.set(4, int(size_conf['height']))

    if config.AUTO_FOCUS:
        while True:
            ret, img = cap.read()
            cv2.imshow('Video', img)
            if cv2.waitKey(10) & 0xFF == 27:
                break
    else :
        ret, img = cap.read()

    cap.release()
    cv2.destroyAllWindows()
    print('# GET IMAGE FROM CAMERA#{}, AUTO_FOCUS: {}'.format(cameraNum, config.AUTO_FOCUS))
    return img

def convert_coord(coord, size_conf):
    widthRatio = size_conf['width_ratio']
    heightRatio = size_conf['height_ratio']
    newCoord = ( int(coord[0] * widthRatio),
                 int(coord[1] * heightRatio),
                 int((coord[0] + coord[2]) * widthRatio),
                 int((coord[1] + coord[3]) * heightRatio))
    return newCoord

def image_capture(dir_path, current_side, cameraNum, do_write_ROI):
    if do_write_ROI : file = open(dir_path + '/' + 'locationInfo.txt', "a+")
    inputbox = inputBox.App("Enter the Object Name")

    original_image = get_image_from_camera(cameraNum, size_conf=config.WINDOW_SIZE)
    cv2.imwrite(dir_path + "/Origin.jpg", original_image)
    origin_path = dir_path + "/Origin.jpg"

    img = get_image_from_camera(cameraNum, size_conf=config.TESTWINDOW_SIZE)
    fromCenter = False
    dirPath = dir_path + '/' + current_side
    elements = {}
    first_img = copy.copy(img)
    fileName_idx = 1

    while True:
        if (len(selected_img) > 0):
            for rect in (selected_img):
                if rect[4]:
                    cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
                else:
                    cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 3)
        r = cv2.selectROI("Select ROI", img, fromCenter)
        while True:
            # imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            if cv2.waitKey(1) & 0xFF == ord('q'):
                inputbox.do_UI()
                objName = inputbox.getValue()
                if objName in elements : elements[objName] += 1
                else : elements[objName] = 0
                x = r[0]
                y = r[1]
                w = r[2]
                h = r[3]
                dirName = current_side + '_' + objName + '_' + str(elements[objName])
                if do_write_ROI == True : dirName += '_cor'
                else : dirName += '_incor'
                temppath = dirPath + '/' + dirName

                fileName = temppath + '/' + current_side + '_' + objName
                config.makeDir(temppath)
                # cv2.imwrite(temppath + '/' + filename, imCrop)
                coord = convert_coord(r, size_conf=config.WINDOW_RATIO)
                crop_image.reduce_and_save_image(origin_image=origin_path,
                                                 crop_coords=coord,
                                                 saved_base_path=fileName + '_' + str(elements[objName]))
                img_path_list.append(temppath)
                selected_img.append([x, y, w, h, do_write_ROI])
                if do_write_ROI :
                    file.write("%s_%s_%s_%s_%s_%s_%s\n" % (x, y, w, h, current_side, objName, elements[objName]))
                    file.flush()
                    print("##-COMPLETE SAVE FILE : " + objName)
                break
            elif cv2.waitKey(1) & 0xFF == ord('d'):
                _size = len(img_path_list)
                if(_size > 0):
                    print("##-IMAGE DELETE")
                    _path = img_path_list.pop()
                    print(_path)
                    config.delete_folder(pathlib.Path(_path))
                    # os.remove()
                    selected_img.pop()
                    img = copy.copy(first_img) #before img
                    fileName_idx -= 1
                else:
                    print("##-IMAGE DELETE - FAILED(No File)")
                break
            elif cv2.waitKey(1) & 0xFF == ord('s'):
                print("##-IMAGE PROCESS COMPELTE")
                cv2.destroyAllWindows()
                if(do_write_ROI):
                    file.close()
                return selected_img

def test_image_capture(infos, O_path, C_path, cameraNum):
    print('## Test image capture:', O_path, C_path)
    img = get_image_from_camera(cameraNum, config.WINDOW_SIZE)
    number = 0

    noise_min = config.NOISE_TEST['min']
    noise_max = config.NOISE_TEST['max']

    for info in infos :
        cropped = img[info.startY:info.endY, info.startX:info.endX]
        image_path = O_path + '/' + info.side + '_' + info.element + '_' + info.number + '_' + str(number) + '.jpg'
        cv2.imwrite(image_path, cropped)
        canny = cv2.Canny(cropped, noise_min, noise_max)
        image_path = C_path + '/' + info.side + '_' + info.element + '_' + info.number + '_' + str(number) + '.jpg'
        cv2.imwrite(image_path, canny)
        number +=1

    return cv2.resize(img, (config.TESTWINDOW_SIZE['width'], config.TESTWINDOW_SIZE['height']))

def checkclicked(checkbox, dirPath, imCrop, x1, x2, y1, y2, file, side):
    while True:
        if(checkbox.flag):
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

def showROI(selectROI, cameraNum):
    capture = cv2.VideoCapture(cameraNum)
    capture.set(3, int(config.TESTWINDOW_SIZE['width']))
    capture.set(4, int(config.TESTWINDOW_SIZE['height']))
    while True:
        ret, frame = capture.read()
        if (len(selected_img) > 0):
            for rect in (selected_img):
                if(rect[4]):
                    cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
                else:
                    cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 3)
        if not ret:
            return

        cv2.imshow('Show ROI', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break;

    capture.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    image_capture()
