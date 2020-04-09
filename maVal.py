import matplotlib
import matplotlib.pyplot as plt

import datetime
import time
from datetime import date 
from poloniex import Poloniex
def maVal(st, et,cur,dp):
	currency= cur
	
	period=86400
	startTime = time.mktime(datetime.datetime.strptime(st, "%Y/%m/%d").timetuple())
	endTime = time.mktime(datetime.datetime.strptime(et, "%Y/%m/%d").timetuple())

	sizeOfMA = dp
	connection = Poloniex("343DL7SG-Z5FLTLRU-W72O0KVT-OH3GZSET","a53e8a0defdd21398547fd4a33f64b80555ae4c3f6704c8b6f0602c05dfbcea459be7af7de9449a28c14c51a2e50b6bba70c7f90ab318293e16ab9241a374ace")
	
	historicalData = connection.returnChartData(currency,period,startTime,endTime)
	dataPoints = len(historicalData)
	countofMA = len(historicalData) - sizeOfMA + 1 

	cPricesPlot = []
	for c in historicalData:
		cPricesPlot.append(c['close'])

	xDatesPlot = []
	for x in historicalData:
		xDatesPlot.append(x['date'])

	datesConv = []
	
	size = len(xDatesPlot)
	for a in range(size):
		dates = xDatesPlot[a] + period
		dates1 = datetime.datetime.fromtimestamp(int(dates)).strftime('%Y-%m-%d ')
		datesConv.append(dates1)
	
	movingAvgs = []
	for a in range(countofMA): #First Loop i indicating moving average index 
		s = 0.0
		for j in range(sizeOfMA): #j is the calculated price in ath index 
			index = a + j																																		
			s = s + cPricesPlot[index] #Adds up the values in cPrices according to sizeofMA
		movingAvgs.append(s/sizeOfMA)


	ret = []	
	for a in range(countofMA):
		index = a + sizeOfMA - 1
		one = dict()
		one['date'] = str(datesConv[index])
		one['cpp'] = cPricesPlot[index]
		one['sma'] = movingAvgs[a]
		ret.append(one)
	return ret

