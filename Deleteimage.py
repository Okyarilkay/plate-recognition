
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import MainPage


baglanti = sqlite3.connect("araclistesi2.db")
cursor = baglanti.cursor()
plaka1 = ""
class deleteimage(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def baglanti_olustur(self):
        baglanti = sqlite3.connect("araclistesi2.db")
        baglanti.commit()
    def UI(self):

        self.setWindowTitle("Delete Menu")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(1000, 331, 500, 500)
        self.plakaLabel = QLabel("Plaka: ")

        self.plaka = QLineEdit()


        self.okbutton = QPushButton("Ok")
        self.checkOutLabel = QLabel("")
        self.checkInLabel = QLabel("")

        self.checkOutTime = QLabel("")

        self.checkInTime=QLabel("")
        self.priceLabel = QLabel("")
        self.price= QLabel("")
        self.bosluk=QLabel("")
        self.deleteButton=QPushButton("")
        self.deleteButton.hide()


        vbox=QVBoxLayout()
        vbox.addWidget(self.plakaLabel)
        vbox.addWidget(self.plaka)

        vbox.addWidget(self.okbutton)

        vbox.addWidget(self.bosluk)

        vbox.addWidget(self.checkInLabel)
        vbox.addWidget(self.checkInTime)

        vbox.addWidget(self.bosluk)

        vbox.addWidget(self.checkOutLabel)
        vbox.addWidget(self.checkOutTime)

        vbox.addWidget(self.bosluk)

        vbox.addWidget(self.priceLabel)
        vbox.addWidget(self.price)
        vbox.addWidget(self.bosluk)
        vbox.addWidget(self.deleteButton)


        vbox.addStretch()
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()
        self.setLayout(hbox)
        self.show()
        self.okbutton.clicked.connect(self.UI2)

    def refreshTable(self):
        MainPage.Ui_CarParkSystem.refresh()

    def UI2(self):
        global plaka1
        an = datetime.now()
        plaka1= self.plaka.text()


        try:
            query = "SELECT c FROM park where b=?"
            check_in = cursor.execute(query,(plaka1,)).fetchone()
            print(type(check_in[0]))
            prnew = (datetime.fromisoformat(check_in[0]))

            c = an - prnew
            # dönen saniyeyi dakikaya çevirme (dakika, saniye)
            dakika = divmod(c.total_seconds(), 60)
            print(dakika)
            result = (dakika[0] * 60 + dakika[1]) * 0.005
            print(result)

            self.checkInLabel.setText("Check-in Time: ")
            self.checkInTime.setText(check_in[0])
            self.checkOutLabel.setText("Check-out time: ")
            self.checkOutTime.setText(str(an))
            self.priceLabel.setText("Price: ")
            self.price.setText("$" + str(result))
            self.deleteButton.setText("Delete the record")
            self.deleteButton.show()
            # self.yazi2.setText("")
            self.deleteButton.clicked.connect(self.deleteRecord)
        except Exception as e:
            QMessageBox.information(self, "Info", "Please type valid plate number!")


    def deleteRecord(self):
        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this Record",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                query = "DELETE FROM park where b=?"
                cursor.execute(query, (plaka1,))
                baglanti.commit()
                QMessageBox.information(self, "Info", "Record has been deleted!")
                self.close()


            except:
                QMessageBox.information(self, "Info", "Record has not been deleted!")





