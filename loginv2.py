# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginfinal.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import AlmostFinalv5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSizeGrip
from datetime import datetime
from datetime import timedelta
import sqlite3
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QMessageBox


#key  = Fernet.generate_key()
key = b'TO_OA2q44NX84H6SUnuGHqWj-QA9C6tzMZzxmU7ZVRs='
cipher = Fernet(key)

expiry = datetime.date(datetime.today()) + timedelta(days=1)
encrypted = cipher.encrypt(str(expiry).encode())
#date = datetime.date(datetime.today())
print(expiry)
print(encrypted)

list_ = []
conn = sqlite3.connect('mta.db')
query = "SELECT * FROM Gibberish"
lis = conn.cursor().execute(query)
conn.commit()
m = str(list(lis.fetchall())[0][0]).encode()
print(type(m))
original = cipher.decrypt(m).decode()

print(original)
today = str(datetime.date(datetime.today()))

class Ui_MainWindow(object):

    def master_open(self):
                self.window = QtWidgets.QMainWindow()
                self.ui = AlmostFinalv5.Ui_MainWindow()
                self.ui.setupUi(self.window)
                self.window.show()


    def exit_(self):
        sys.exit(app.exec_())

    def open(self):
        #if datetime.strptime(original, "%Y-%m-%d") > datetime.strptime(today, "%Y-%m-%d"):
        try:
            if self.uname.text() == "KD" and self.password.text() == "123":
                self.window = QtWidgets.QMainWindow()
                self.ui = AlmostFinalv5.Ui_MainWindow()
                self.ui.setupUi(self.window)
                self.window.show()

            else:
                msg = QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
                msg.setWindowTitle("Error")
                msg.setText(
                    "You have entered either wrong username or wrong password")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Close)
                x = msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("The Licence Period is over. If you want to continue using the software call at +918131838939")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()



    def setupUi(self, MainWindow):



        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 779)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background:url(:/newPrefix/t2.jpg)")
        MainWindow.setDocumentMode(True)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks|QtWidgets.QMainWindow.ForceTabbedDocks|QtWidgets.QMainWindow.GroupedDragging|QtWidgets.QMainWindow.VerticalTabs)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.close = QtWidgets.QPushButton(self.centralwidget)
        self.close.setGeometry(QtCore.QRect(870, 10, 31, 23))
        self.close.clicked.connect(self.exit_)
        self.close.setStyleSheet("QPushButton{background:transparent}\n"
"QPushButton{border:none}")
        self.close.setText("")
        self.close.setObjectName("close")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(250, 450, 121, 41))
        self.login.setAutoDefault(True)
        self.login.clicked.connect(self.open)
        self.login.setAutoDefault(True)
        self.login.setStyleSheet("QPushButton{background:transparent}\n"
"QPushButton{border:none}")
        self.login.setText("")
        self.login.setObjectName("login")
        self.master = QtWidgets.QPushButton(self.centralwidget)
        self.master.clicked.connect(self.master_open)
        self.master.setGeometry(QtCore.QRect(530, 450, 121, 41))
        self.master.setStyleSheet("QPushButton{background:transparent}\n"
"QPushButton{border:none}")
        self.master.setText("")
        self.master.setObjectName("master")
        self.uname = QtWidgets.QLineEdit(self.centralwidget)
        self.uname.setGeometry(QtCore.QRect(330, 310, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.uname.setFont(font)
        self.uname.setStyleSheet("QLineEdit{background:transparent}\n"
"QLineEdit{border:none}")
        self.uname.setAlignment(QtCore.Qt.AlignCenter)
        self.uname.setObjectName("uname")
        self.uname.setFocus()
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(330, 370, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Charmonman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.password.setFont(font)
        self.password.setStyleSheet("QLineEdit{background:transparent}\n"
"QLineEdit{border:none}")
        self.password.setInputMask("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setAlignment(QtCore.Qt.AlignCenter)
        self.password.setObjectName("password")
        self.password.returnPressed.connect(self.open)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.uname.setTabOrder(self.uname, self.password)
        self.uname.setTabOrder(self.password, self.login)
        self.uname.setTabOrder(self.login, self.master)
        self.uname.setTabOrder(self.master, self.close)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
import abc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    MainWindow.show()
    sys.exit(app.exec_())
