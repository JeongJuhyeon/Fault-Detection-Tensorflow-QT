import sys
from PyQt5.QtWidgets import QLabel, QApplication, QFormLayout, QLineEdit, QDialog, QDialogButtonBox
from PyQt5.QtCore import QObject, pyqtSignal

class devnameCameraXYInputbox(QDialog):
    def __init__(self):
        super(devnameCameraXYInputbox, self).__init__()
        self.initUI()

    def initUI(self):
        self.curDevName = ""
        self.newDevice = True
        self.foundDeviceLineNo = -1
        self.textChanged = False
        self.configFilePath = "../devices.txt"


        # Add labels and self.lineEdits
        self.labels = ["left 1", "right 1", "above", "left 2", "right 2"]
        form = QFormLayout(self)
        form.addRow(QLabel("            Camera positions:"))
        self.lineEdits = []
        for label in self.labels:
            lineEdit = QLineEdit(self)
            lineEdit.textChanged.connect(self.onChanged)
            self.lineEdits.append(lineEdit)
            form.addRow(label, lineEdit)

        # Add buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.onOkay)
        form.addRow(buttonBox)

        #Open file
        try:
            self.file = open(self.configFilePath, 'r')
        except IOError:
            open(self.configFilePath, 'w')
            self.file = open(self.configFilePath, 'r+')

        self.lines = self.file.read().splitlines()

    # Searches if device name was used before, if it was, populate self.lineEdits
    def searchDevice(self):
        self.newDevice = True
        for i, line in enumerate(self.lines):
            if i % 8 == 0:
                if line[1:-1] == self.curDevName:
                    self.newDevice = False
                    self.foundDeviceLineNo = i
                    i += 1
                    for j in range(5):
                        self.lineEdits[j].setText(self.lines[i+j].split("=")[1])
                    self.textChanged = False
                    break

    # If okay is clicked, write to file if necessary
    def onOkay(self):
        # New device
        if self.newDevice:
            self.file.close()
            self.file = open(self.configFilePath, 'a')
            self.file.write("[" + self.curDevName + "]\n")
            for i, pos in enumerate(self.labels):
                self.file.write(pos.replace(" ", "") + "=" + self.lineEdits[i].text() + "\n")
            self.file.write("\n\n")
            self.file.close()

        # Already used device but values changed
        elif not self.newDevice and self.textChanged:
            for i in range(1, 6):
                self.lines[i + self.foundDeviceLineNo] = self.labels[i - 1].replace(" ", "") + "=" + self.lineEdits[i - 1].text()
            self.file.close()
            open("../devices.txt", 'w').write('\n'.join(self.lines))

        self.accept()

    def onChanged(self):
        self.textChanged = True



if __name__ == '__main__':
    import random
    app = QApplication(sys.argv)
    dialog = devnameCameraXYInputbox()
    dialog.curDevName = "Bob" + str(random)
    dialog.searchDevice()
    a = dialog.exec()
    print(a,  "selected")
