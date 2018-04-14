# -*- coding:utf-8 -*-
from generalmethod import GeneralMethod

class ARModel(object):
    #data : [float]
    #p : int
    def __init__(self, data, p):
        self.data = data
        self.p = p

    def coefficientAR(self):
        vector = list()
        coefficientAR = self.coefficientOfAR(self.data, self.p)
        vector.append(coefficientAR)
        return vector

    #data : [float]
    #p : int
    def coefficientOfAR(self, data, p):
        coefficient = [0]*(p+1)
        method = GeneralMethod()
        covariance = method.autocorrelationCoefficient(data, p)
        result = method.LevinsonSolve(covariance)
        for index in range(p):
            coefficient[index] = result[p][index + 1]
        coefficient[p] = result[0][p]
        return coefficient
