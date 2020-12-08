#!/usr/bin/env python3

from PyQt5 import QtWidgets, uic
from mcstatus import MinecraftServer
import sys

XPOS = 200
YPOS = 200
WIDTH = 300
HEIGHT = 300

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('interface.ui', self)

        #insertButton
        self.insertButton = self.findChild(QtWidgets.QPushButton, 'insertButton')  #search for insertButton widget
        self.insertButton.clicked.connect(self.insertButtonCmd)  #exec insertButtonCmd when insertButton clicked

        #removeButton
        self.removeButton = self.findChild(QtWidgets.QPushButton, 'removeButton')  #search for removeButton widget
        self.removeButton.clicked.connect(self.removeButtonCmd)  #exec removeButtonCmd when removeButton clicked

        #serverInput
        self.serverInput = self.findChild(QtWidgets.QLineEdit, 'serverInput')  #search for serverInput widget

        #serverList
        self.serverList = self.findChild(QtWidgets.QListWidget, 'listWidget')  #search for serverList widget
        self.serverList.clicked.connect(self.serverStatusCmd) #exec serverStatusCmd when serverList change selection
        
        #pingOutput
        self.pingOutput = self.findChild(QtWidgets.QTextBrowser, 'pingOutput') #search for pingOutput widget
        
        #playersOutput
        self.playersOutput = self.findChild(QtWidgets.QTextBrowser, 'playersOutput') #search for playersOutput widget
        
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
        server = MinecraftServer.lookup(self.serverList.currentItem().text())
        status = server.status()
        query = server.query()
        players = query.players.names        
        
        self.pingOutput.clear()
        self.pingOutput.append("Latency: " + str(status.latency) + "\nPlayers: " + str(status.players.online))
        self.playersOutput.clear()
        for name in players:
            self.playersOutput.append(name + "\n")
        

app = QtWidgets.QApplication(sys.argv)
win = Ui()
Ui.loadList(win)
app.exec_()
