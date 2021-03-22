#!/usr/bin/env python3

from PyQt5 import QtWidgets, uic, QtCore
from mcstatus import MinecraftServer
import sys
import pyqtgraph as pg
from random import randint
#added for matplotlib implementation
#from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')

MAINWINDOWUI = 'ui/interface.ui'
ERRORDIALOGUI = 'ui/error.ui'
WIDTH = 800
HEIGHT = 760
REDUCEDHEIGHT = 333

x = [0]

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(MAINWINDOWUI, self)
            
        #windowSize
        self.WINDOWSTATUS = 'REDUCED'
        self.setFixedSize(WIDTH, REDUCEDHEIGHT)
        
        #insertButton
        self.insertButton = self.findChild(QtWidgets.QPushButton, 'insertButton')  #search for insertButton widget
        self.insertButton.clicked.connect(self.insertButtonCmd)  #exec insertButtonCmd when insertButton clicked

        #removeButton
        self.removeButton = self.findChild(QtWidgets.QPushButton, 'removeButton')  #search for removeButton widget
        self.removeButton.clicked.connect(self.removeButtonCmd)  #exec removeButtonCmd when removeButton clicked
        
        #refreshButton
        self.refreshButton = self.findChild(QtWidgets.QPushButton, 'refreshButton')
        self.refreshButton.clicked.connect(self.serverStatusCmd)
        
        #queryButton
        self.queryButton = self.findChild(QtWidgets.QPushButton, 'queryButton')
        self.queryButton.clicked.connect(self.queryCmd)
        
        #serverInput
        self.serverInput = self.findChild(QtWidgets.QLineEdit, 'serverInput')  #search for serverInput widget

        #serverList
        self.serverList = self.findChild(QtWidgets.QListWidget, 'listWidget')  #search for serverList widget
        self.serverList.clicked.connect(self.serverStatusCmd) #exec serverStatusCmd when serverList change selection
        
        #pingOutput
        self.pingOutput = self.findChild(QtWidgets.QTextBrowser, 'pingOutput') #search for pingOutput widget
        
        #playersOutput
        self.playersOutput = self.findChild(QtWidgets.QTextBrowser, 'playersOutput') #search for playersOutput widget
        
        #liveRadiobtn
        self.liveRadiobtn = self.findChild(QtWidgets.QRadioButton, 'liveRadiobtn') #search for liveRadiobtn widget
        self.liveRadiobtn.clicked.connect(self.livePing) #exec livePing when liveRadiobtn change status
        
        #livePing
        ''' inizialization axis values '''
        self.x = list(range(100))  # 100 time points
        self.y = [0] * 100  # 100 data points
        
        self.plotLayout = self.findChild(QtWidgets.QVBoxLayout, 'plotLayout')  #search for plotLayout widget
        self.graphWidget = pg.PlotWidget()  #define graph widget
        self.plotLayout.addWidget(self.graphWidget)  #add graph to plotLayout
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.graphWidget.setBackground('w')  #set background graph colour
        pen = pg.mkPen(color=(0, 0, 255))  #set graph line color
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)  # first plot
        
        self.timer = QtCore.QTimer() #set qt timer
        self.timer.setInterval(1000) #set interval of 1 sec
        self.timer.timeout.connect(self.update_plot_data) #call update_plot_data every sec
        
            
        #show UI
        self.show()
        
    
        
    def insertButtonCmd(self):
        flag = False
        
        with open("servers.dt", "r") as file: #open file
            servers = file.read().splitlines() #server ips reading
        
        for line in servers:
            if line == self.serverInput.text():
                flag = True
                break
        
        if flag == False:        
            file = open("servers.dt", "a")
            file.write(self.serverInput.text() + "\n")
            file.close()
            self.serverList.clear()
            Ui.loadList(self)
            
           
    def removeButtonCmd(self):
        self.pingOutput.clear()
        self.playersOutput.clear()
        
        selection = self.serverList.currentItem().text() #obtain text from selected object by serverList
        
        with open("servers.dt", "r") as file: #open file
            servers = file.read().splitlines() #server ips reading
        
        file = open("servers.dt", "w")   
        for line in servers:
            if line != selection:
                file.write(line + "\n")
        print(servers)
        file.close()
        self.serverList.clear()
        Ui.loadList(self)
        
        print(selection)
        
        
    def loadList(self):
        with open("servers.dt", "r") as file: #open file
            servers = file.read().splitlines() #server ips reading
        file.close()
        self.serverList.addItems(servers)  #adding server ips in serverList
        
        
    def serverStatusCmd(self):
        self.pingOutput.clear()
        self.playersOutput.clear()
        try:
            server = MinecraftServer.lookup(self.serverList.currentItem().text())
            status = server.status() 
            self.pingOutput.append("Latency: " + str(status.latency) + "\nPlayers: " + str(status.players.online))
            players = [ user['name'] for user in status.raw['players']['sample'] ]
            for name in players:
                self.playersOutput.append(name)
        except ConnectionRefusedError:
            self.pingOutput.append("Server unavailable.\nCheck server ip or your connection.")
        except Exception as exc:
            if str(exc) == 'timed out':
                self.pingOutput.append("Connection timed out. Cannot reach the server.")
            
            
    def livePing(self):
        if self.WINDOWSTATUS == 'FULL':
            self.WINDOWSTATUS = 'REDUCED'
            self.setFixedHeight(REDUCEDHEIGHT)
            self.timer.stop() #stop timer
            self.x = list(range(100))  # reset x
            self.y = [0] * 100  # reset y
        else:
            self.WINDOWSTATUS = 'FULL'
            self.setFixedHeight(HEIGHT)
            self.timer.start() #start timer
            

    def queryCmd(self):
        server = MinecraftServer.lookup(self.serverList.currentItem().text())
        query = server.query()
        players = query.players.names
        print(players)
        
        
    def update_plot_data(self):
        self.pingOutput.clear()
        self.playersOutput.clear()
        try:
            server = MinecraftServer.lookup(self.serverList.currentItem().text())
            status = server.status() 
            self.pingOutput.append("Latency: " + str(status.latency) + "\nPlayers: " + str(status.players.online))
            players = [ user['name'] for user in status.raw['players']['sample'] ]
            for name in players:
                self.playersOutput.append(name)
        except ConnectionRefusedError:
            self.pingOutput.append("Server unavailable.\nCheck server ip or your connection.")
        except Exception as exc:
            if str(exc) == 'timed out':
                self.pingOutput.append("Connection timed out. Cannot reach the server.")
        
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first 
        self.y.append(status.latency)  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.
        
                
class ErrorDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorDialog, self).__init__()
        uic.loadUi(ERRORDIALOGUI, self)
        
        #closeButton
        self.closeButton = self.findChild(QtWidgets.QPushButton, 'closeButton')  #search for closeButton widget
        self.closeButton.clicked.connect(self.closeButtonCmd)  #exec closeButtonCmd when closeButton clicked
        
        #errorLabel
        self.errorLabel = self.findChild(QtWidgets.QLabel, 'errorLabel') #search for errorLabel widget
        self.errorLabel.setText("Something went wrong")
        #label
        self.show()
        
    
    def closeButtonCmd(self):
        self.close()
    

app = QtWidgets.QApplication(sys.argv)

try:
    file = open("servers.dt","r")
    file.close()
except FileNotFoundError:
    file = open("servers.dt","w")
    file.write("")
    file.close()

win = Ui()
Ui.loadList(win)
app.exec_()
