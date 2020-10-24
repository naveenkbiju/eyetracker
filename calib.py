from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python ")
        self.showFullScreen()
        self.data = {}
        self.check = []
        self.c = 0;
        self.re = []
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)
        self.ht = self.height()
        self.wt = self.width()
        print(str(self.ht)+ str(self.wt))
        self.UiComponents()
        self.shortcut_close = QShortcut(QKeySequence('Q'), self)
        self.shortcut_close.activated.connect(self.closeApp)
        self.show()
    def UiComponents(self):
        button = []
        k=0
        half_ht = int((self.ht-30) /2)
        half_wt = int((self.wt-30)/ 2)
        for i in range(3):
            for j in range(3):
                x = j*half_wt
                y = i*half_ht
                button.append(QPushButton(str(k+1), self))
                button[k].setGeometry(x,y , 30, 30)
                button[k].setStyleSheet(open('buttonStyle.css').read())
                button[k].clicked.connect(self.calib(button ,k+1,x,y))
                button[k].show()
                self.re.append(0)
                k=k+1

    def calib(self,button ,k,x,y):
        def add_data():
            if(self.re[k-1] != 5):
                self.re[k-1] = self.re[k-1] + 1
            else:
                button[k-1].setStyleSheet("background-color: red")
                self.data[k] = (x, y)
                print(k)
                if k not in self.check:
                    self.c = self.c + 1
                    self.check.append(k)
                if (self.c == 9):
                    print("calibration completed")
                    print(self.data)
                    sys.exit()
        return add_data

    def closeApp(self):
        App.quit()
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
