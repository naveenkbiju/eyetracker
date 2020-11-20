from .Calibration import CalibrationModel
from .Calibration import PredictionModel
from .Prediction import GazePredict
from .self_calibration import SelfCalibration
from .video import  Video
import logging
from PyQt5.QtWidgets import QApplication
import sys
class EyeTracker(object):
    def __init__(self):
        self.is_started = False
    def start(self):
        self.video = Video().start()
        self.calib = SelfCalibration(self.video)
        self.is_started  = True
    def stop(self):
        self.video.stop_webcam()
        self.calib.stop()  
        self.is_started = False  
    def load_calibration_model(self):
        App = QApplication(sys.argv)
        window = CalibrationModel(App,self.video)
        logging.info("calibration model started")
        self.App.exec()
    def train(self):
        self.p = GazePredict()
        self.p.train()
        logging.info("trainig the model")
    def predict(self,eye):
        pass
    def load_prediction_model(self):
        self.App = QApplication(sys.argv)
        window = PredictionModel()
        logging.info("load prediction model")
        self.App.exec()
    