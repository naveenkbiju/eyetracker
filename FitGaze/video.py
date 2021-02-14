import cv2
from .lib.gaze_tracking import GazeTracking
class Video:
    def __init__(self):
        self.gaze = GazeTracking()
    def update_frame(self,frame):
        self.gaze.refresh(frame)
    def videoFrame(self):
        return self.gaze.annotated_frame()    
    def is_eye_detected(self):
        if ((self.gaze.pupil_left_coords() == None) or (self.gaze.pupil_right_coords() == None)):
            return False
        return True
    def get_pupil_coords(self):
        if self.is_eye_detected() :
            return self.gaze.pupil_left_coords(),self.gaze.pupil_right_coords()
