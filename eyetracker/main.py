from .Calibration import Calibrate
from .Prediction import GazePredict
from PyQt5.QtWidgets import QApplication
import sys
class EyeTracker(object):
    def __init__(self):
        pass
    def load_calibration_model(self):
        Calibrate()
    def train(self):
        self.p = GazePredict()
        self.p.train()
    def predict(self,eye):
        return self.p.predict(x,y)
