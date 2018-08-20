import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton

class correctIncorrectDialog(QMessageBox):


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Correct/Incorrect")
        self.setText("Recapturing correct or incorrect region?")

        # add buttons
        correct_button = self.addButton("Correct", QMessageBox.YesRole)
        incorrect_button = self.addButton("Incorrect", QMessageBox.NoRole)
        correct_button.setDefault(True)

        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = correctIncorrectDialog()
    buttonPressed = ex.exec()
    if buttonPressed == 0:
        print("correct")
    else:
        print("incorrect")
    # sys.exit(app.exec_())
    # exit()