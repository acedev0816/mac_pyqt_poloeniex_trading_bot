#Calculation of Exponential Moving Average 
from poloniex import Poloniex
import datetime
import time
from datetime import date 

def emaVal(st,et,cur,dp):
    currency= cur
    period = 86400
    startTime = time.mktime(datetime.datetime.strptime(st, "%Y/%m/%d").timetuple())
    endTime = time.mktime(datetime.datetime.strptime(et, "%Y/%m/%d").timetuple())

    sizeOfMA = dp
    connection = Poloniex("343DL7SG-Z5FLTLRU-W72O0KVT-OH3GZSET","a53e8a0defdd21398547fd4a33f64b80555ae4c3f6704c8b6f0602c05dfbcea459be7af7de9449a28c14c51a2e50b6bba70c7f90ab318293e16ab9241a374ace")
    historicalData = connection.returnChartData(currency,period,startTime,endTime)
    countofMA = len(historicalData) - sizeOfMA + 1 


    startTimeConv = datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S')
    endTimeConv = datetime.datetime.fromtimestamp(int(endTime)).strftime('%Y-%m-%d %H:%M:%S')

    dataPoints = len(historicalData)
    datesP = dataPoints - countofMA
										
    # print("Exponential Moving Averages displayed from " + str(startTimeConv) + " To " + str(endTimeConv))

    cPricesPlot = []
    for c in historicalData:
	    cPricesPlot.append(c['close'])

    xDatesPlot = []
    for x in historicalData:
        xDatesPlot.append(x['date'])

    datesConv = []
    size = len(xDatesPlot)
    for i in range(size):
        dates = xDatesPlot[i] + period
        dates1 = datetime.datetime.fromtimestamp(int(dates)).strftime('%Y-%m-%d ')
        datesConv.append(dates1)
    movingAvgs = []
    multiplier = 1/(sizeOfMA+1)
    for i in range(countofMA): #First Loop i indicating moving average index 													
        s = 0.0
        for j in range(sizeOfMA): #j is the calculated price in index 
            index = i + j
            if j==0:
                s = cPricesPlot[index]
                continue
            s = cPricesPlot[index] * multiplier + s*(1-multiplier) #Adds up the values in cPrices according to sizeofMA
        movingAvgs.append(s)

    ret = []	
    for a in range(countofMA):
        index = a + sizeOfMA - 1
        one = dict()
        one['date'] = str(datesConv[index])
        one['cpp'] = cPricesPlot[index]
        one['ema'] = movingAvgs[a]
        ret.append(one)
    return ret
# print(emaVal('2019/4/20','2019/5/16'))


