from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit,QDialog,QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap,QIcon
import sys
import maVal
import emaVal
import rsiVal
import maTS
import maPlot
tableui = None
tsui = None
loginui = None
welcomeui = None
mainui = None
class LoginUI(QDialog):
    def __init__(self):
        super(LoginUI, self).__init__()
        uic.loadUi("login.ui", self)
        pix = QPixmap("logo.png")
        self.le_logo.setPixmap(pix.scaled(self.le_logo.size()))
        self.btn_login.clicked.connect(self.clickedBtn)
        self.show()
 
 
 
    def clickedBtn(self):
        self.accept()
        welcomeui.exec()
        

class WelcomeUI(QDialog):
    def __init__(self):
        super(WelcomeUI, self).__init__()
        uic.loadUi("welcome.ui", self)
 
        self.btn_go.clicked.connect(self.clickedBtn)
        
    def clickedBtn(self):
        self.accept()
        mainui.show()

class TableUI(QDialog):
    def __init__(self):
        super(TableUI, self).__init__()
        uic.loadUi("table.ui", self)
        w = self.tw_data.width()
        
        self.tw_data.setColumnWidth(0,w/3)
        self.tw_data.setColumnWidth(2,w/3)
        self.tw_data.setColumnWidth(1,w/3)
        self.btn_back.clicked.connect(self.clickedBack)
       
    def clickedBack(self):
        self.accept()
        
class TSUI(QDialog):
    def __init__(self):
        super(TSUI, self).__init__()
        uic.loadUi("ts.ui", self)
        
        self.tw_orders.setColumnWidth(0,40)
        self.tw_orders.setColumnWidth(1,120)
        self.tw_orders.setColumnWidth(2,60)
        self.tw_orders.setColumnWidth(3,70)
        self.tw_orders.setColumnWidth(4,70)
        self.btn_back.clicked.connect(self.clickedBack)

        self.tw_orders.setHorizontalHeaderLabels(['No','Date','Order','Price','MA'])
        self.tw_summary.setColumnWidth(0,150)
        self.tw_summary.setColumnWidth(1,209)
       
    def clickedBack(self):
        self.accept()
class MainUI(QMainWindow):
    def __init__(self):
        
        super(MainUI, self).__init__()
        uic.loadUi("main.ui", self)
        self.btn_ma.clicked.connect(self.clickedMA)
        self.btn_ema.clicked.connect(self.clickedEMA)
        self.btn_rsi.clicked.connect(self.clickedRSI)
        self.btn_strategy.clicked.connect(self.clickedTS)
        self.btn_plot.clicked.connect(self.clickedPlot)
        self.btn_back.clicked.connect(self.clickedBack)
    def clickedBack(self):
        self.hide()
        welcomeui.exec()    
    def clickedPlot(self):
        #calc input params first
        st = self.le_st.text()
        et = self.le_et.text()
        cur = self.le_currency.text()
        dp = int(self.le_dp.text())
        #calc
        maPlot.maPlot(st,et,cur,dp)

    def clickedTS(self):
        #calc input params first
        st = self.le_st.text()
        et = self.le_et.text()
        cur = self.le_currency.text()
        dp = int(self.le_dp.text())
        #calc
        orders,profit = maTS.maTS(st,et,cur,dp)
        id = 0
        bc = sc = 0
        for order in orders:
            id += 1
            if order['action'] == 'Buy':
                bc += 1
            elif order['action'] == 'Sell':
                sc += 1
            rowPosition = tsui.tw_orders.rowCount()
            tsui.tw_orders.insertRow(rowPosition)
            tsui.tw_orders.setItem(rowPosition, 0, QTableWidgetItem(str(id)))
            tsui.tw_orders.setItem(rowPosition, 1, QTableWidgetItem(order['date']) )
            tsui.tw_orders.setItem(rowPosition, 2, QTableWidgetItem(order['action']))
            tsui.tw_orders.setItem(rowPosition, 3, QTableWidgetItem(str(round(order['price'],4))))
            tsui.tw_orders.setItem(rowPosition, 4, QTableWidgetItem(str(round(order['ma'],4))))
        tsui.tw_summary.setItem(0,1, QTableWidgetItem(str(sc)))
        tsui.tw_summary.setItem(1,1, QTableWidgetItem(str(bc)))
        tsui.tw_summary.setItem(2,1, QTableWidgetItem(str(profit)))
        tsui.exec()
    def clickedMA(self):
        tableui.tw_data.setHorizontalHeaderLabels(['Date','Currency Pair Price','SMA'])
        #calc input params first
        st = self.le_st.text()
        et = self.le_et.text()
        cur = self.le_currency.text()
        dp = int(self.le_dp.text())
        #call func
        val = maVal.maVal(st,et,cur,dp)
        size = len(val)
        
        for i in range(size):
            rowPosition = tableui.tw_data.rowCount()
            tableui.tw_data.insertRow(rowPosition)
            tableui.tw_data.setItem(rowPosition, 0, QTableWidgetItem(val[i]['date']))
            tableui.tw_data.setItem(rowPosition, 1, QTableWidgetItem(str(val[i]['cpp'])))
            tableui.tw_data.setItem(rowPosition, 2, QTableWidgetItem(str(round(val[i]['sma'],6))))
        tableui.exec()
    def clickedEMA(self):
        tableui.tw_data.setHorizontalHeaderLabels(['Date','Currency Pair Price','EMA'])
        #calc input params first
        st = self.le_st.text()
        et = self.le_et.text()
        cur = self.le_currency.text()
        dp = int(self.le_dp.text())
        #call func
        val = emaVal.emaVal(st,et,cur,dp)
        size = len(val)
        
        for i in range(size):
            rowPosition = tableui.tw_data.rowCount()
            tableui.tw_data.insertRow(rowPosition)
            tableui.tw_data.setItem(rowPosition, 0, QTableWidgetItem(val[i]['date']))
            tableui.tw_data.setItem(rowPosition, 1, QTableWidgetItem(str(val[i]['cpp'])))
            tableui.tw_data.setItem(rowPosition, 2, QTableWidgetItem(str(round(val[i]['ema'],6))))
        tableui.exec()
    def clickedRSI(self):
        tableui.tw_data.setHorizontalHeaderLabels(['Date','Currency Pair Price','RSI'])
        #calc input params first
        st = self.le_st.text()
        et = self.le_et.text()
        cur = self.le_currency.text()
        dp = int(self.le_dp.text())
        #call func
        val = rsiVal.rsiVal(st,et,cur,dp)
        size = len(val)
        
        for i in range(size):
            rowPosition = tableui.tw_data.rowCount()
            tableui.tw_data.insertRow(rowPosition)
            tableui.tw_data.setItem(rowPosition, 0, QTableWidgetItem(val[i]['date']))
            tableui.tw_data.setItem(rowPosition, 1, QTableWidgetItem(str(val[i]['cpp'])))
            tableui.tw_data.setItem(rowPosition, 2, QTableWidgetItem(str(round(val[i]['rsi'],6))))
        tableui.exec()    

# val = maVal.maVal()
app = QApplication(sys.argv)
loginui = LoginUI()
welcomeui = WelcomeUI()
mainui = MainUI()
tableui = TableUI()
tsui = TSUI()

ret = loginui.exec()
# if ret == QDialog.Accepted:
#     welcomeui = WelcomeUI()
#     ret1 = welcomeui.exec()
#     if (ret1 == QDialog.Accepted):
#         mainui = MainUI()
#         mainui.show
app.exec_()