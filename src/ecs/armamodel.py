# -*- coding:utf-8 -*-
from generalmethod import GeneralMethod
import math

class ARMAModel(object):
    #data : [float]
    #p : int
    #q : int
    def __init__(self, data, p, q):
        self.data = data
        self.p = p
        self.q = q

    def coefficientARMA(self):
        vector = list()
        coefficientARMA = self.coefficientOfARMA(self.data, self.p, self.q)
        coefficientAR = [0]*(self.p+1)
        coefficientAR = coefficientARMA
        coefficientMA = [0]*(self.q+1)
        coefficientMA = coefficientARMA[self.p+1:]
        vector.append(coefficientAR)
        vector.append(coefficientMA)
        return vector


    def coefficientOfARMA(self, data, p, q):
        method = GeneralMethod()
        allCovariance = method.autocorrelationCoefficient(data, p + q)
        covariance = [0.0]*(p+1)
        for index in range(len(covariance)):
            covariance[index] = allCovariance[q + index]
        ARResult = method.LevinsonSolve(covariance)
        coefficientAR = ARResult[0.0]*(p+1)
        for index in range(p):
            coefficientAR[index] = ARResult[p][index + 1]
        coefficientAR[p] = ARResult[0][p]
        alpha = [0.0]*(p + 1)
        alpha[0] = -1
        for index in range(1,p+1):
            alpha[index] = coefficientAR[index - 1]
        paraGarma = [0.0]*(q+1)
        for index_k in range(q+1):
            summation = 0.0
            for index_i in range(p+1):
                for index_j in range(p+1):
                    summation += alpha[index_i] * alpha[index_j]\
                    *allCovariance[abs(index_k + index_i - index_j)]
            paraGarma[index_k] = summation
        MAResult = method.LevinsonSolve(paraGarma)
        coefficientMA = [0.0]*(q+1)
        for index in range(q+1):
            coefficientMA[index] = MAResult[q][index]
        coefficientMA[0] = MAResult[0][q]
        coefficientARMA = [0.0]*(p+q+2)
        for index in range(len(coefficientARMA)):
            if index < len(coefficientAR):
                coefficientARMA[index] = coefficientAR[index]
            else:
                coefficientARMA[index] = coefficientMA[index - coefficientAR.length]
        return coefficientARMA