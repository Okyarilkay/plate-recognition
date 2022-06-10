import datetime
import sys, os, shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import main
import sqlite3


import MainPage

path = ""
imagePath = "1.png"
newpath = ""
fileN = ""



baglanti = sqlite3.connect("araclistesi2.db")
cursor = baglanti.cursor()


class AddImage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vehicle Entry Menu")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 600, 750)
        #self.setFixedSize(self.size())

        self.UI()
        self.show()


    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.setGeometry(500, 331, 500, 500)
        self.add = QPushButton("Add")
        self.parknumberlabel=QLabel("Park number: ")
        self.parknumber=QComboBox()
        self.bosluk=QLabel("")
        test2 = self.comboValue()
        temp = list()
        for i in test2:
            temp.append(i[0])
        temp2 = list(range(1, 21))
        ye = set(temp2) - set(temp)
        for i in ye:
            self.parknumber.addItem(str(i))

        self.add.clicked.connect(self.addFunc)
        self.openPdf = QPushButton("Open Image")
        self.openPdf.clicked.connect(self.pushButtonhandler)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(("Park number: "),self.parknumber)
        self.bottomLayout.addRow(self.bosluk)
        self.bottomLayout.addRow(QLabel(""), self.openPdf)
        self.bottomLayout.addRow(self.bosluk)
        self.bottomLayout.addRow(QLabel(""),self.add)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLeftLayout.addWidget(self.topFrame)
        self.mainLeftLayout.addWidget(self.bottomFrame)
        self.mainLayout.addLayout(self.mainLeftLayout)
        self.setLayout(self.mainLayout)

    def pushButtonhandler(self):
        self.openDialogBox()

    def openDialogBox(self):
        global path, newpath, fileN,imagePath
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        test = path.split("/")
        imagePath = test[-1]

    def comboValue(self):

        query = "SELECT a FROM park"
        test = cursor.execute(query).fetchall()
        return test

    def refreshTable(self):
        MainPage.Ui_CarParkSystem.displayTable()

    def addFunc(self):
        main.main(imagePath)
        test2 = main.test(imagePath)
        an = datetime.datetime.now()
        parkNumber = int(self.parknumber.currentText())
        try:
            query = "INSERT INTO park (a,b,c) VALUES (?,?,?)"
            cursor.execute(query, (parkNumber,test2,str(an)))
            baglanti.commit()
            QMessageBox.information(self, "Info", "Record has been added!")
            self.close()

        except:
            QMessageBox.information(self, "Info", "Record has not been added!")

















