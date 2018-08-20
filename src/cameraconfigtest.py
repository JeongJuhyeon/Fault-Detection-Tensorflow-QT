from config import cameraConfig
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
import correctincorrect_dialog

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