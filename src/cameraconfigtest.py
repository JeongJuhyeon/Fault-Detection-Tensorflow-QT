import os
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

a = "../res/a/b/c"
print(a.split('.')[0])
"""d = cameraConfig()
print(d.get_camera_number('LEFT'))
a = cameraConfig()
a.set_camera_number('LEFT', 1)
print(a.get_camera_number('LEFT'))
print(d.get_camera_number('LEFT'))
c = cameraConfig()
print(c.get_camera_number('LEFT'))1
1"""

resultspath_relative = "../res/restest/" + "side1"
image_folder_names = os.listdir(resultspath_relative)
print(image_folder_names)
class_correct_incorrect_dict = {}

for folder in image_folder_names:
    class_and_is_correct = folder.split('_')[1] + folder.split('_')[-1]
    if class_and_is_correct in class_correct_incorrect_dict:
        class_correct_incorrect_dict[class_and_is_correct] += 1
    else:
        class_correct_incorrect_dict[class_and_is_correct] = 0

print((cur_cor, cur_incor))


app = QApplication(sys.argv)
#correctdialog = correctincorrect_dialog.correctIncorrectDialog()
#is_correct = correctdialog.exec()
#if is_correct == QMessageBox.Accepted:
#    print("correct")
#else:
#    print("incorrect")
correctdialog2 = QMessageBox()
correctdialog2.setText("Recapturing correct or incorrect region?")
correctdialog2.setWindowTitle("Correct/Incorrect")

is_correct = correctdialog2.exec()
if is_correct == 0:
    print("Correct")
else:
    print("Incorrect")