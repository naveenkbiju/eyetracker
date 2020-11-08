from .Calibration import CalibrationModel
from .Calibration import PredictionModel
from .Prediction import GazePredict
import logging
from PyQt5.QtWidgets import QApplication
import sys
class EyeTracker(object):
    def __init__(self):
        self.App = QApplication(sys.argv)
    def load_calibration_model(self):
        window = CalibrationModel(self.App)
        logging.info("calibration model started")
        self.App.exec()
    def train(self):
        self.p = GazePredict()
        self.p.train()
        logging.info("trainig the model")
    def predict(self,eye):
        pass
    def load_prediction_model(self):
        window = PredictionModel()
        window.startPrediction()
        logging.info("load prediction model")
        self.App.exec()