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
from .Prediction import GazePredict
from .accuracy import AccuracyTest
from .Classifier import *
import time
import cv2
class CalibrationModel(QWidget):
    def __init__(self, testAccuracy,video):
        self.data = []
        super().__init__()
        self.accuracyTest = testAccuracy
        self.setWindowTitle("Python")
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
        self.showFullScreen()
        self.ht, self.wt = self.height(), self.width()
        print(str(self.ht) + str(self.wt))
        self.initialisation()
        self.showpoints()
        self.start()
        self.app_shortcut()
        self.display_image(video)
        self.show()
        self.infoDialog("click each points 5 times" , "EyeTracker" , "press Q to quit \n press R to recalibrate")
    def initialisation(self):
        self.x_train = []
        self.y_train = []
    def app_shortcut(self):
        self.shortcut_close = QShortcut(QKeySequence('Q'), self)
        self.shortcut_close.activated.connect(self.closeAppDialog)
        self.shortcut_recalibrate = QShortcut(QKeySequence('R'), self)
        self.shortcut_recalibrate.activated.connect(self.recalibrateDialog)
    def start(self):
        self.video = Video()
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)
    def stop(self):
        self.timer.stop()
        self.capture.release()
    def update_frame(self):
        _,frame = self.capture.read()
        self.video.update_frame(frame)
        self.update_image()
    def display_image(self,flag = True):
        self.image_label = QLabel(self)
        self.image_label.move(0,self.rad)
        self.image_label.resize(self.wt/3.5, self.ht/3)
        if(flag):
            self.image_label.show()
    def update_image(self):
        image = self.video.videoFrame()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.wt/3.5, self.ht/3, Qt.KeepAspectRatio)
        self.image_label.setPixmap(QPixmap.fromImage(p))    
    def getPath(self,path_name):
        cwd = os.path.abspath(os.path.dirname(__file__))
        css_path = os.path.abspath(os.path.join(cwd, path_name))
        return css_path

    def showpoints(self):
        self.button = []
        self.buttonRepeat = []
        self.buttonComplete = 0
        k = 0
        self.rad = 20
        self.half_ht = int((self.ht - self.rad) / 2)
        self.half_wt = int((self.wt - self.rad) / 2)
        for i in range(3):
            for j in range(3):
                x = j * self.half_wt
                y = i * self.half_ht
                self.button.append(QPushButton("O", self))
                self.button[k].setGeometry(x, y, self.rad, self.rad)
                self.button[k].setStyleSheet(open(self.getPath("stylesheet/buttonStyle.css")).read())
                self.button[k].clicked.connect(self.ButtonPress(k, x, y))
                self.button[k].show()
                self.buttonRepeat.append(0)
                k = k + 1
        self.buttonCenter = QPushButton("O", self)
        self.buttonCenter.setGeometry(self.half_wt, self.half_ht, self.rad , self.rad)
        self.buttonCenter.setStyleSheet("background-color: red ; border-radius: 10px;")        
    def hideButtons(self):
        for i  in self.button:
            i.hide()
    def ButtonPress(self, k, x, y):
        def calib():
            logging.info("button pressed")
            if self.video.is_eye_detected():
                self.add_data(x, y)
                if self.isFiveTimes(k):
                    self.button[k].setStyleSheet("background-color: red ; ; border-radius: 10px")
                if self.isCalibComplete():
                    self.save()
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
            pickle.dump(data, open("calibration.p", "wb"))
        except(IOError):
            logging.error("calibration file not found")
    def testAccuracy(self):
        self.infoDialog("look at the center point for some time" , "Accuracy Test")
        self.hideButtons()
        self.buttonCenter.show()
        self.predict = [GazePredict(model = model).train() for model in list_models()]
        self.data = []
        self.TestTimer = QTimer(self)
        self.TestTimer.timeout.connect(self.test_getData)
        self.TestTimer.start(250)
    def test_getData(self):
            print("testdata")
            if len(self.data) == 50:
                self.stop_timer()         
            if self.video.is_eye_detected() :
                    (x1,y1),(x2,y2) = self.video.get_pupil_coords() 
                    xy_pred = [p.predict(x1,y1,x2,y2) for p in self.predict]
                    print("data added ") 
                    self.data.append(xy_pred)
                    self.update()
    def stop_timer(self):
        print("stoped")
        self.TestTimer.stop()
        accuracy = AccuracyTest()
        centerPoint = self.half_wt , self.half_ht
        test_value = ''
        models = list_models()
        print(models)
        compare = accuracy.compare(self.data , centerPoint,self.ht)
        print(compare)
        for model , result in zip(list_models() , compare) :
            test_value += (str(model) + " Accuracy : "  + str(result) + "\n")
        self.infoDialog(test_value , "Accuracy Test")
        self.recalibrateDialog()
    def paintEvent(self , event):
        qp = QPainter(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        for i in self.data :
            x,y = i[0]
            qp.drawEllipse(x,y, 15 , 15)
    def recalibrate(self):
        self.data = []
        self.update()
        self.buttonCenter.hide()
        
        self.buttonComplete = 0
        for k in range(9):
            self.buttonRepeat[k] = 0
            self.button[k].setStyleSheet(open(self.getPath("stylesheet/buttonStyle.css")).read())
            self.button[k].show()           
    def closeApp(self):
        self.stop()
        self.close()
    def showRetryDialog(self):
        logging.warn("Eyes not detected")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Eyes Not Detected")
        msg.setInformativeText("Place your Eyes in camera")
        msg.setWindowTitle("warning")
        msg.setStandardButtons(QMessageBox.Retry)
        msg.exec_()
    def infoDialog(self,text , title,info = ""):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setInformativeText(info)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    def closeAppDialog(self):
        logging.warning("Recalibrate")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to close app ?")
        msg.setWindowTitle("EyeTracker")
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Close )
        if(msg.exec_() == QMessageBox.Close):
            self.closeApp()               
    def recalibrateDialog(self):
        logging.warning("Recalibrate")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to recalibrate ?")
        msg.setInformativeText("Do you want to recalibrate ?")
        msg.setWindowTitle("EyeTracker")
        msg.setStandardButtons(QMessageBox.Abort | QMessageBox.Yes )
        if(msg.exec_() == QMessageBox.Yes):
            self.recalibrate()
        else:
            self.closeApp()        
    def accuracyTestMessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("calibration completed")
        msg.setInformativeText("do you want to test accuracy ?")
        msg.setWindowTitle("Accuracy test")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.testAccuracy)
        msg.exec_() 