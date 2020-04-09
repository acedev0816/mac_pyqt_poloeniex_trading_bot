
from poloniex import Poloniex
import datetime 
from datetime import date 
import time

def maTS(st, et,cur,dp):
	currency=cur
	period=86400
	periodDays = dp

	startTime = time.mktime(datetime.datetime.strptime(st, "%Y/%m/%d").timetuple())
	endTime = time.mktime(datetime.datetime.strptime(et, "%Y/%m/%d").timetuple())


	connection = Poloniex("343DL7SG-Z5FLTLRU-W72O0KVT-OH3GZSET","a53e8a0defdd21398547fd4a33f64b80555ae4c3f6704c8b6f0602c05dfbcea459be7af7de9449a28c14c51a2e50b6bba70c7f90ab318293e16ab9241a374ace")


	sellOrders = 0
	buyOrders=0
	
	sellPrices = []
	buyPrices = []

	current_MA = 0	
	movingAvgs = []

	historicalData = connection.returnChartData(currency,period,startTime,endTime)
	

	cPrices = []
	for c in historicalData:
		cPrices.append(c['close']) #closing prices for all days in period 


	
	datesConv=[]
	for d in historicalData:
		dates = d['date'] + period
		dates1 = datetime.datetime.fromtimestamp(int(dates)).strftime('%Y-%m-%d')
		datesConv.append(dates1)

	
	#calculate number of mas
	countofMA = len(historicalData) - periodDays + 1 #How many moving averages will be generated according to values derived from API according to start time to end time 
	if(countofMA < 1):
		return [],0,0,0
	orders = []	
	#from now calculate
	for i in range(countofMA): #First Loop i indicating moving average index, 0 start
												
		s = 0.0
		xPrices = []
		for j in range(periodDays): #j is the calculated price in index 
			index = i + j																																		
			xPrices.append(cPrices[index]) #prices added to xPrices list
			s = s + cPrices[index] #Adds up the values in cPrices according to sizeofMA

		current_day = datesConv[i+periodDays-1] 																																																																								
		movingAvgs.append(s/periodDays)
		current_MA = movingAvgs[-1]
		priceNow = xPrices[-1]	
		lastPrice = xPrices[-2]

		order = dict()
		order['date'] = current_day
		order['price'] = priceNow
		order['ma'] = current_MA

		if ((priceNow > current_MA) and (priceNow < lastPrice)):
			# print("Sell Order at ", current_day,  " [Current Price:" , priceNow, " MA:",current_MA,"]")
			order['action'] = 'Sell'

		elif ((priceNow<current_MA) and (priceNow > lastPrice)):
			# print("Buy Order at ", current_day, " [Current Price:" , priceNow, " MA:",current_MA,"]")
			order['action'] = 'Buy'						

		else:
			order['action'] = 'Exit'
		orders.append(order)
	finalPrice = cPrices[-1]
	
		
	# print("Total sellOrders " + str(sellOrders))
	# print("Total buyOrders " + str(buyOrders))
	sellTotal = 0
	buyTotal = 0
	sellOrders = 0
	buyOrders = 0	
	for order in orders:
		if order['action'] == 'Sell':
			sellTotal+= order['price']
			sellOrders += 1
		if order['action'] == 'Buy':
			buyTotal+= order['price']
			buyOrders += 1
	
	profit = 0.0

	if sellOrders > buyOrders:
		diff = sellOrders - buyOrders
		buyBack = diff * finalPrice
		profit = sellTotal - buyTotal - buyBack
	else:
		diff = buyOrders - sellOrders
		sellBack = diff * finalPrice
		profit = sellTotal - buyTotal + sellBack
	return orders,profit
# orders,profit = maTS('2019/4/1','2019/4/20','BTC_ETH',14)
# print(orders,profit)


