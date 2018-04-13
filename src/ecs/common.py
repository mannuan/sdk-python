# -*- coding:utf-8 -*-
from flavor import Flavor

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



        //实例化ARIMA模型
        ARIMAModel ARIMA = new ARIMAModel(data);
        ArrayList<int[] > list = new ArrayList<>();

        //进行预测,预测制定次数,每次的值放到数组中
        for (int index = 0; index < predictTimes; index++) {
            //获取模型的参数, p: bestModel[0], q: bestModel[1], AIC: bestModel[2]
            int[] bestModel = ARIMA.getARIMAModel(period, list, (index == 0)? false : true);

            if (bestModel.length == 0){ //当无法获取到合适的参数的时候,用与预测值当天对应的日期的作为预测值
                tempPredictValue[index] = (int)data[data.length - period];
                count++;
                break;
            } else { //获取到合适的参数时,用参数进行预测
                //进行预测,获取预测值
                int differencePredictValue = ARIMA.predictValue(bestModel[0], bestModel[1], period);
                tempPredictValue[index] = ARIMA.afterDealDifference(differencePredictValue, period);
                count++;
            }

            //System.out.println("BestModel: " + bestModel[0] + " " + bestModel[1]);
            //将本次获取的bestModel储存起来,
            list.add(bestModel);
        }

        //求平均,确定预测值
        double summationPredictValue = 0.0;
        for (int index = 0; index < count; index++) {
            summationPredictValue += (double)tempPredictValue[index];
        }

        return (int)Math.round(summationPredictValue / count);
    }

    public static int predictPeriod(String startTime, String endTime){
        /**
         * @method: predictPeriod
         * @param: startDate 开始日期
         * @param: endDate 结束日期
         * @return: int
         * @description: 通过开始日期和结束日期,确定需要预测的周期,以天为单位
         */

        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date startDate = null, endDate = null;

        try {
            startDate = dateFormat.parse(startTime);
            endDate = dateFormat.parse(endTime);
        } catch (ParseException e){
            e.printStackTrace();
        }

        //获取时间间隔,以天为单位
        //向上取整,不足1天,按1天算
        int days = (int)Math.ceil( (endDate.getTime() - startDate.getTime() ) / (1000 * 60 * 60 * 24) );

        //间隔天数,加上当天,等于预测周期数
        //比如:2015-01-01 到 2015-01-07,间隔6天,共需要预测7个点
        return days;
    }

    public static void testData(String testFilePath){
        /**
         * @method: testData
         * @param: testFilePath 测试集文件路径
         * @return: void
         * @description: 统计测试集数据
         */

        String[] testContent = FileUtil.read(testFilePath, null);
        History testData = new History(testContent);
        testData.show();
    }

    public static String[] parseResults(TreeMap<String, List<Integer> > predictResult, Integer length){
        /**
         * @method: parseResult
         * @param: length
         * @return: java.lang.String[]
         * @description: 将结果解析成字符串数组
         */

        String[] results = new String[length];

        //解析预测结果
        int total = 0; //记录预测VM的总数
        int count = 1;
        System.out.println("\n========= 预测结果 ==========");
        for (Map.Entry<String, List<Integer>> entry : predictResult.entrySet()){
            System.out.println(entry.getKey());
            //每一种flavor的总数
            int summation = 0;
            for (Integer value : entry.getValue()){
                summation += value;
                System.out.print(value + " ");
            }
            results[count++] = entry.getKey() + " " + summation;
            total += summation;
            System.out.println("\n===========================");
        }
        results[count] = "";

        //记录总数到结果集
        results[0] = String.valueOf(total);

        return results;
    }

    public static ArrayList<Integer> LRPredict(List<Integer> dataList, int days){
        /**
         * @method: LRPredict
         * @param: dataList
         * @param: days
         * @return: java.util.ArrayList<java.lang.Integer>
         * @description: 利用线性回归进行预测
         */

        //预测的分组,可以调整
        int period = (int)Math.round(days * 2);
        //int period = 10;
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
