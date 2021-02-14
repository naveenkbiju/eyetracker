from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
from FitGaze import EyeTracker
class PredictionModel(QWidget):
    def __init__(self,tracker):
        self.x_coords = 50
        self.y_coords = 50
        super().__init__()
        self.setWindowTitle("Python Prediction")
        self.showFullScreen()
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
        self.tracker = tracker
        self.start_camera()
        self.startPrediction()
        self.show()
    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
    def startPrediction(self):
        timer = QTimer(self)
        timer.timeout.connect(self.updatePoint)
        timer.start(100)
    def updatePoint(self):
        _,frame = self.capture.read()
        self.tracker.refresh(frame)
        gaze_point = self.tracker.gaze_point()
        if gaze_point is not None:
            self.x_coords  , self.y_coords  = gaze_point
            self.update()
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.drawEllipse(self.x_coords,self.y_coords, 15 , 15)
        
        
if __name__ == '__main__' :
        tracker = EyeTracker()
        tracker.calibrate(TestAccuracy = True)
        app = QApplication(sys.argv)
        a = PredictionModel(tracker)
        sys.exit(app.exec())    