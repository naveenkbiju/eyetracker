from .Calibration import CalibrationModel
from .Prediction import GazePredict
import logging
from PyQt5.QtWidgets import QApplication
from .video import Video
import sys
class EyeTracker(object):
    def __init__(self):
        self.video = Video()
        
        self.frame = None
        logging.basicConfig(level=logging.DEBUG , filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    def calibrate(self,TestAccuracy = False,video = True):
        self.App = QApplication(sys.argv)
        window = CalibrationModel(TestAccuracy , video)
        logging.info("calibration model started")
        self.App.exec()
        self.train()
    def train(self,model = "LR" , calibration_file_name = "calibration.p"):
        self.gaze= GazePredict(model)
        self.gaze.train(calibration_file_name)
        logging.info("trainig the model")
    def refresh(self , frame ):
          self.frame = frame
          self.video.update_frame(frame)  
    def gaze_point(self):
        if(self.frame is  None):
            logging.warning("refresh the frame to predict")
            return None
        if(not self.video.is_eye_detected()):
            logging.warning("eye not detected cannot predict gaze point")
            return None
        (x1,y1),(x2,y2) = self.video.get_pupil_coords()
        return self.gaze.predict(x1,y1,x2,y2)
    def annotated_frame(self):
        if(self.frame == None):
            logging.warning("refresh the frame")
            return None
        return self.video.videoFrame()
                 
