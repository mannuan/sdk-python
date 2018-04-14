# -*- coding:utf-8 -*-
import sys
from mamodel import MAModel
from armodel import ARModel
from armamodel import ARMAModel
from generalmethod import GeneralMethod
import math

class ARIMAModel(object):

    #data : [float]
    def __init__(self, data):
        self.data = data
        self.coefficientARIMA = list()

    #preData : [float]
    def preFirstDifference(self, preData):
        tempData = [0]*(len(preData)-1)
        for index in range(len(preData)):
            tempData[index] = preData[index+1] - preData[index]
        return tempData

    #preData : [float]
    #period : int
    def preSeasonDifference(self, preData, period):
        tempData = [0]*(len(preData) - period)
        for index in range(len(preData) - period):
            tempData[index] = preData[index + period] - preData[index]
        return tempData

    #period : int
    def preDealdifference(self, period):
        if period >= len(self.data)-1:
            period = 0

        if period == 0:
            return self.data
        elif period == 1:
            return self.preFirstDifference(self.data)
        else:
            return self.preSeasonDifference(self.data, period)

    #period : int
    #notModel : [[int]]
    #needNot : boolean
    def getARIMAModel(self, period, notModel, needNot):
        dataAfterDifference = self.preDealdifference(period)
        minAIC = sys.float_info.max
        bestModel = [0]*3
        type = 0
        coefficient = None
        length = len(dataAfterDifference)
        if length > 5:
            length = 5
        size = ((length + 2) * (length + 1)) / 2 - 1
        model = [[0]*size]*2
        count = 0
        for index_i in range(length+1):
            for index_j in range(length-index_i):
                if index_i == 0 and index_j == 0:
                    continue
                model[count][0] = index_i
                count += 1
                model[count][1] = index_j
        for index_i in range(len(model)):
            token = False
            if needNot:
                for index_j in range(len(notModel)):
                    if model[index_i][0] == notModel[index_i][0] and \
                            model[index_i][1] == notModel[index_j][1]:
                        token = True
                        break
            if token:
                continue
            if model[index_i][0] == 0:
                MA = MAModel(dataAfterDifference, model[index_i][1])
                coefficient = MA.coefficientMR()
                type = 1
            elif model[index_i][1] == 0:
                AR = ARModel(dataAfterDifference, model[index_i][0])
                coefficient = AR.coefficientAR()
                type = 2
            else:
                ARMA = ARMAModel(dataAfterDifference, model[index_i][0], model[index_i][1])
                coefficient = ARMA.coefficientARMA()
                type = 3
            aic = GeneralMethod().getModelAIC(coefficient, dataAfterDifference, type)
            try:
                float(aic)
            except Exception:
                minAIC = aic
                bestModel[0] = model[index_i][0]
                bestModel[1] = model[index_i][1]
                bestModel[2] = round(minAIC)
                self.coefficientARIMA = coefficient
        return bestModel

    #predictValue : int
    #period : int
    def afterDealDifference(self, predictValue, period):
        if period >= len(self.data):
            period = 0
        if period == 0:
            return predictValue
        elif period == 1:
            return int(predictValue + self.data[len(self.data) - 1])
        else:
            return int(predictValue + self.data[len(self.data) - period])

    def predictValue(self, p, q, period):
        dataAfterDifference = self.preDealdifference(period)
        length = len(dataAfterDifference)
        predict = 0
        tempAR = 0.0
        tempMA = 0.0
        errorData = [0.0]*(q+1)
        random = None
        if p == 0:
            coefficientMA = self.coefficientARIMA[0]
            for index_i in range(len(q,length)):
                tempMA = 0
                for index_j in range(1,q+1):
                    tempMA += coefficientMA[index_j] * errorData[index_j]
                for index_j in range(1,q+1)[::-1]:
                    errorData[index_j] = errorData[index_j - 1]
                errorData[0] = random.nextGaussian() * math.sqrt(coefficientMA[0])
            predict = int(tempMA)
        elif(q==0):
            coefficientAR = self.coefficientARIMA[0]
            for index_i in range(p,length):
                tempAR = 0
                for index_j in range(p):
                    tempAR += coefficientAR[index_j] * dataAfterDifference[index_i - index_j - 1]
            predict = int(tempAR)
        else:
            coefficientAR = self.coefficientARIMA[0]
            coefficientMA = self.coefficientARIMA[1]
            for index_i in range(p,length):
                tempAR = 0
                tempMA = 0
                for index_j in range(p):
                    tempAR += coefficientAR[index_j] * dataAfterDifference[index_i - index_j - 1]
                for index_j in range(1,q+1):
                    tempMA += coefficientMA[index_j] * errorData[index_j]
                for index_j in range(1,q+1)[::-1]:
                    errorData[index_j] = errorData[index_j - 1]
                errorData[0] = random.nextGaussian() * math.sqrt(coefficientMA[0])
            predict = int(tempAR + tempMA)
        return predict