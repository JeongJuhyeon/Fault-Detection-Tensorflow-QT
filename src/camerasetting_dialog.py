import sys

from PyQt5.QtWidgets import QMessageBox, QApplication


class CameraSettingDialog(QMessageBox):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Camera selection")
        self.setText("Please select the location of this camera")

        # add buttons
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Close)
        self.setDefaultButton(QMessageBox.Save)

        self.button(QMessageBox.Save).setText("Left (l)")
        self.button(QMessageBox.Save).setShortcut("l")
        self.button(QMessageBox.Discard).setText("Center (c)")
        self.button(QMessageBox.Discard).setShortcut("c")
        self.button(QMessageBox.Close).setText("Right (r)")
        self.button(QMessageBox.Close).setShortcut("r")

        self.hide()

    # def keyPressEvent(self, e):
    #    if e.key() == q:


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraSettingDialog()
    buttonPressed = ex.exec()
    if buttonPressed == 0x00000800:
        print("saved")
    elif buttonPressed == 0x00800000:
        print("deleted")
    elif buttonPressed == 0x00200000:
        print("quit")
    buttonPressed = ex.exec()
    if buttonPressed == 0x00000800:
        print("saved")
    elif buttonPressed == 0x00800000:
        print("deleted")
    elif buttonPressed == 0x00200000:
        print("quit")
    # sys.exit(app.exec_())
    # exit()
