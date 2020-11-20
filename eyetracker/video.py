import logging
import cv2
from gaze_tracking import GazeTracking
from multiprocessing import Process
from threading import Thread, Lock
class Video:
    def  __init__(self):
        self.gaze = GazeTracking()
        self.is_camera_running = False
        self.lock  = Lock()
        self.t = Thread(target=self.webcam_video , args=())
    def start(self):
        if self.is_camera_running:
            return False
        self.is_camera_running = True
        self.capture = cv2.VideoCapture(0)
        self.t.start()
        return self
    def stop_webcam(self):
        self.capture.release()
        self.is_camera_running = False    
    def webcam_video(self): 
        while True:
            _, frame = self.capture.read()
            self.lock.acquire()
            self.gaze.refresh(frame)
            self.lock.release()
    def is_eye_detected(self):
        self.lock.acquire()
        if not self.is_camera_running:
            logging.warning("camera is not running")
            return 
        if ((self.gaze.pupil_left_coords() == None) or (self.gaze.pupil_right_coords() == None)):
            logging.info("Eye not detected")
            return False
        logging.info("eye_detected")
        return True
    def get_pupil_coords(self):
        if self.is_eye_detected() :
            self.lock.acquire()
            x,y =  self.gaze.pupil_left_coords(),self.gaze.pupil_right_coords()
            self.lock.release()
            return x,y