from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Python ")
        self.showFullScreen()
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(palette)
        self.ht = self.height()
        self.wt = self.width()
        print(str(self.ht)+ str(self.wt))
        self.UiComponents()
        self.show()
        self.data = {}
        self.check = []
        self.c = 0;
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
                button[k].setStyleSheet("border-radius :15;border: 1px solid white")
                button[k].clicked.connect(self.calib(k+1,x,y))
                button[k].show()
                k=k+1

    def calib(self, k,x,y):
        def add_data():
            self.data[k] = (x,y)
            print(k)
            if k not in self.check:
                self.c= self.c+1
                self.check.append(k)
            if(self.c ==  9 ):
                print("calibration completed")
                print(self.data)
                sys.exit()
        return add_data

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())