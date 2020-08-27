from PyQt5.QtWidgets import QApplication, QMainWindow,QDateEdit,QFrame, QPushButton,QTextEdit, QLabel,\
    QLineEdit,QToolBar,QComboBox, QMenu, QAction,QTableWidget,QTableWidgetItem,QHeaderView,\
    QVBoxLayout,QWidget
import sys
from PyQt5 import QtGui, QtCore, QtWidgets

from PyQt5.QtCore import QRect,QTimer
import cv2
from ONVIFCameraControl import ONVIFCameraControl,ONVIFCameraControlError
import numpy as np
from time import strftime,sleep

#import dlib
fwidth = 400
fheight = 300
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# This allows us to detect faces in images
#face_detector = dlib.get_frontal_face_detector()
fgbg = cv2.createBackgroundSubtractorMOG2()
class Shortcuts(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Shortcuts")
        self.setWindowIcon(QtGui.QIcon("../Resources/About.png"))
        self.setFixedWidth(300)
        self.setFixedHeight(438)

        layout = QVBoxLayout()

        self.tableWidget = QtWidgets.QTableWidget()

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(13)
        self.tableWidget.setHorizontalHeaderLabels(("Actions", "Shortcuts"))
        self.tableWidget.setDisabled(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setItem(0,0,QTableWidgetItem("Face Detection"))
        self.tableWidget.setItem(0,1,QTableWidgetItem("F1"))
        self.tableWidget.setItem(1,0,QTableWidgetItem("Motion Detection"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("M"))
        self.tableWidget.setItem(2,0,QTableWidgetItem("Record"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Ctrl+R"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Move Up"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Up Arrow Key"))
        self.tableWidget.setItem(4, 0, QTableWidgetItem("Move Down"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem("Down Arrow Key"))
        self.tableWidget.setItem(5, 0, QTableWidgetItem("Move Left"))
        self.tableWidget.setItem(5, 1, QTableWidgetItem("Left Arrow Key"))
        self.tableWidget.setItem(6, 0, QTableWidgetItem("Move Right"))
        self.tableWidget.setItem(6, 1, QTableWidgetItem("Right Arrow Key"))
        self.tableWidget.setItem(7, 0, QTableWidgetItem("Zoom In"))
        self.tableWidget.setItem(7, 1, QTableWidgetItem("Ctrl++"))
        self.tableWidget.setItem(8, 0, QTableWidgetItem("Zoom Out"))
        self.tableWidget.setItem(8, 1, QTableWidgetItem("Ctrl+-"))
        self.tableWidget.setItem(9, 0, QTableWidgetItem("Maximize"))
        self.tableWidget.setItem(9, 1, QTableWidgetItem("Alt+M"))
        self.tableWidget.setItem(10, 0, QTableWidgetItem("Increase Time Duration"))
        self.tableWidget.setItem(10, 1, QTableWidgetItem("Alt+I"))
        self.tableWidget.setItem(11, 0, QTableWidgetItem("Exit"))
        self.tableWidget.setItem(11, 1, QTableWidgetItem("Esc"))
        self.tableWidget.setItem(12, 0, QTableWidgetItem("About"))
        self.tableWidget.setItem(12, 1, QTableWidgetItem("I"))

        layout.addWidget(self.tableWidget)

        self.setLayout(layout)
class FrameGrabber(QtCore.QThread):
    def __init__(self, parent=None):
        super(FrameGrabber, self).__init__(parent)
        self.CamIP = 0
        self.windowzoomsize = 0
        self.SetFaceDetection = False
        self.SetMotionDetection = False
       # self.SetNormalVideo = True

    signal = QtCore.pyqtSignal(QtGui.QImage)
    signalm = QtCore.pyqtSignal(np.ndarray)

    def run(self):
        static_back = None
        #CamIP = "192.168.1.23"
        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(f'rtsp://admin:admin@{self.CamIP}:554/cam/realmonitor?channel=1&subtype=2')
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        #width = camera.set(CAP_PROP_FRAME_WIDTH, 1600)
        #height = camera.set(CAP_PROP_FRAME_HEIGHT, 1080)
       # cap.set(cv2.CAP_PROP_FPS, 4)
        while cap.isOpened():
            #if self.SetNormalVideo == True:
            for _ in range(1):
                success, frame = cap.read()
            if self.windowzoomsize == 2:
                success, frame = cap.read()
                success, frame = cap.read()
                success, frame = cap.read()
                success, frame = cap.read()
            if self.SetFaceDetection == True:
                for _ in range(5):
                    success, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            elif self.SetMotionDetection == True :
                frame1 = frame
                success, frame2 = cap.read()
                try:
                    # Difference between frame1(image) and frame2(image)
                    diff = cv2.absdiff(frame1, frame2)
                    # Converting color image to gray_scale image
                    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                    # Converting gray scale image to GaussianBlur, so that change can be find easily
                    blur = cv2.GaussianBlur(gray, (5, 5), 0)
                    # If pixel value is greater than 20, it is assigned white(255) otherwise black
                    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                   # frame = np.ndarray(thresh)
                    #print(type(thresh))
                    self.signalm.emit(thresh)
                    frame1 = frame2
                    success, frame2 = cap.read()
                except:
                    print('error in motion detetion')
                    #self.signalm.emit(frame)
            if success:
                self.image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
                if self.windowzoomsize == 0:
                    self.image = self.image.scaled(800, 600)
                    #print('False')
                elif self.windowzoomsize == 1 :
                    self.image = self.image.scaled(960, 720)
                else :
                    self.image = self.image.scaled(1280,1080)
                #if self.SetMotionDetection == False :
                self.signal.emit(self.image)
                #self.signalm.emit(frame)

class Window(QMainWindow):
    def __init__(self, windowTitle,CamIP):
        super().__init__()

        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

        self.left = 5
        self.top = 0
        self.width = 800
        self.height = 650
        Icon = "Icon.png"
        self.setWindowIcon(QtGui.QIcon(Icon))
        self.setWindowTitle(windowTitle)
        self.setGeometry(200,  50, 810, 875)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.CustomizeWindowHint)
        self.UiComponents()
        self.grabber = FrameGrabber()
        self.grabber.CamIP = CamIP
        self.cam = ONVIFCameraControl((CamIP, 80), "admin", "admin")
        self.grabber.signal.connect(self.updateFrame)
        self.grabber.signalm.connect(self.motionimage)
        self.grabber.start()
        #self.cam = ONVIFCameraControl((CamIP, 80), "admin", "admin")
        #self.cam.goto_preset(preset_token="2")
        self.timer = QTimer(self)
        self.time = 30
        self.timer.start(5000)
        print(self.timer.remainingTime())
        self.timer.timeout.connect(self.Fun_Exit)
        #self.timer =
        self.show()

    def UiComponents(self):
        self.time = 30
        self.timer = QTimer(self)
        self.lcd = QtWidgets.QLabel(self)
        #self.lcd.
        font = QtGui.QFont()  # Sets Font
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(750)
        self.lcd.setFont(font)
        self.color_effect = QtWidgets.QGraphicsColorizeEffect()
        self.color_effect.setColor(QtCore.Qt.yellow)
        self.lcd.setGraphicsEffect(self.color_effect)
        self.lcd.setStyleSheet("border-radius : 30;border: 2px solid red;")
        self.lcd.setText("Time Remaining :" + str(self.time) + "Seconds")
        self.lcd.setGeometry(500,80,290,30)

        self.timer.start(self.time * 1000)
        self.T_FaceDetect = "Face Detect"
        self.T_motionDetect = "Motion Detect"
        self.T_record = "Start Recording"
        self.T_MoveUp = "Camera Tilt Up"
        self.T_MoveDown = "Camera Tilt  Down"
        self.T_MoveLeft = "Pan Left"
        self.T_MoveRight = "Pan Right"
        self.T_ZoomIn = "Zoom In"
        self.T_ZoomOut = "Zoom Out"
        self.T_Maximize = "Maximize"
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QtCore.QSize(15, 15))
        self.addToolBar(toolbar)
        self.Face = QAction(QtGui.QIcon("../Resources/Face2.jpg"), self.T_FaceDetect, self)  # add student icon
        self.Face.triggered.connect(self.Face_Detect)
        self.Face.setShortcut("F1")
        self.Face.setStatusTip("Face Detect")
        self.Motion = QAction(QtGui.QIcon("../Resources/Motion.png"), self.T_motionDetect, self)  # add student icon
        self.Motion.triggered.connect(self.Motion_Detect)
        self.Motion.setShortcut("M")
        self.Motion.setStatusTip("Motion Detect")
        self.Record = QAction(QtGui.QIcon("../Resources/re.png"), self.T_record, self)  # add student icon
        self.Record.triggered.connect(self.Fun_Record)
        self.Record.setShortcut("Ctrl+R")
        self.Record.setStatusTip("Record")
        self.Up = QAction(QtGui.QIcon("../Resources/Up.jpg"), self.T_MoveUp, self)  # add student icon
        self.Up.triggered.connect(self.Move_Up)
        self.Up.setShortcut("Up")
        self.Up.setStatusTip("Move Up")
        self.Down = QAction(QtGui.QIcon("../Resources/Down.jpg"), self.T_MoveDown, self)  # add student icon
        self.Down.triggered.connect(self.Move_Down)
        self.Down.setShortcut("Down")
        self.Down.setStatusTip("Move Down")
        self.Left = QAction(QtGui.QIcon("../Resources/Left.jpg"), self.T_MoveLeft, self)  # add student icon
        self.Left.triggered.connect(self.Move_Left)
        self.Left.setShortcut("Left")
        self.Left.setStatusTip("Move Left")
        self.Right = QAction(QtGui.QIcon("../Resources/Right.jpg"), self.T_MoveRight, self)  # add student icon
        self.Right.triggered.connect(self.Move_Right)
        self.Right.setShortcut("Right")
        self.Right.setStatusTip("Move Right")
        self.ZoomIn = QAction(QtGui.QIcon("../Resources/ZoomIn.png"),self.T_ZoomIn, self)  # add student icon
        self.ZoomIn.triggered.connect(self.Zoom_In)
        self.ZoomIn.setShortcut("=")
        self.ZoomIn.setStatusTip("Zoom In")
        self.ZoomOut = QAction(QtGui.QIcon("../Resources/ZoomOut.png"), self.T_ZoomOut, self)  # add student icon
        self.ZoomOut.triggered.connect(self.Zoom_Out)
        self.ZoomOut.setShortcut("-")
        self.ZoomOut.setStatusTip("Zoom Out")
        self.Maximize = QAction(QtGui.QIcon("../Resources/Minimize.png"),self.T_Maximize,self)
        self.Maximize.triggered.connect(self.Fun_Maximize)
        self.Maximize.setShortcut("Alt+M")
        self.Maximize.setStatusTip("Maximize")
        self.TimeIncrement = QtWidgets.QAction(QtGui.QIcon("../Resources/Clock.jpg"),"Clock",self)
        self.TimeIncrement.triggered.connect(self.Funtion_Time)
        self.TimeIncrement.setShortcut("Alt+I")
        self.TimeIncrement.setStatusTip("Clock")
        self.Exit = QAction(QtGui.QIcon("../Resources/Exit1.png"),"Exit",self)
        self.Exit.setShortcut("Esc")
        self.Exit.triggered.connect(self.Main_Exit)
        self.About = QAction(QtGui.QIcon("../Resources/About.png"),"Shortcuts",self)
        self.About.setShortcut("I")
        self.About.triggered.connect(self.Fun_About)
        toolbar.addAction(self.Face)
        toolbar.addAction(self.Motion)
        toolbar.addAction(self.Record)
        toolbar.addAction(self.Up)
        toolbar.addAction(self.Down)
        toolbar.addAction(self.Left)
        toolbar.addAction(self.Right)
        toolbar.addAction(self.ZoomIn)
        toolbar.addAction(self.ZoomOut)
        toolbar.addAction(self.Maximize)
        toolbar.addAction(self.TimeIncrement)
        toolbar.addAction(self.Exit)
        toolbar.addAction(self.About)
        self.statusBar().show()





    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 50, self.image)
        self.image = QtGui.QImage()

    def Face_Detect(self):
        print("Function Face Detect Connected")
        if self.grabber.SetFaceDetection == True :
            self.statusBar().showMessage("Face Detection Stopped")
            self.grabber.SetFaceDetection = False
        else :
            self.grabber.SetFaceDetection = True
            self.statusBar().showMessage("Face Detection Started")


        self.grabber.SetMotionDetection = False



    def Motion_Detect(self):
        print("Function Motion Detect Connected")
        if self.grabber.SetMotionDetection == True:
            self.statusBar().showMessage("Motion Detection Stopped")
            self.grabber.SetMotionDetection = False
            try:
                cv2.destroyWindow("motion video")
            except:
                print('motion video already closed')
        else:
            self.statusBar().showMessage("Motion Detection Started")
            self.grabber.SetMotionDetection = True



        self.grabber.SetFaceDetection = False

    def Fun_Record(self):
        print("Function Record Connected")
        self.statusBar().showMessage("Started Recording")
    def Move_Up(self):
        print("Function Move Up Connected")
        ptz_velocity_vector = (0, -0.85, 0)
        self.cam.move_continuous(ptz_velocity_vector)
        sleep(0.25)
        self.cam.stop()
    def Move_Down(self):
        print("Function Move Down Connected")
        ptz_velocity_vector = (0, 0.85, 0)
        self.cam.move_continuous(ptz_velocity_vector)
        sleep(0.25)
        self.cam.stop()
    def Move_Left(self):
        print("Function Move Left Connected")
        ptz_velocity_vector = (-0.85, 0, 0)
        self.cam.move_continuous(ptz_velocity_vector)
        sleep(0.25)
        self.cam.stop()
    def Move_Right(self):
        print("Function Move Right Connected")
        ptz_velocity_vector = (0.85, 0, 0)
        self.cam.move_continuous(ptz_velocity_vector)
        sleep(0.25)
        self.cam.stop()
    def Zoom_In(self):
        print("Function Zoom In Connected")
        ptz_velocity_vector = (0, 0, 0.25)
        self.cam.move_continuous(ptz_velocity_vector)
        sleep(1)
        self.cam.stop()
    def Zoom_Out(self):
        print("Function Zoom Out Connected")
        ptz_velocity_vector = (0, 0, -0.25)
        self.cam.move_continuous(ptz_velocity_vector)
        sleep(1)
        self.cam.stop()
    def Fun_Maximize(self):
        self.move(200,5)
        self.grabber.windowzoomsize = (self.grabber.windowzoomsize + 1) % 2

    def Funtion_Time(self):
        self.time=30

    def Fun_Exit(self):
        self.lcd.setText("Time Remaining :"+str(self.time)+" Seconds")
        if self.time==0:
            QApplication.quit()
        elif(self.time>5):
           # self.lcd.setText("Time Remaining :" + str(self.time) + " Seconds")

            self.color_effect.setColor(QtCore.Qt.yellow)
            self.lcd.setGraphicsEffect(self.color_effect)
            self.time = self.time - 1
        elif(self.time<=5):
            #self.lcd.setText("Time Remaining :" + str(self.time) + " Seconds")
            self.color_effect.setColor(QtCore.Qt.white)
            self.lcd.setGraphicsEffect(self.color_effect)
            self.time = self.time - 1
        elif(self.time==1):
            #self.lcd.setText("Time Remaining :" + str(self.time) + " Second")
            self.time=self.time-1
        else:
            self.time=self.time-1
    def Main_Exit(self):
        QApplication.quit()

    def Fun_About(self):
        dlg = Shortcuts()
        dlg.exec_()

    @QtCore.pyqtSlot(QtGui.QImage)
    def updateFrame(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

    @QtCore.pyqtSlot(np.ndarray)
    def motionimage(self, image):
        #print('Cv2.show')
        cv2.imshow("motion video", image)
        #cv2.resize("motion video",(800,600))

def Main():
    App = QApplication(sys.argv)
    windowTitle = "Camera1"
    CamIP = "192.168.1.10"
    window = Window(windowTitle,CamIP)
    sys.exit(App.exec())

if __name__ == "__main__":
    Main()
