import numpy as np
from sklearn.linear_model import LinearRegression
import logging
import pickle
from .Classifier import *
from sklearn.model_selection import train_test_split


class GazePredict:
    def __init__(self , model):
        self.is_trained = False
        self.model = model
    def load_data(self ,filename):
        return pickle.load(open(filename, 'rb'))
    def train(self,filename = "calibration.p"):
        data = self.load_data(filename)
        x_train = data['x_train']
        y_train = data['y_train']
        x_train,x_test , y_train , y_test = train_test_split(x_train,y_train)
        self.reg = getModel(self.model)().fit(x_train, y_train)
        self.is_trained = True
        return self
    def predict(self,x1,y1,x2,y2):
        if self.is_trained :
            coords = self.reg.predict([[x1,y1,x2,y2]])
            return coords[0][0] , coords[0][1]
        logging.error("You Need to Train the Model before Predict")
        return None
