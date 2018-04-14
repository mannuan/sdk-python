# -*- coding:utf-8 -*-
from __future__ import division
import math

class GeneralMethod(object):

    #data : [float]
    def averageValue(self, data):
        summation = 0.0
        for index in range(len(data)):
            summation += data[index]
        return summation / len(data)

    #data : [float]
    def varianceValue(self, data):
        variance = 0.0
        average = self.averageValue(data)
        if len(data) <= 1:
            return 0.0
        for index in range(len(data)):
            variance += (data[index] - average) * (data[index] - average)
        return variance / (data.length - 1)

    #data : [float]
    def standardDeviationValue(self, data):
        return math.sqrt(self.varianceValue(data))

    #data : [float]
    #order : int
    def autocorrelationCoefficient(self, data, order):
        autocorrelationCoefficient = [0]*(order+1)
        average = self.averageValue(data)
        for interval in range(order + 1):
            autocorrelationCoefficient[interval] = 0.0
            for index in range(len(data) - interval):
                autocorrelationCoefficient[interval] += (data[index + interval] - average)*\
                                                        (data[index] - average)
            autocorrelationCoefficient[interval] /= (len(data) - interval)
        return autocorrelationCoefficient

    #covariance : [float]
    def LevinsonSolve(self, covariance):
        order = len(covariance) - 1
        result = [[0]*(order+1)]*(order+1)
        sigmaSq = [0]*(order+1)
        sumTop = None
        sumSub = None
        sigmaSq[0] = covariance[0]
        result[1][1] = covariance[1] / sigmaSq[0]
        sigmaSq[1] = sigmaSq[0] * (1.0 - result[1][1] * result[1][1])
        for index_i in range(1,order):
            sumTop = 0.0
            sumSub = 0.0
            for index_j in range(1, index_i+1):
                sumTop += covariance[index_i + 1 - index_j] * result[index_i][index_j]
                sumSub += covariance[index_j] * result[index_i][index_j]
            result[index_i + 1][index_i + 1] = (covariance[index_i + 1] - sumTop) / (covariance[0] - sumSub)
            for index_k in range(1, index_i+1):
                result[index_i + 1][index_k] = result[index_i][index_k] - result[index_i + 1][index_i + 1]\
                *result[index_i][index_i + 1 - index_k]
            sigmaSq[index_i + 1] = sigmaSq[index_i] * (1.0 - result[index_i + 1][index_i + 1]\
                                                       * result[index_i + 1][index_i + 1])
        result[0] = sigmaSq
        return result

    #vector : []
    #data : [float]
    #type : int
    def getModelAIC(self, vector, data, type):
        length = data.length
        p = 0
        q = 0
        tempAR = None
        tempMA = None
        summationError = 0.0
        random = None
        if type == 1:
            coefficientMA = vector[0]
            q = len(coefficientMA)
            errorData = [0]*q
            for index_i in range(q-1, length):
                tempMA = 0.0
                for index_j in range(1,q):
                    tempMA += coefficientMA[index_j] * errorData[index_j]
                for index_j in range(q)[::-1]:
                    errorData[index_j] = errorData[index_j - 1]
                errorData[0] = random.nextGaussian() * math.sqrt(coefficientMA[0])
                summationError += (data[index_i] - tempMA) * (data[index_i] - tempMA)
            return (length - (q - 1)) * math.log(summationError / (length - (q - 1))) + (q + 1) * 2
        elif type == 2:
            coefficientAR = vector[0]
            p = len(coefficientAR)
            for index_i in range(p-1,length):
                tempAR = 0.0
                for index_j in range(p-1):
                    tempAR += coefficientAR[index_j] * data[index_i - index_j - 1]
                summationError += (data[index_i] - tempAR) * (data[index_i] - tempAR)
            return (length - (p - 1)) * math.log(summationError / (length - (p - 1))) + (p + 1) * 2
        else:
            coefficientAR = vector[0]
            coefficientMA = vector[1]
            p = len(coefficientAR)
            q = len(coefficientMA)
            errorData = [0]*q
            for index_i in range(p-1,length):
                tempAR = 0.0
                for index_j in range(p-1):
                    tempAR += coefficientAR[index_j] * data[index_i - index_j - 1]
                tempMA = 0.0
                for index_j in range(1,q):
                    tempMA += coefficientMA[index_j] * errorData[index_j]
                for index_j in range(q)[::-1]:
                    errorData[index_j] = errorData[index_j - 1]
                errorData[0] = random.nextGaussian() * math.sqrt(coefficientMA[0])
                summationError += (data[index_i] - tempAR - tempMA) * (data[index_i] - tempAR - tempMA)
            return (length - (q + p - 1)) * math.log(summationError / (length - (q + p - 1))) + (p + q) * 2