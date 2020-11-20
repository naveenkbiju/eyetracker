import logging
import pickle
from .mouse import Mouse
from .video import Video
class SelfCalibration:
    def __init__(self,video):
        self.video = video
        self.save_count = 0
        self.screen_coords = [] 
        self.pupil_coords = []
        self.mouse = Mouse(self.mouseClicked)
    def app_shortcut(self):
        self.shortcut_close = QShortcut(QKeySequence('Q'), self)
        self.shortcut_close.activated.connect(self.close)
    def close(self):
        self.video.stop_webcam()
        exit(0)        
    def mouseClicked(self, x,y):
        print("mouse clicker " + str(x) + ","  + str(y) )
        if(self.video.is_eye_detected()):
            print("eye_detected")
            x,y = self.video.get_pupil_coords()
            self.screen_coords.append([x,y])
            self.pupil_coords.append([x,y])
            self.save()
    def save(self):
        data = {}
        data['x_train'] = self.screen_coords
        data['y_train'] = self.pupil_coords 
        try :
            pickle.dump(data, open("calibration_data/calibration.p", "wb"))
            self.save_count += 1
        except(IOError):
            logging.error("calibration_data  directory  not found")
        