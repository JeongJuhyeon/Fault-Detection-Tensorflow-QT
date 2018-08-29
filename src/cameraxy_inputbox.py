import sys

from PyQt5.QtWidgets import QLabel, QApplication, QFormLayout, QLineEdit, QDialog, QDialogButtonBox

import config


class cameraXYInputbox(QDialog):
    def __init__(self, curDevName):
        super(cameraXYInputbox, self).__init__()
        self.curDevName = curDevName
        self.initUI()

    def initUI(self):
        self.newDevice = True
        self.foundDeviceLineNo = -1
        self.textChanged = False
        self.devices_file_path = "../devices.txt"

        # Add labels and self.lineEdits
        self.labels = config.SIDE_NAMES
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

        # Open file
        try:
            file = open(self.devices_file_path, 'r')
        except IOError:
            open(self.devices_file_path, 'w')
            file = open(self.devices_file_path, 'r+')

        self.lines = file.read().splitlines()
        file.close()

    # Searches if device name was used before, if it was, populate self.lineEdits
    def searchDevice(self):
        self.newDevice = True
        found = False
        for i, line in enumerate(self.lines):
            if i % 8 == 0:
                if line[1:-1] == self.curDevName:
                    self.newDevice = False
                    self.foundDeviceLineNo = i
                    i += 1
                    for j in range(5):
                        self.lineEdits[j].setText(self.lines[i + j].split("=")[1])
                    self.textChanged = False
                    found = True
                    break
        if not found:
            raise FileNotFoundError

    # If okay is clicked, write to file if necessary
    def onOkay(self):
        # New device
        if self.newDevice:
            with open(self.devices_file_path, 'a') as file:
                file.write("[" + self.curDevName + "]\n")
                for i, pos in enumerate(self.labels):
                    file.write(pos.replace(" ", "") + "=" + self.lineEdits[i].text() + "\n")
                file.write("\n\n")

        # Already used device but values changed
        elif not self.newDevice and self.textChanged:
            for i in range(1, 6):
                self.lines[i + self.foundDeviceLineNo] = self.labels[i - 1].replace(" ", "") + "=" + self.lineEdits[
                    i - 1].text()
            with open(self.devices_file_path, 'w') as file:
                file.write('\n'.join(self.lines))
                file.write('\n')

        self.accept()

    def onChanged(self):
        self.textChanged = True

    def __repr__(self):
        return 'cameraXYInputbox(%r)' % self.curDevName


if __name__ == '__main__':
    import random

    app = QApplication(sys.argv)
    dialog = cameraXYInputbox("Bob")
    dialog.curDevName = "Bob" + str(random)
    dialog.searchDevice()
    a = dialog.exec()
    print(a, "selected")
