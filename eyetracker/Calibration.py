import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .video import Video
from .Prediction import GazePredict
import logging
import pickle
import sys
from .PredictionModel import PredictionModel
class CalibrationModel(QWidget):
    def __init__(self, App):
        super().__init__()
        self.App = App
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
        self.prediction_model = PredictionModel()
    def app_shortcut(self):
        self.shortcut_close = QShortcut(QKeySequence('Q'), self)
        self.shortcut_close.activated.connect(self.closeApp)

    def start_webcam(self):
        self.video = Video()
        self.video.start_webcam()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video.update_frame)
        self.timer.start(2)

    def getCssPath(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        css_path = os.path.abspath(os.path.join(cwd, "stylesheet/buttonStyle.css"))
        return css_path

    def showpoints(self):
        self.button = []
        self.buttonRepeat = []
        self.buttonComplete = []
        k = 0
        rad = 30
        half_ht = int((self.ht - rad) / 2)
        half_wt = int((self.wt - rad) / 2)
        for i in range(3):
            for j in range(3):
                x = j * half_wt
                y = i * half_ht
                self.button.append(QPushButton(str(k + 1), self))
                self.button[k].setGeometry(x, y, rad, rad)
                self.button[k].setStyleSheet(open(self.getCssPath()).read())
                self.button[k].clicked.connect(self.ButtonPress(k, x, y))
                self.button[k].show()
                self.buttonRepeat.append(0)
                self.buttonComplete.append(False)
                k = k + 1

    def showRetryDialog(self):
        print("Eyes Not Detected")
        logging.info("Eyes not detected")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Eyes Not Detected")
        msg.setInformativeText("Place your Eyes in camera")
        msg.setWindowTitle("warning")
        msg.setStandardButtons(QMessageBox.Retry)
        msg.exec_()

    def showCalibCompleteDialog(self):
        print("Calibration completed")
        logging.info("calibration completed")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("calibration completed ")
        msg.setWindowTitle("Eye Tracking ")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.save)
        msg.exec()

    def ButtonPress(self, k, x, y):
        def calib():
            if self.video.is_eye_detected():
                self.add_data(x, y)
                if self.isFiveTimes(k):
                    self.button[k].setStyleSheet("background-color: red ")
                if self.isCalibComplete():
                    self.showCalibCompleteDialog()
            else:
                self.showRetryDialog()

        return calib

    def isFiveTimes(self, k):
        self.buttonRepeat[k] = self.buttonRepeat[k] + 1
        if (self.buttonRepeat[k] == 5):
            self.buttonComplete[k] = True
            return True
        return False

    def isCalibComplete(self):
        if False in self.buttonComplete:
            return False
        return True

    def add_data(self, x, y):
        (x1, y1), (x2, y2) = self.video.get_pupil_coords()
        self.x_train.append([x1, y1, x2, y2])
        self.y_train.append([x, y])

    def save(self):
        data = {}
        data["x_train"] = self.x_train
        data["y_train"] = self.y_train
        pickle.dump(data, open("calibration_data/calibration.p", "wb"))
        self.closeApp()

    def closeApp(self):
        self.App.quit()
    def showGazePoint(self):
        self.p = GazePredict()
    def updateGazePoint(self):
        x , y = self.p.predict(self.video.get_pupil_coords())
