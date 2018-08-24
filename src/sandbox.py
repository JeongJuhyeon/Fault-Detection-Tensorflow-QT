import os
import sys

from PyQt5.QtWidgets import QInputDialog, QApplication, QMainWindow

selected_rois = []


def f():
    return


selected_rois.append(f)

line = "530_194_33_34_side1_screw10_4"
selected_rois.append(line.split('_')[:4])
selected_rois[-1].append('True')
selected_rois[-1].append('side1')
print(selected_rois)


def getname():
    curDevName = "Cashcounter"
    resultspath_relative = "../res" + "/" + curDevName + "/result"
    try:
        folder_names = os.listdir(resultspath_relative)
    except:
        return 1
    return int(folder_names[-1].split('_')[0]) + 1


print(getname())

a = ('{:04}'.format(getname()))
print(a)

app = QApplication(sys.argv)
MainWindow = QMainWindow()
b = QInputDialog.getText(MainWindow, "Device Number", "Enter device number:")
curDeviceNo = 5
resultsDeviceNo = 4

try:
    t = int(b[0])
    if (1 <= t <= curDeviceNo - 1):
        resultsDeviceNo = t
    else:
        print("Incorrect number entered!")
except:
    print("Incorrect number entered!")

print(resultsDeviceNo)
sys.exit(app.exec_())
