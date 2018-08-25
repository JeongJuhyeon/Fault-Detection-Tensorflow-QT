import os
import sys

from PyQt5.QtWidgets import QInputDialog, QApplication, QMainWindow

selected_rois = []

with open('../res\\filetest' + '/' + 'locationInfo.txt', 'r+') as file:
    file.seek(0, os.SEEK_END)  # seek to end of file
    file_end = file.tell()  # get number of bytes in file
    i = 13
    while True:
        if file_end - i < 12:
            print("There's only one line.")
            file.truncate(0)
            file.close()
            break

        file.seek(file_end - i, os.SEEK_SET)  # go to end - i bytes
        c = file.read(1)
        print(c)
        if c == '\n':
            print("End of line found.")
            file.truncate(file_end - i + 1)
            file.close()
            break
        i += 1
    file.close()

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
