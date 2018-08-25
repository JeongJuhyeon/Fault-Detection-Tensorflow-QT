import sys

from PyQt5.QtWidgets import QMessageBox, QApplication


class ROIActionDialog(QMessageBox):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ROI Selected")
        self.setText("Save ROI, Delete last ROI, Quit?")

        # add buttons
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Close)
        self.setDefaultButton(QMessageBox.Save)

        self.button(QMessageBox.Save).setText("Save (s)")
        self.button(QMessageBox.Save).setShortcut("s")
        self.button(QMessageBox.Discard).setText("Delete last (d)")
        self.button(QMessageBox.Discard).setShortcut("d")
        self.button(QMessageBox.Close).setText("Quit (q)")
        self.button(QMessageBox.Close).setShortcut("q")

        self.hide()

    #def keyPressEvent(self, e):
    #    if e.key() == q:


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ROIActionDialog()
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