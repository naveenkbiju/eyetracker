import logging
import math
class AccuracyTest(object):
    def __init__(self):
        self.data = None
    def compare(self , data ,centerpoint, windowHeight):
        rez = [[data[j][i] for j in range(len(data))] for i in range(len(data[0]))]
        return [str(self.checkAccuracy(d , centerpoint , windowHeight) ) for d in rez]
    def checkAccuracy(self,data , point,windowHeight):
        self.data = data 
        if self.data is None:
            logging.error("data cannot be none")
            return
        startingPointX,startingPointY = point
        count , precisionPercentages = 0 , 0
        for i in self.data:
                x,y = i
                xDiff = startingPointX  - x
                yDiff = startingPointY - y
                halfWindowHeight = windowHeight/2
                distance = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))
                precision = 0
                if distance <= halfWindowHeight and distance > -1 :
                    precision = 100 - (distance/halfWindowHeight *100)
                elif distance  > halfWindowHeight :
                    precision = 0
                elif(distance > -1):
                    precision = 100
                precisionPercentages += precision
                count += 1
                
        return round(precisionPercentages/count , 2)                