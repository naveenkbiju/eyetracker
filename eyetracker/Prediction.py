import numpy as np
from sklearn.linear_model import LinearRegression
import logging
import pickle
from sklearn.model_selection import train_test_split

class GazePredict:
    def __int__(self):
        self.is_trained = False
    def train(self,data):
        x_train = data['x_train']
        y_train = data['y_train']
        x_train,x_test , y_train , y_test = train_test_split(x_train,y_train)
        self.reg = LinearRegression().fit(x_train, y_train)
        self.is_trained = True
    def predict(self,x1,y1,x2,y2):
        if self.is_trained :
           return self.reg.predict([[x1,y1,x2,y2]])
        logging.error("You Need to Train the Model before Predict")
