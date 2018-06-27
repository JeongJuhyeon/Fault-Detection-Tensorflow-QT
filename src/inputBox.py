import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

class App(QWidget):
    def __init__(self, subtitle = "Enter", choose = 0):
        super().__init__()
        self.title = 'GUI'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.subtitle = subtitle
        self.val = ''
        self.okPressed = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.hide()
        # self.do_UI()

    def do_UI(self):
        self.val, self.okPressed = QInputDialog.getText(self, "Get text", self.subtitle, QLineEdit.Normal, "")

    def getValue(self):
        if self.okPressed and self.val != '':
            return self.val
        else:
            return "NONE"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.do_UI()
    sys.exit(app.exec_())