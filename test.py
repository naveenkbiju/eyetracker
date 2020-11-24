import sys
from eyetracker import EyeTracker

e = EyeTracker()
e.start()
e.load_calibration_model()
