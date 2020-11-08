from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .video import Video
from .Prediction import GazePredict
import sys
class PredictionModel(QWidget):
    def __init__(self):
        self.x_coords = 50
        self.y_coords = 50
        super().__init__()
        self.setWindowTitle("Python Prediction")
        self.showFullScreen()
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
        self.Initialisation()
        self.show()
    def Initialisation(self):
        self.video = Video()
        self.predict = GazePredict()

    def startPrediction(self):
        self.video.start_webcam()
        self.predict.train()
        timer = QTimer(self)
        timer.timeout.connect(self.updatePoint)
        timer.start(2)

    def updatePoint(self):
        self.video.update_frame()
        if self.video.is_eye_detected():
            (x1,y1),(x2,y2) = self.video.get_pupil_coords()
            coords  = self.predict.predict(x1,y1,x2,y2)
            self.x_coords = coords[0][0]
            self.y_coords = coords[0][1]
            print(self.x_coords,self.y_coords)
            self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt. blue , 8 , Qt.SolidLine))
        qp.drawEllipse(self.x_coords,self.y_coords, 30 , 30)