from .Calibration import CalibrationModel
from .Calibration import PredictionModel
from .Prediction import GazePredict
from PyQt5.QtWidgets import QApplication
import sys
class EyeTracker(object):
    def __init__(self):
        self.App = QApplication(sys.argv)
    def load_calibration_model(self):
        window = CalibrationModel(self.App)
        self.App.exec()
    def train(self):
        self.p = GazePredict()
        self.p.train()
    def predict(self,eye):
        pass
    def load_prediction_model(self):
        window = PredictionModel()
        window.load()
        window.startPrediction()
        self.App.exec()