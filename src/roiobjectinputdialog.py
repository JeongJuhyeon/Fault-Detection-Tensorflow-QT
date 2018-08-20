import sys

from PyQt5.QtWidgets import QApplication, QInputDialog


class ROIobjectInputDialog(QInputDialog):
    def __init__(self):
        super(ROIobjectInputDialog, self).__init__()
        self.initUI()

    def initUI(self):
        self.setComboBoxEditable(False)
        self.itemNames = ["screw10", "screw20", "screw30", "label-date", "label-usage", "label-warning"]
        self.setComboBoxItems(self.itemNames)
        self.setLabelText("Object name:")
        self.setOption(2)
        self.textValueSelected.connect(self.onSelected)

    def onSelected(self):
        self.setResult(self.itemNames.index(self.textValue()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ROIobjectInputDialog()
    a = dialog.exec()
    print(a, "selected")
