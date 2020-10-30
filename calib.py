from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
import sys
from gaze_tracking import GazeTracking
import cv2
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python ")
        self.showFullScreen()
        self.data = {}
        self.check = []
        self.c = 0
        self.re = []
        self.is_camera_running  = False
        self.is_eyes_detected = False
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
        self.ht = self.height()
        self.wt = self.width()
        print(str(self.ht)+ str(self.wt))
        self.gaze = GazeTracking()
        self.start_webcam()
        self.UiComponents()
        self.shortcut_close = QShortcut(QKeySequence('Q'), self)
        self.shortcut_close.activated.connect(self.closeApp)
        self.show()
    def start_webcam(self):
        if not self.is_camera_running:
            self.capture = cv2.VideoCapture(0)
            self.is_camera_running = True
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(2)
    def update_frame(self):
        _, frame = self.capture.read()
        self.gaze.refresh(frame)
        if(self.gaze.pupil_left_coords() != None and self.gaze.pupil_right_coords() != None):
            self.is_eyes_detected = True
        else:
            self.is_eyes_detected = False
    def UiComponents(self):
        button = []
        k=0
        half_ht = int((self.ht-30) /2)
        half_wt = int((self.wt-30)/ 2)
        for i in range(3):
            for j in range(3):
                x = j*half_wt
                y = i*half_ht
                button.append(QPushButton(str(k+1), self))
                button[k].setGeometry(x,y , 30, 30)
                button[k].setStyleSheet(open('buttonStyle.css').read())
                button[k].clicked.connect(self.calib(button ,k+1,x,y))
                button[k].show()
                self.re.append(0)
                k=k+1
    def showDialog(self):
        print("Eyes Not Detected")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Eyes Not Detected")
        msg.setInformativeText("Place your Eyes in camera")
        msg.setWindowTitle("warning")
        msg.setStandardButtons(QMessageBox.Retry)
        msg.exec_()
    def calib(self,button ,k,x,y):
        def add_data():
            if self.is_eyes_detected :
                self.data[(x,y)] = (self.gaze.pupil_left_coords(),self.gaze.pupil_right_coords())
                if (self.re[k - 1] != 5):
                    self.re[k - 1] = self.re[k - 1] + 1
                else:
                    button[k - 1].setStyleSheet("background-color: red")
                    print(k)
                    if k not in self.check:
                        self.c = self.c + 1
                        self.check.append(k)
                    if (self.c == 9):
                        print("calibration completed")
                        print(self.data)
                        sys.exit()
            else:
                self.showDialog()
        return add_data
    def closeApp(self):
        App.quit()
App = QApplication(sys.argv)
window = Window()
App.exec()
sys.exit(App.exec())
