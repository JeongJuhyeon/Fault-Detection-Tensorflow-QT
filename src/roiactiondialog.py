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
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Close | QMessageBox.Apply)
        self.setDefaultButton(QMessageBox.Save)

        self.button(QMessageBox.Save).setText("Save (s)")
        self.button(QMessageBox.Save).setShortcut("s")
        self.button(QMessageBox.Discard).setText("Delete last (d)")
        self.button(QMessageBox.Discard).setShortcut("d")
        self.button(QMessageBox.Close).setText("Cancel (c)")
        self.button(QMessageBox.Close).setShortcut("c")
        self.button(QMessageBox.Apply).setText("Quit (q)")
        self.button(QMessageBox.Apply).setShortcut("q")

        self.hide()

    #def keyPressEvent(self, e):
    #    if e.key() == q:


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ROIActionDialog()
    buttonPressed = ex.exec()
    if buttonPressed == QMessageBox.Save:
        print("saved")
    elif buttonPressed == QMessageBox.Discard:
        print("deleted")
    elif buttonPressed == QMessageBox.Close:
        print("cancel")
    elif buttonPressed == QMessageBox.Apply:
        print("quit")
    buttonPressed = ex.exec()
    if buttonPressed == QMessageBox.Save:
        print("saved")
    elif buttonPressed == QMessageBox.Discard:
        print("deleted")
    elif buttonPressed == QMessageBox.Close:
        print("cancel")
    elif buttonPressed == QMessageBox.Apply:
        print("quit")
    # sys.exit(app.exec_())
    # exit()