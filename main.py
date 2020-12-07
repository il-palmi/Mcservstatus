from PyQt5 import QtWidgets, uic
import sys

XPOS = 200
YPOS = 200
WIDTH = 300
HEIGHT = 300

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/untitled.ui', self)

        #addButton
        self.addButton = self.findChild(QtWidgets.QPushButton, 'addButton')  #cerca il pulsante
        self.addButton.clicked.connect(self.addButtonCmd)  #esegui comando quando pulsante premuto

        #cancButton
        self.cancButton = self.findChild(QtWidgets.QPushButton, 'cancButton')  #cerca il pulsante
        self.cancButton.clicked.connect(self.cancButtonCmd)  #esegui comando quando pulsante premuto

        #serverInput
        self.serverInput = self.findChild(QtWidgets.QLineEdit, 'serverInput')  #cerca campo di testo

        #serverList
        self.serverList = self.findChild(QtWidgets.QListWidget, 'serverList')  #cerca lista
        rfile = open("servers.dt", "r")  #apre file database
        servers = rfile.readlines()  #lettura servers
        for lines in servers:
            self.serverList.addItem(lines.strip('\n'))  #inserimento server in lista

        self.show()

    def addButtonCmd(self):
        file = open("servers.dt", "a")
        file.write(self.serverInput.text() + "\n")
        file.close()
        print("server aggiunto: " + self.serverInput.text())

    def cancButtonCmd(self):
        rfile = open('servers.dt','r')
        servers = rfile.readlines()
        rfile.close()
        file = open("servers.dt","w")
        for line in servers:
            if line.strip("\n") != self.serverList.selectedItems():
                file.write(line)
        print("server rimosso: "+ str(self.serverList.selectedItems()))



app = QtWidgets.QApplication(sys.argv)
win = Ui()
app.exec_()