# -*- coding:utf-8 -*-
from __future__ import division
import math
from generalmethod import GeneralMethod

class MAModel(object):
    #data : [float]
    #q : int
    def __init__(self, data, q):
        self.data = list()
        self.q = None

    #data : [float]
    #q : int
    def coefficientMR(self):
        vector = list()
        coefficientMR = self.coefficientOfMR(self.data, self.q)
        vector.append(coefficientMR)
        return vector

    #data : [float]
    #q : int
    def coefficientOfMR(self, data, q):
        p = math.log(len(data))
        method = GeneralMethod()
        covariance = method.autocorrelationCoefficient(data, p)
        result = method.LevinsonSolve(covariance)
        alpha = [0]*(p+1)
        for index in range(1,p+1):
            alpha[index] = result[p][index]
        paraGrama = [0]*(q+1)
        for index_i in range(q+1):
            summation = 0.0
            for index_j in range(p-index_i):
                summation += alpha[index_j] * alpha[index_i + index_j]
            paraGrama[index_i] = summation / result[0][p]
        temp = method.LevinsonSolve(paraGrama)
        coefficientMR = [0]*(q+1)
        for index in range(len(coefficientMR)):
            coefficientMR[index] = -temp[q][index]

        coefficientMR[0] = 1 / temp[0][q]
        return coefficientMR
