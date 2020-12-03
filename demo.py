from PyQt5.QtCore import  *
import sys
import time
from  multiprocessing import Process
from gaze_tracking import GazeTracking
from PyQt5.QtCore import *
import cv2
import time
gaze = GazeTracking()
webcam = cv2.VideoCapture(0) 
class newClass():
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0) 
        #timer  =  QTimer()
        #timer.timeout.connect(self.run_webcam)
        #timer.start(500)
        p = Process(target=self.run_in_loop, args = ())
        p.start()
        print("test print")
    def is_eye_detected(self):
        if ((self.gaze.pupil_left_coords() == None) or (self.gaze.pupil_right_coords() == None)):
            return False   
        return True
    def run_webcam(self): 
            _, frame = self.webcam.read()
            #cv2.imshow("Demo", frame)
            print(self.is_eye_detected())
    def run_in_loop(self):
        while True:
            self.run_webcam()
            if cv2.waitKey(1) == 27 : 
                break
#pp = QCoreApplication([])              
newClass()
#sys.exit(app.exec_())
