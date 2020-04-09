
from poloniex import poloniex
import datetime 
from datetime import date 
import time
from poloniex import Poloniex

def rsiVal(st,et,cur,dp):
	currency=cur
	period=86400
	periodDays = dp

	startTime = time.mktime(datetime.datetime.strptime(st, "%Y/%m/%d").timetuple())
	endTime = time.mktime(datetime.datetime.strptime(et, "%Y/%m/%d").timetuple())
	

	connection = Poloniex("343DL7SG-Z5FLTLRU-W72O0KVT-OH3GZSET","a53e8a0defdd21398547fd4a33f64b80555ae4c3f6704c8b6f0602c05dfbcea459be7af7de9449a28c14c51a2e50b6bba70c7f90ab318293e16ab9241a374ace")
	historicalData = connection.returnChartData(currency,period,startTime,endTime)
	
	numOfRSIs = len(historicalData) - periodDays + 1

	#1 getDates
	xDatesPlot = []
	cPricesPlot = []
	for x in historicalData:
		xDatesPlot.append(x['date'])
		cPricesPlot.append(x['close'])
	
	datesConv = []
	size = len(xDatesPlot)
	for i in range(size):
		dates = xDatesPlot[i] + period
		dates1 = datetime.datetime.fromtimestamp(int(dates)).strftime('%Y-%m-%d ')
		datesConv.append(dates1)
		
	#2 check the formula you want to use and adjust data to fit the formula e.g. you need price get the price from data
	closedUp=[]  
	closedDown=[]

	for data in historicalData: 
		if data['open']>data['close']:
			closedDown.append(data['open']-data['close'])
			closedUp.append(0)
		else:
			closedUp.append(data['close']-data['open'])
			closedDown.append(0)


	#3 once you get data right and once you have every part of the equation e.g. v=s/t in order to calculate it you need road lenght and time 
	#formulate the equation and count what you need 
	rsi = []
	for i in range(numOfRSIs):
		#calculate every RSIs
		avg_loss = 0.0
		avg_gain = 0.0
		for j in range(periodDays):
			index = j + i
			avg_loss += closedDown[index]
			avg_gain += closedUp[index]
		avg_loss /= periodDays
		avg_gain /= periodDays

		#calculate RSI
		RSI = 0
		if avg_loss == 0: 
			RSI = 100
		else:
			RSI = 100 - (100 / ( 1 + avg_gain/avg_loss))
		#print RSI
		rsi.append(RSI)
		index = i + periodDays - 1
		#print('For date' + str(datesConv[index]) + "The RSI is ")
		#print(RSI)
	ret = []	
	for a in range(numOfRSIs):
		index = a + periodDays - 1
		one = dict()
		one['date'] = str(datesConv[index])
		one['cpp'] = cPricesPlot[index]
		one['rsi'] = rsi[a]
		ret.append(one)
	return ret
# print(rsiVal('2019/1/1','2020/2/1'))