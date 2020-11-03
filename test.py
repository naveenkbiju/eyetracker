from PyQt5.QtWidgets import QApplication
import sys
from eyetracker import EyeTracker

e = EyeTracker()
e.train()

print(e.predict(100,120))
print("complete")
