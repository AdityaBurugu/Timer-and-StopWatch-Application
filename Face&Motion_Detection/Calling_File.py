#######################################################################################################################
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

from Face_Motion_Detection_File import *
########################################################################################################################
class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
#########################################################a\ffi\\ff##############################################################

class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        #self.button = QPushButton("Start Server", self)
        self.pushButton = QPushButton("click me", self)#QtGui.QPushButton("click me")

        self.setCentralWidget(self.pushButton)

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton.setShortcut("H")
        self.dialogs = list()

    def on_pushButton_clicked(self):
        dialog = Window("192.168.1.10","192.168.1.10",60)
        self.dialogs.append(dialog)
        dialog.show()
        dia = Window("192.168.1.23","192.168.1.23",60)
        self.dialogs.append(dia)
        dia.show()

########################################################################################################################
def main():
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())
########################################################################################################################
if __name__ == '__main__':
    main()