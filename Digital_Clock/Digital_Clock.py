import sys
from PyQt5 import QtGui, QtCore,QtWidgets

from time import strftime

var = True


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.CustomizeWindowHint)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.Time)
        # Reduced update time to fasten the change from w/ secs to w/o secs
        timer.start(10)

        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.resize(250, 100)

        # Added self.lcd.move and moved the clock 30px down to make space for buttons

        self.lcd.move(0, 30)
        self.lcd.display(strftime("%H" + ":" + "%M"))

        self.r1 = QtWidgets.QRadioButton("Hide seconds", self)
        self.r1.move(10, 0)
        self.r2 = QtWidgets.QRadioButton("Show seconds", self)
        self.r2.move(110, 0)

        self.r1.toggled.connect(self.woSecs)
        self.r2.toggled.connect(self.wSecs)

        # ---------Window settings --------------------------------

        # Expanded window height by 30px

        self.setGeometry(300, 300, 250, 130)
        self.setWindowTitle("Clock")
        self.setWindowIcon(QtGui.QIcon(""))
        self.show()

    # -------- Slots ------------------------------------------

    def Time(self):
        global var
        if var == True:
            self.lcd.display(strftime("%H" + ":" + "%M"))
        elif var == False:
            self.lcd.display(strftime("%H" + ":" + "%M" + ":" + "%S"))

    def wSecs(self):
        global var
        var = False

        self.resize(375, 130)
        self.lcd.resize(375, 100)
        self.lcd.setDigitCount(8)

    def woSecs(self):
        global var
        var = True

        self.resize(250, 130)
        self.lcd.resize(250, 100)
        self.lcd.setDigitCount(5)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()