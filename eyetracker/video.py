import cv2
from gaze_tracking import GazeTracking
class Video:
    def __init__(self):
        self.gaze = GazeTracking()
        self.is_camera_running = False
    def start_webcam(self):
        if self.is_camera_running:
            return False
        self.capture = cv2.VideoCapture(0)
        self.is_camera_running = True
    def update_frame(self):
        if not self.is_camera_running:
            return False
        _, frame = self.capture.read()
        self.gaze.refresh(frame)
    def is_eye_detected(self):
        if ((self.gaze.pupil_left_coords() == None) or (self.gaze.pupil_right_coords() == None)):
            return False
        return True
    def get_pupil_coords(self):
        if self.is_eye_detected() :
            return self.gaze.pupil_left_coords(),self.gaze.pupil_right_coords()
