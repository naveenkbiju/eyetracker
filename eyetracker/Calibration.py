import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .video import Video
from .Prediction import GazePredict
import logging
import pickle
import logging
import sys
from .PredictionModel import PredictionModel
from .Prediction import GazePredict
from .accuracy import AccuracyTest
import time
class CalibrationModel(QWidget):
    def __init__(self, App , testAccuracy):
        self.data = []
        super().__init__()
        self.App = App
        self.accuracyTest = testAccuracy
        self.setWindowTitle("Python")
        self.showFullScreen()
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
        self.ht, self.wt = self.height(), self.width()
        print(str(self.ht) + str(self.wt))
        self.initialisation()
        self.showpoints()
        self.start_webcam()
        self.app_shortcut()
        self.show()
    def initialisation(self):
        self.x_train = []
        self.y_train = []
    def app_shortcut(self):
        self.shortcut_close = QShortcut(QKeySequence('Q'), self)
        self.shortcut_close.activated.connect(self.closeApp)

    def start_webcam(self):
        self.video = Video()
        self.video.start_webcam()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video.update_frame)
        self.timer.start(1)

    def getPath(self,path_name):
        cwd = os.path.abspath(os.path.dirname(__file__))
        css_path = os.path.abspath(os.path.join(cwd, path_name))
        return css_path

    def showpoints(self):
        self.button = []
        self.buttonRepeat = []
        self.buttonComplete = 0
        k = 0
        rad = 30
        self.half_ht = int((self.ht - rad) / 2)
        self.half_wt = int((self.wt - rad) / 2)
        for i in range(3):
            for j in range(3):
                x = j * self.half_wt
                y = i * self.half_ht
                self.button.append(QPushButton(str(k + 1), self))
                self.button[k].setGeometry(x, y, rad, rad)
                self.button[k].setStyleSheet(open(self.getPath("stylesheet/buttonStyle.css")).read())
                self.button[k].clicked.connect(self.ButtonPress(k, x, y))
                self.button[k].show()
                self.buttonRepeat.append(0)
                k = k + 1
    def hideButtons(self,  notkey  = None):
        for i  in self.button:
            if(i != self.button[notkey]):
                i.hide()
    def showRetryDialog(self):
        logging.warn("Eyes not detected")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Eyes Not Detected")
        msg.setInformativeText("Place your Eyes in camera")
        msg.setWindowTitle("warning")
        msg.setStandardButtons(QMessageBox.Retry)
        msg.exec_()
    def infoDialog(self,text , title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setInformativeText(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.do_nothing)
        msg.exec_()
    def accuracyTestMessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("calibration completed")
        msg.setInformativeText("do you want to test accuracy ?")
        msg.setWindowTitle("Accuracy test")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.testAccuracy)
        msg.exec_()
    def do_nothing(self):
        pass    
    def ButtonPress(self, k, x, y):
        def calib():
            logging.info("button pressed")
            if self.video.is_eye_detected():
                self.add_data(x, y)
                if self.isFiveTimes(k):
                    self.button[k].setStyleSheet("background-color: red ")
                if self.isCalibComplete():
                    self.save()
                    print(self.accuracyTest)
                    if self.accuracyTest :
                        self.accuracyTestMessageBox()
                    else :    
                        self.infoDialog("calibration completed "  , "EyeTracking")
                        self.closeApp()
            else:
                self.showRetryDialog()

        return calib

    def isFiveTimes(self, k):
        self.buttonRepeat[k] = self.buttonRepeat[k] + 1
        if (self.buttonRepeat[k] == 5):
            self.buttonComplete+= 1
            return True
        return False

    def isCalibComplete(self):
        if self.buttonComplete == 9:
            return True
        return False

    def add_data(self, x, y):
        (x1, y1), (x2, y2) = self.video.get_pupil_coords()
        self.x_train.append([x1, y1, x2, y2])
        self.y_train.append([x, y])

    def save(self):
        data = {}
        data["x_train"] = self.x_train
        data["y_train"] = self.y_train
        try :
            pickle.dump(data, open("calibration_data/calibration.p", "wb"))
        except(IOError):
            logging.error("calibration file not found")
    def testAccuracy(self):
        self.infoDialog("look at the center point for some time" , "Accuracy Test")
        centerButtonKey  = 5
        self.hideButtons(notkey = centerButtonKey -1)
        self.predict = GazePredict()
        self.predict.train()
        self.data = []
        self.TestTimer = QTimer(self)
        self.TestTimer.timeout.connect(self.test_getData)
        self.TestTimer.start(500)
    def test_getData(self):
            print("testdata")
            if len(self.data) == 50:
                self.stop_timer()         
            if self.video.is_eye_detected() :
                    (x1,y1),(x2,y2) = self.video.get_pupil_coords() 
                    x_pred , y_pred = self.predict.predict(x1,y1,x2,y2)
                    print("data added ")
                    self.data.append((x_pred , y_pred))
                    self.update()
    def stop_timer(self):
        print("stoped")
        self.TestTimer.stop()
        accuracy = AccuracyTest().load(self.data)
        centerPoint = self.half_wt , self.half_ht
        test_value = "Accuracy : "  + str(accuracy.checkAccuracy(centerPoint,self.ht))
        self.infoDialog(test_value , "Accuracy Test")
        self.closeApp()
    def paintEvent(self , event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt. blue , 8 , Qt.SolidLine))
        for i in self.data :
            x,y = i
            qp.drawEllipse(x,y, 30 , 30)   
    def closeApp(self):
        self.App.exit()
