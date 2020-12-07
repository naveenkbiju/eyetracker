from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier 

models = {"LR" : LinearRegression , "RFC" : RandomForestClassifier}
def getModel(model):
    return models[model]
def list_models():
    return [name for name , _ in models.items()]   