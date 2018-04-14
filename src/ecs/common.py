# -*- coding:utf-8 -*-
from __future__ import division
from flavor import Flavor
from arimamodel import ARIMAModel
import time,math

class Common(object):

    '''
    inputContent : [str]
    flavorList : Flavor
    '''
    def parseInput(self, inputContent, flavorList):
        input = dict()
        temp = inputContent[0].split(' ')
        if len(temp) > 0:
            value1 = [temp[0]]
            input.setdefault('cpu', value1)

            value2 = [temp[1]]
            input.setdefault('memory', value2)

            value3 = [temp[2]]
            input.setdefault('disk',value3)

        value4 = [inputContent[2]]
        input.setdefault('numberOfFlavor', value4)

        value5 = list()
        numberOfFlavor = int(inputContent[2])
        for index in range(numberOfFlavor):
            temp = inputContent[3 + index].split(' ')
            value5.append(temp[0])
            flavorList.setFlavor(temp[0], int(temp[1]), int(temp[2]))
        input.setdefault("flavors", value5)

        value6 = [inputContent[numberOfFlavor + 4]]
        input.setdefault("type", value6)

        if len(inputContent[numberOfFlavor + 6].split(' ')) > 0:
            value7 = [inputContent[numberOfFlavor + 6].split(' ')[0]]
            input.setdefault('start',value7)

        if len(inputContent[numberOfFlavor + 7].split(' ')) > 0:
            value8 = [inputContent[numberOfFlavor + 7].split(' ')[0]]
            input.setdefault("end", value8)

        return input

    #dataList : [int]
    #days : int
    def rollingPredict(self, dataList, days):
        predictResult = list()
        data = [len(dataList) + days]
        for index in range(len(dataList)):
            data[index] = dataList[index]

        for index in range(days):
            predictValue = self.singlePointPredict(data, days)
            if predictValue < 0:
                predictValue = 0
            predictResult.append(predictValue)
            data[len(dataList) + index] = predictValue
        return predictResult

    #data : [float]
    #days : int
    def singlePointPredict(self, data, days):
        period = 17
        predictTimes = 5000
        count = 0
        tempPredictValue = [0]*predictTimes
        ARIMA = ARIMAModel(data)
        _list = []
        for index in range(predictTimes):
            bestModel = ARIMA.getARIMAModel(period, list, (lambda x:False if x==0 else True)(index))
            if len(bestModel) == 0:
                tempPredictValue[index] = int(data[data.length - period])
                count += 1
                break
            else:
                differencePredictValue = ARIMA.predictValue(bestModel[0], bestModel[1], period)
                tempPredictValue[index] = ARIMA.afterDealDifference(differencePredictValue, period)
                count += 1
            _list.append(bestModel)
        summationPredictValue = 0.0
        for index in range(count):
            summationPredictValue += float(tempPredictValue[index])
        return int(round(summationPredictValue / count))

    #startTime : str
    #endTime : str
    def predictPeriod(self, startTime, endTime):

        dateFormat = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        startDate = None
        endDate = None
        try:
            startDate = time.mktime(time.strptime(startTime, "%Y-%m-%d"))
            endDate = time.mktime(time.strptime(endTime, "%Y-%m-%d"))
        except Exception as e:
            print e
        days = int(math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)))
        return days
    #testFilePath : str
    def testData(self):
        pass

    #predictResult : TreeMap<String, List<Integer> >
    #length : int
    def parseResults(self, predictResult, length):
        results = ['']*length
        total = 0
        count = 1
        print "\n========= 预测结果 =========="
        for entry in predictResult.items():
            print entry[0]
            summation = 0
            for value in entry[1]:
                summation += value
                print value + " "
            count += 1
            results[count] = str(entry[0]) + ' ' +str(summation)
            total += summation
            print '\n==========================='
        results[count] = ""
        results[0] = str(total)
        return results
    #dataList : [int]
    #days : int
    def LRPredict(self, dataList, days):
        period = int(round(days * 2))


        //参数:训练数据集, 分组周期, 迭代次数, 迭代步长, 每次迭代使用的样本数量, 损失阈值
        LinearRegression LR = new LinearRegression(dataList, period, 100000,
                                                    0.01, 2, 0.0001);
        LR.trainModel();
        ArrayList<Integer> predictList = LR.predict(dataList, days);

        return predictList;
    }

    public static ArrayList<Integer> weightedAverage(ArrayList<Integer> listARIMA, ArrayList<Integer> listLR){
        /**
         * @method: weightedAverage
         * @param: listARIMA
         * @param: listLR
         * @return: java.util.ArrayList<java.lang.Integer>
         * @description: 求ARIMA预测和LR预测的结果的加权
         */
        //权值,可以调整=
        double weight = 0.8;
        ArrayList<Integer> average = new ArrayList<>();

        if(listARIMA.size() == listLR.size()){
            for (int index = 0; index < listARIMA.size(); index++) {
                int temp = (int)Math.round(weight * listARIMA.get(index) + (1 - weight) * listLR.get(index));
                average.add(temp);
            }
        }

        return average;
    }

}
