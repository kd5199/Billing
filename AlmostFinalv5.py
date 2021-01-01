# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testy.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import sqlite3
import datetime
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.pagesizes import A5
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Table
from PyQt5.QtWidgets import QMessageBox
import PyPDF2
import webbrowser as wb
import os
import csv
import abc_rc
import sys
import pandas as pd
import requests

import xlsxwriter
""" datetime.date.today()
##print(month)
end_date = datetime.datetime.today()
start_date = datetime.datetime(2020, 8, 1)
num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
##print(num_months)"""

"""addeddates = []
for k in range(3):
    addeddates.append(str(datetime.datetime.today().month + k)+"/"+str(datetime.datetime.today().year))
self.query = "SELECT * FROM Stock WHERE Exp LIKE '{}','{}','{}'".format(str(self.addeddates[0]), str(self.addeddates[1]), str(self.addeddates[2]))


##print(query)"""
dummy1 = 0  # Add product
dummy2 = 0


# InvoiceID = str(datetime.date.today())+str(subscript) #Bill No

# ##print(datetime.datetime.date(datetime.datetime.today()))

class Ui_MainWindow(object):
    def txtgst(self):
        with open('GST_Report.txt', 'w') as yourFile:
            yourFile.write(str(self.total_2.toPlainText()))
            wb.open_new(r'{}/{}'.format(os.getcwd(), 'GST_Report.txt'))


    def send(self):
        try:
            url = "https://www.fast2sms.com/dev/bulk"

            querystring = {
                "authorization": "w7A5niGUF0ZNuMDO9rjbqmdvTaXL6Rek3xpf4zKtBC1YVSglWQ38ausw52FmEJxhUirTV7p4lIdozQDS",
                "sender_id": "FSTSMS",
                "message": "{}".format(self.textEdit.toPlainText()),
                "language": "english",
                "route": "p",
                "numbers": "{}".format(int(self.customertable.item(self.customertable.currentRow(), 1).text()))}

            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)

            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Information")
            msg.setText(response.text)
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        except:
            #print("{}".format(self.textEdit.toPlainText()))
            #print("{}".format(int(self.customertable.item(self.customertable.currentRow(), 1).text())))
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Couldn't send!!!"+"\n"+"Check if you have Internet Connection and the Contact is 10 digit No. or Please try after some time.")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()


    def save_print_modify_pur(self):

        try:

            self.pur_productlist = []
            self.pur_mrplist = []
            self.pur_ratelist = []
            self.pur_hsnlist = []
            self.pur_batchlist = []
            self.pur_quantitylist = []
            self.pur_freelist = []
            self.pur_explist = []
            self.pur_discountlist = []
            self.pur_gstlist = []
            self.pur_amountlist = []
            self.pur_pidlist = []

            for i in range(self.tableWidget_16.rowCount()):
                self.pur_productlist.append(self.tableWidget_16.item(i, 0).text())
                self.pur_hsnlist.append(self.tableWidget_16.item(i, 1).text())
                self.pur_batchlist.append(self.tableWidget_16.item(i, 2).text())
                self.pur_mrplist.append(self.tableWidget_16.item(i, 3).text())
                self.pur_ratelist.append(self.tableWidget_16.item(i, 4).text())
                self.pur_quantitylist.append(self.tableWidget_16.item(i, 5).text())
                self.pur_freelist.append(self.tableWidget_16.item(i, 6).text())
                self.pur_explist.append(self.tableWidget_16.item(i, 7).text())
                self.pur_discountlist.append(self.tableWidget_16.item(i, 8).text())
                self.pur_gstlist.append(self.tableWidget_16.item(i, 9).text())
                self.pur_amountlist.append(self.tableWidget_16.item(i, 10).text())
                self.pur_pidlist.append(self.tableWidget_16.item(i, 11).text())
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While creating list!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        try:
            self.query = "SELECT PID, Quantity, Free  FROM PurchaseData WHERE PurchaseID = {}".format(self.purchaseid_)
            ##print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.mode1 = self.lis.fetchall()
            self.mode1 = list(dict.fromkeys(self.mode1))
            ##print(len(self.mode1))
            for i in range(len(self.mode1)):
                self.query = "UPDATE Stock SET Quantity = Quantity-{}-{}  WHERE PID = {}".format(int(self.mode1[i][1]),int(self.mode1[i][2]),self.mode1[i][0])
                ##print(self.query)
                self.conn.cursor().execute(self.query)
                self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating quantity!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT Dealer, Address, Date FROM Purchase WHERE PurchaseID = {}".format(self.purchaseid_)
            ##print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.m = self.lis.fetchall()
            self.m = list(dict.fromkeys(self.m))
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While creating Doc list!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()


        try:

            self.query = "DELETE FROM PurchaseData WHERE PurchaseID = {} ".format(self.purchaseid_)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While  deleting!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:

            for i in range(len(self.pur_productlist)):
                self.query = "INSERT INTO PurchaseData VALUES('{}','{}',{},'{}','{}','{}','{}','{}',{},{},{},{},'{}',{},{},{},{})".format(
                    self.m[0][0],
                    self.m[0][1],
                    self.purchaseid_,
                    self.invoicedate_3,
                    self.m[0][2],
                    self.pur_productlist[i],
                    self.pur_hsnlist[i],
                    self.pur_batchlist[i],
                    self.pur_mrplist[i],
                    self.pur_ratelist[i],

                    self.pur_quantitylist[i],
                    self.pur_freelist[i],
                    self.pur_explist[i],
                    self.pur_discountlist[i],
                    self.pur_gstlist[i],
                    self.pur_amountlist[i], self.pur_pidlist[i])
                ##print(self.query)
                self.lis = self.conn.cursor().execute(self.query)
                self.conn.commit()

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating sales!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()



        try:
            self.query = "SELECT PID, Quantity, Free  FROM PurchaseData WHERE PurchaseID = {}".format(self.purchaseid_)
            ##print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.mode1 = self.lis.fetchall()
            self.mode1 = list(dict.fromkeys(self.mode1))
            ##print(len(self.mode1))
            for i in range(len(self.mode1)):
                self.query = "UPDATE Stock SET Quantity = Quantity+{}+{}  WHERE PID = {}".format(int(self.mode1[i][1]),int(self.mode1[i][2]),self.mode1[i][0])
                ##print(self.query)
                self.conn.cursor().execute(self.query)
                self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating quantity!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()




        try:
            self.textBrowser_6.clear()
            # ##print("Entered")
            self.total_taxable_purchase = 0.00
            self.total_payable_purchase = 0.00
            self.tax_purchase = 0.00
            self.discount_purchase = 0.00
            self.Wdiscount_purchase = 0.0

            for i in range(self.tableWidget_16.rowCount()):
                # ##print(int(self.tableWidget_2.item(i, 6).text()))
                # ##print('here')

                """self.total_taxable_purchase = float(self.tableWidget_3.item(i, 7).text()) / (
                            1 + (float(self.tableWidget_2.item(i, 6).text())) / 100) + self.total_taxable"""
                # ##print("Entered0")
                self.total_taxable_purchase = self.total_taxable_purchase + float(self.tableWidget_16.item(i, 10).text())
                self.tax_purchase = round(
                    float(self.tableWidget_16.item(i, 10).text()) * float(self.tableWidget_16.item(i, 9).text()) / 100,
                    2) + self.tax_purchase
                self.Wdiscount_purchase = self.Wdiscount_purchase + float(
                    float(self.tableWidget_16.item(i, 4).text()) * float(self.tableWidget_16.item(i, 5).text()))

            # ##print("Entered1")
            self.total_payable_purchase = self.total_taxable_purchase + self.tax_purchase
            self.discount_purchase = self.Wdiscount_purchase - self.total_taxable_purchase
            # ##print("Entered2")

            self.textBrowser_6.setText("Total Taxable Amount : {}".format(round(self.total_taxable_purchase)))
            self.textBrowser_6.append("Total SGST           : {}".format(round(self.tax_purchase / 2), 2))
            self.textBrowser_6.append("Total CGST           : {}".format(round(self.tax_purchase / 2), 2))
            self.textBrowser_6.append("Discount             : {}".format(round(self.discount_purchase, 2)))
            self.textBrowser_6.append("Amount To Pay        : {}".format(round(self.total_payable_purchase, 2)))
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While calculating!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.Localpurchase12 = 0.0
            self.Localpurchase18 = 0.0
            self.Localpurchase5 = 0.0

            for i in range(len(self.pur_productlist)):
                if int(self.pur_gstlist[i]) == 12:
                    self.Localpurchase12 = self.Localpurchase12 + float(self.pur_amountlist[i])
                elif int(self.pur_gstlist[i]) == 18:
                    self.Localpurchase18 = self.Localpurchase18 + float(self.pur_amountlist[i])
                elif int(self.pur_gstlist[i]) == 5:
                    self.Localpurchase5 = self.Localpurchase5 + float(self.pur_amountlist[i])




        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating sale1!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:



            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT Mode FROM Purchase WHERE PurchaseID = {}".format(self.purchaseid_)
            #print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.mode1 = self.lis.fetchall()
            self.mode1 = list(dict.fromkeys(self.mode1))
            #print(self.mode1)
            #print(self.mode1[0][0])

            """self.textBrowser_6.setText("Total Taxable Amount : {}".format(round(self.total_taxable_purchase)))
            self.textBrowser_6.append("Total SGST           : {}".format(round(self.tax_purchase / 2), 2))
            self.textBrowser_6.append("Total CGST           : {}".format(round(self.tax_purchase / 2), 2))
            self.textBrowser_6.append("Discount             : {}".format(round(self.discount_purchase, 2)))
            self.textBrowser_6.append("Amount To Pay        : {}".format(round(self.total_payable_purchase, 2)))  self.tax_purchase, self.total_payable_purchase,"""


            if self.mode1[0][0] == "Credit":

                self.query = "UPDATE Purchase SET Amount = {}, Tax = {}, Local12 = {}, Local18={}, Local5={},Credit = {}, Balance = {}  WHERE PurchaseID = {}".format(
                    self.total_payable_purchase,

                    self.tax_purchase,
                    round(self.Localpurchase12 * 0.12, 2),
                    round(self.Localpurchase18 * 0.18, 2),
                    round(self.Localpurchase5 * 0.05, 2),
                    self.total_payable_purchase,
                    self.total_payable_purchase,
                    self.purchaseid_)
                ##print(self.query)

            elif self.mode1[0][0] == "Cash":
                self.query = "UPDATE Purchase SET Amount = {}, Tax = {}, Local12 = {}, Local18={}, Local5={},Debit = {},Credit = 0, Balance = 0  WHERE PurchaseID = {}".format(
                    self.total_payable_purchase,

                    self.tax_purchase,
                    round(self.Localpurchase12 * 0.12, 2),
                    round(self.Localpurchase18 * 0.18, 2),
                    round(self.Localpurchase5 * 0.05, 2),
                    self.total_payable_purchase,
                    self.purchaseid_)
            #print(self.query)
            self.conn.cursor().execute(self.query)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating sale!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT InvoiceNo FROM Purchase WHERE PurchaseID  = {}".format(self.purchaseid_)
            ##print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.invID_ = self.lis.fetchall()
            self.invID_ = list(dict.fromkeys(self.invID_))[0][0]


            self.conn = sqlite3.connect("mta.db")
            self.query = "UPDATE DayBook SET Amount = {}, TaxAmount = {} WHERE InvoiceNo = {} AND Event = 'Purchase'".format(
                float(self.total_payable_purchase), round(float(self.tax_purchase), 2), self.invID_)
            ##print(self.query)
            self.conn.cursor().execute(self.query)
            self.conn.commit()

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While misc1!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.query = "UPDATE GST SET Localsale12 = {},Localsale18 ={},Localsale5 = {} WHERE InvoiceNo = {} ".format(
                self.Localpurchase12, self.Localpurchase18,
                self.Localpurchase5, self.invID_)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While misc2!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        self.show_stock()



    def add_to_modify_pur(self):
        dummy2 = self.tableWidget_16.rowCount()
        row = self.tableWidget_17.currentRow()

        self.PIDpur = self.tableWidget_17.item(row, 0).text()
        self.Productpur = self.tableWidget_17.item(row, 1).text()
        self.Batchpur = self.tableWidget_17.item(row, 2).text()
        self.MRPpur = self.tableWidget_17.item(row, 3).text()
        self.Ratepur = self.tableWidget_17.item(row, 4).text()
        self.Exppur = self.tableWidget_17.item(row, 5).text()
        self.HSNpur = self.tableWidget_17.item(row, 6).text()
        self.GSTpur = self.tableWidget_17.item(row, 7).text()
        self.Avlpur = self.tableWidget_17.item(row, 8).text()
        self.Rackpur = self.tableWidget_17.item(row, 9).text()
        self.Quanpur = self.tableWidget_17.item(row, 10).text()
        self.freepur = self.tableWidget_17.item(row, 11).text()
        self.Discountpur = self.tableWidget_17.item(row, 12).text()
        self.amount = str((float(self.Quanpur) * float(self.Ratepur)) - ((float(self.Quanpur) * float(self.Ratepur)) * (int(self.Discountpur) / 100)))

        self.tableWidget_16.insertRow(dummy2)
        self.tableWidget_16.setColumnCount(12)
        self.tableWidget_16.setHorizontalHeaderLabels(
            ["Product", "HSN Code", "Batch", "MRP", "Rate", "Quantity", "Free", "Expiry Date", "Discount", "GST",
             "Amount", "PID"])
        self.tableWidget_16.setItem(dummy2, 0, QtWidgets.QTableWidgetItem(str(self.Productpur)))
        self.tableWidget_16.setItem(dummy2, 1, QtWidgets.QTableWidgetItem(str(self.HSNpur)))
        self.tableWidget_16.setItem(dummy2, 2, QtWidgets.QTableWidgetItem(str(self.Batchpur)))
        self.tableWidget_16.setItem(dummy2, 3, QtWidgets.QTableWidgetItem(str(self.MRPpur)))
        self.tableWidget_16.setItem(dummy2, 4, QtWidgets.QTableWidgetItem(str(self.Ratepur)))
        self.tableWidget_16.setItem(dummy2, 5, QtWidgets.QTableWidgetItem(str(self.Quanpur)))
        self.tableWidget_16.setItem(dummy2, 6, QtWidgets.QTableWidgetItem(str(self.freepur)))
        self.tableWidget_16.setItem(dummy2, 7, QtWidgets.QTableWidgetItem(str(self.Exppur)))
        self.tableWidget_16.setItem(dummy2, 8, QtWidgets.QTableWidgetItem(str(self.Discountpur)))
        self.tableWidget_16.setItem(dummy2, 9, QtWidgets.QTableWidgetItem(str(self.GSTpur)))
        self.tableWidget_16.setItem(dummy2, 10, QtWidgets.QTableWidgetItem(self.amount))
        self.tableWidget_16.setItem(dummy2, 11, QtWidgets.QTableWidgetItem(str(self.PIDpur)))

        self.product_3.setFocus()






        # ##print("here2")
        #self.calculate_purchase()
        # ##print("here3")




    def delete_modify_pur(self):
        self.tableWidget_6.removeRow(self.tableWidget_16.currentRow())

    def show_to_modify_pur(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Purchase WHERE InvoiceNo = '{}' AND Date = '{}'".format(self.invoiceno_2.currentText(), self.invoicedate_3.text())

        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.mode1 = self.lis.fetchall()
        self.mode1 = list(dict.fromkeys(self.mode1))
        self.Party.setText(self.mode1[0][0])


        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT PurchaseID FROM Purchase WHERE InvoiceNo = '{}' AND Date = '{}'".format(
                self.invoiceno_2.currentText(), self.invoicedate_2.text())
            ##print(self.query)
            self.lis = self.conn.execute(self.query)
            self.purchaseid_ = self.lis.fetchall()
            self.purchaseid_ = list(dict.fromkeys(self.purchaseid_))[0][0]

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Enter Date!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT Product, HSN, Batch, MRP, Rate, Quantity,Free, Expiry,Discount, GST, Amount, PID FROM PurchaseData WHERE PurchaseID = {} ".format(
                self.purchaseid_)

            ##print(self.query)
            self.result = self.conn.execute(self.query)
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Enter Date1!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        self.tableWidget_16.setRowCount(0)
        self.tableWidget_16.setColumnCount(12)
        self.tableWidget_16.setHorizontalHeaderLabels(
            ["Product", "HSN Code", "Batch", "MRP","Rate", "Quantity","Free", "Expiry Date","Discount", "GST", "Amount","PID"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_16.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_16.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number!=5 or 6:
                    self.tableWidget_16.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.show_to_select_product_modify_pur()


    def show_to_select_product_modify_pur(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT PID, PName, Batch, MRP, Rate, Exp, HSN,GST, Quantity, RackNo FROM Stock WHERE PName = '{}'".format(
            self.product_3.currentText())
        self.result = self.conn.execute(self.query)
        self.tableWidget_17.setRowCount(0)
        self.tableWidget_17.setColumnCount(13)
        self.tableWidget_17.setHorizontalHeaderLabels(
            ["PID", "Product ", "Batch", "MRP", "Rate", "Expiry Date", "HSN", "GST", "Available", "Rack",
             "Quantity","Free","Discount"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_17.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_17.setItem(row_number, 10, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_17.setItem(row_number, 11, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_17.setItem(row_number, 12, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_17.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number!=10 or 11 or 12:
                    self.tableWidget_17.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.tableWidget_17.setColumnWidth(0, 50)
        self.tableWidget_17.setColumnWidth(1, 200)
        self.tableWidget_17.setColumnWidth(2, 100)
        self.tableWidget_17.setColumnWidth(3, 80)
        self.tableWidget_17.setColumnWidth(4, 80)
        self.tableWidget_17.setColumnWidth(5, 200)
        self.tableWidget_17.setColumnWidth(6, 100)
        self.tableWidget_17.setColumnWidth(7, 70)
        self.tableWidget_17.setColumnWidth(8, 90)
##########################################################################################
##########################################################################################
##########################################################################################
    def save_print_modify_sale(self):
        try:

            self.productlist = []
            self.hsnlist = []
            self.mrplist = []
            self.batchlist = []
            self.quantitylist = []
            self.explist = []
            self.gstlist = []
            self.amountlist = []
            self.pidlist = []
            for i in range(self.tableWidget_14.rowCount()):
                self.productlist.append(self.tableWidget_14.item(i, 0).text())
                self.hsnlist.append(self.tableWidget_14.item(i, 1).text())
                self.batchlist.append(self.tableWidget_14.item(i, 2).text())
                self.mrplist.append(self.tableWidget_14.item(i, 3).text())
                self.quantitylist.append(self.tableWidget_14.item(i, 4).text())
                self.explist.append(self.tableWidget_14.item(i, 5).text())
                self.gstlist.append(self.tableWidget_14.item(i, 6).text())
                self.amountlist.append(self.tableWidget_14.item(i, 7).text())
                self.pidlist.append(self.tableWidget_14.item(i, 8).text())
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While creating list!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()


        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT Doctor, Customer, CustomerContact, InvoiceDate FROM Sales WHERE InvoiceID = {}".format(self.Invoiceno.currentText())
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.m = self.lis.fetchall()
            self.m = list(dict.fromkeys(self.m))
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While creating Doc list!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.query = "SELECT PID, Quantity FROM Sales WHERE InvoiceID = {}".format(self.Invoiceno.currentText())
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.mode1 = self.lis.fetchall()
            self.mode1 = list(dict.fromkeys(self.mode1))
            for i in range(len(self.mode1)):

                self.query = "UPDATE Stock SET Quantity = Quantity + {} WHERE PID = {}".format(int(self.mode1[i][1]),self.mode1[i][0])
                self.lis = self.conn.cursor().execute(self.query)
                self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating quantity!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:

            self.query = "DELETE FROM Sales WHERE InvoiceID = {} ".format(self.Invoiceno.currentText())
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While  deleting!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:

            for i in range(len(self.productlist)):
                self.query = "INSERT INTO Sales VALUES({},'{}','{}',{},'{}',{},{},'{}',{},{},{},'{}','{}','{}',{})".format(
                    self.Invoiceno.currentText(),
                    self.invoicedate_2.text(),
                    self.productlist[i],
                    self.hsnlist[i],
                    self.batchlist[i],
                    self.mrplist[i],
                    self.quantitylist[i],
                    self.explist[i],
                    self.gstlist[i],
                    self.discount.value(),
                    self.amountlist[i],
                    self.m[0][0],
                    self.m[0][1],
                    self.m[0][2],
                    self.pidlist[i])
                self.lis = self.conn.cursor().execute(self.query)
                self.conn.commit()

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating sales!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.query = "SELECT PID, Quantity FROM Sales WHERE InvoiceID = {}".format(self.Invoiceno.currentText())
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.mode1 = self.lis.fetchall()
            self.mode1 = list(dict.fromkeys(self.mode1))
            for i in range(len(self.mode1)):
                self.query = "UPDATE Stock SET Quantity = Quantity - {} WHERE PID = {}".format(int(self.mode1[i][1]),
                                                                                               self.mode1[i][0])
                self.lis = self.conn.cursor().execute(self.query)
                self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating quantity!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()




        try:
            self.total_taxable = 0.00
            self.total_amount = 0.00
            self.total_amount_wod = 0.00
            self.tax = 0.0
            for i in range(self.tableWidget_14.rowCount()):
                # ##print(int(self.tableWidget_2.item(i, 6).text()))
                # ##print('here')

                self.total_taxable = float(self.tableWidget_14.item(i, 7).text()) / (
                        1 + (float(self.tableWidget_14.item(i, 6).text())) / 100) + self.total_taxable
                self.total_amount_wod = self.total_amount_wod + float(self.tableWidget_14.item(i, 7).text())

            self.total_amount = self.total_amount_wod - round((self.total_amount_wod * float(self.discount.value()) / 100),
                                                              2)
            self.tax = self.total_amount_wod - self.total_taxable

            self.textBrowser_5.append("Total Taxable Amount : {}".format(round(self.total_taxable, 2)))
            self.textBrowser_5.append("Total SGST           : {}".format(round(self.tax, 4) / 2))
            self.textBrowser_5.append("Total SGST           : {}".format(round(self.tax, 4) / 2))
            self.textBrowser_5.append("Discount             : {}".format(round((self.total_amount_wod * float(self.discount.value()) / 100)), 2))
            self.textBrowser_5.append("Total  Amount        : {}".format(round(self.total_amount_wod, 2)))
            self.textBrowser_5.append("Amount to pay        : {}".format(round(self.total_amount, 2)))
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While calculating!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:
            self.Localsale12 = 0.0
            self.Localsale18 = 0.0
            self.Localsale5 = 0.0

            for i in range(len(self.productlist)):
                if int(self.gstlist[i]) == 12:
                    self.Localsale12 = self.Localsale12 + float(self.amountlist[i])
                elif int(self.gstlist[i]) == 18:
                    self.Localsale18 = self.Localsale18 + float(self.amountlist[i])
                elif int(self.gstlist[i]) == 5:
                    self.Localsale5 = self.Localsale5 + float(self.amountlist[i])


        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating sale1!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT Mode FROM Sale WHERE InvoiceID = {}".format(self.Invoiceno.currentText())
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.mode1 = self.lis.fetchall()
            self.mode1 = list(dict.fromkeys(self.mode1))

            if self.mode1[0][0] == 'Credit':
                self.query = "UPDATE Sale SET Amount = {}, Discount = {}, Tax = {}, Local12 = {}, Local18={}, Local5={},Credit = {}, Balance = {}  WHERE InvoiceID = {}".format(
                    self.total_amount,
                    round((self.total_amount_wod * float(self.discount.value()) / 100), 2),
                    self.tax,
                    round(self.Localsale12 * 0.12, 2),
                    round(self.Localsale18 * 0.18, 2),
                    round(self.Localsale5 * 0.05, 2),
                    self.total_amount,
                    self.total_amount,
                    self.Invoiceno.currentText())

            elif self.mode1[0][0] == 'Cash':
                self.query = "UPDATE Sale SET Amount = {}, Discount = {}, Tax = {}, Local12 = {}, Local18={}, Local5={},Debit = {}  WHERE InvoiceID = {}".format(
                    self.total_amount,
                    round((self.total_amount_wod * float(self.discount.value()) / 100), 2),
                    self.tax,
                    round(self.Localsale12 * 0.12, 2),
                    round(self.Localsale18 * 0.18, 2),
                    round(self.Localsale5 * 0.05, 2),
                    self.total_amount,
                    self.Invoiceno.currentText())

            self.conn.cursor().execute(self.query)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While updating sale!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        try:
            ##print(float(self.total_amount))
            ##print(float(self.tax))
            ##print(float(int(self.Invoiceno.currentText())))
            self.conn = sqlite3.connect("mta.db")
            self.query = "UPDATE DayBook SET Amount = {}, TaxAmount = {} WHERE InvoiceNo = {}".format(
                float(self.total_amount), round(float(self.tax),2), int(self.Invoiceno.currentText()))
            ##print(self.query)
            self.conn.cursor().execute(self.query)
            self.conn.commit()

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While misc1!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()


        try:
            self.query = "UPDATE GST SET Localsale12 = {},Localsale18 ={},Localsale5 = {} WHERE InvoiceNo = {} ".format(
             self.Localsale12, self.Localsale18,
                self.Localsale5, self.Invoiceno.currentText())
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()

            self.Localsale12 = 0
            self.Localsale18 = 0
            self.Localsale5 = 0
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While misc2!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        # ##print(self.InvoiceID)
        try:
            self.list = []
            self.list_of_list_ = []
            for i in range(self.tableWidget_14.rowCount()):
                self.list.append(i)
                for j in range(self.tableWidget_14.columnCount()-1):

                    self.list.append(self.tableWidget_14.item(i, j).text())
                self.list_of_list_.append(self.list)
                self.list = []
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While misc!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        # ##print(self.InvoiceID)
        try:

            self.info = [
                ['Invoice No : {}'.format(self.Invoiceno.currentText()), 'Patient name : {}'.format(self.m[0][1])],
                ['Date : {}'.format(self.m[0][3]),
                 'Patient Contact : {}'.format(self.m[0][2])],
                ['', 'Prescribed By : {}'.format(self.m[0][0])]
            ]

            self.amount_info = [
                ['Taxable Amount :' + str(round(self.total_taxable, 2)), 'SGST :' + str(round(self.tax, 2) / 2),
                 'CGST :' + str(round(self.tax / 2, 2)),
                 'Discount :' + str(
                     round((self.total_amount_wod * float(self.discount.value()) / 100), 2)),
                 'Amount To Pay :' + str(round(self.total_amount))]]

            self.header = [["Sl", "Product", "HSN Code", "Batch", "MRP", "Quantity", "Expiry Date", "GST",
                            "Amount"]]  # .append(self.list_of_list)

            for i in range(len(self.list_of_list_)):
                self.header.append(self.list_of_list_[i])

            # self.list_of_list = [self.header,self.list_of_list[0],self.list_of_list[1],self.list_of_list[2],self.list_of_list[3],self.list_of_list[4],self.list_of_list[5],self.list_of_list[6],self.list_of_list[7],self.list_of_list[8]]
            # self.header.append(self.list_of_list)
            # self.header.append(self.amount_info)

            self.buffer = 'buffer.pdf'
            self.fileName = '{}.pdf'.format("mta" + str(self.Invoiceno.currentText()))
            self.pdf = SimpleDocTemplate(self.buffer, pagesize=landscape(A5), leftMargin=0, rightMargin=0,
                                         topMargin=80, bottomMargin=20)

            self.info_table = Table(self.info, hAlign="CENTER")
            self.product_table = Table(self.header, hAlign="CENTER")
            self.amount_table = Table(self.amount_info, hAlign="CENTER")

            # add style
            self.info_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), -5),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 5)

            ])

            self.product_style1 = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ])

            # 3) Add borders('GRID', (0, 0), (-1, -1), 1, colors.purple),
            self.product_style2 = TableStyle([
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            self.info_table.setStyle(self.info_style)
            self.product_table.setStyle(self.product_style2)
            self.amount_table.setStyle(self.product_style1)

            # ##print("Style created")

            self.elems = []

            self.elems.append(self.info_table)
            self.elems.append(self.product_table)
            self.elems.append(self.amount_table)

            # ##print("Appended")

            self.pdf.build(self.elems)
            # wb.open_new(r'{}/{}'.format(os.getcwd(), self.buffer))

            pdf_file = "Watermark.pdf"
            watermark = self.buffer
            merged_file = self.fileName
            input_file = open(pdf_file, 'rb')
            input_pdf = PyPDF2.PdfFileReader(pdf_file)
            watermark_file = open(watermark, 'rb')
            watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
            pdf_page = input_pdf.getPage(0)
            watermark_page = watermark_pdf.getPage(0)
            pdf_page.mergePage(watermark_page)
            output = PyPDF2.PdfFileWriter()
            output.addPage(pdf_page)
            merged_file = open(self.fileName, 'wb')
            output.write(merged_file)
            merged_file.close()
            watermark_file.close()
            input_file.close()

            wb.open_new(r'{}/{}'.format(os.getcwd(), self.fileName))

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("While making pdf!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        """self.textBrowser.clear()
        self.tableWidget_2.clear()
        self.tableWidget_11.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_11.setColumnCount(0)
        self.patientname.clear()
        self.lineEdit_11.clear()
        self.discount.clear()"""


        self.show_stock()


    def add_to_modify_sale(self):
        dummy3 = self.tableWidget_14.rowCount()
        row = self.tableWidget_15.currentRow()

        self.PIDsale = self.tableWidget_15.item(row, 0).text()
        self.Productsale = self.tableWidget_15.item(row, 1).text()
        self.Batchsale = self.tableWidget_15.item(row, 2).text()
        self.MRPsale = self.tableWidget_15.item(row, 3).text()
        self.Ratesale = self.tableWidget_15.item(row, 4).text()
        self.Expsale = self.tableWidget_15.item(row, 5).text()
        self.HSNsale = self.tableWidget_15.item(row, 6).text()
        self.GSTsale = self.tableWidget_15.item(row, 7).text()
        self.Avlsale = self.tableWidget_15.item(row, 8).text()
        self.Racksale = self.tableWidget_15.item(row, 9).text()
        self.Quansale = self.tableWidget_15.item(row, 10).text()
        ##print(self.Quansale)
        self.amount = float(self.MRPsale) * float(self.Quansale)
        ##print(self.amount)

        self.tableWidget_14.insertRow(dummy3)
        self.tableWidget_14.setColumnCount(9)
        self.tableWidget_14.setHorizontalHeaderLabels(
            ["Product", "HSN Code", "Batch", "MRP", "Quantity", "Expiry Date", "GST", "Amount", "PID"])

        self.tableWidget_14.setItem(dummy3, 0, QtWidgets.QTableWidgetItem(str(self.Productsale)))
        self.tableWidget_14.setItem(dummy3, 1, QtWidgets.QTableWidgetItem(str(self.HSNsale)))
        self.tableWidget_14.setItem(dummy3, 2, QtWidgets.QTableWidgetItem(str(self.Batchsale)))
        self.tableWidget_14.setItem(dummy3, 3, QtWidgets.QTableWidgetItem(str(self.MRPsale)))
        self.tableWidget_14.setItem(dummy3, 4, QtWidgets.QTableWidgetItem(str(self.Quansale)))
        self.tableWidget_14.setItem(dummy3, 5, QtWidgets.QTableWidgetItem(str(self.Expsale)))
        self.tableWidget_14.setItem(dummy3, 6, QtWidgets.QTableWidgetItem(str(self.GSTsale)))
        self.tableWidget_14.setItem(dummy3, 7, QtWidgets.QTableWidgetItem(str(self.amount)))
        self.tableWidget_14.setItem(dummy3, 8, QtWidgets.QTableWidgetItem(str(self.PIDsale)))

        self.product_2.setFocus()





    def delete_modify_sale(self):
        self.tableWidget_14.removeRow(self.tableWidget_14.currentRow())

    def show_to_modify_sale(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Customer FROM Sale WHERE InvoiceID = {}".format(self.Invoiceno.currentText())
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.mode1 = self.lis.fetchall()
        self.mode1 = list(dict.fromkeys(self.mode1))

        self.party_2.setText(self.mode1[0][0])
        self.conn = sqlite3.connect("mta.db")
        self.query= "SELECT Product, HSNCode, Batch, MRP, Quantity, Expiry, GST, Amount, PID FROM Sales WHERE InvoiceID = {} ".format(self.Invoiceno.currentText())
        try:
            self.result = self.conn.execute(self.query)
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Enter Date!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        self.tableWidget_14.setRowCount(0)
        self.tableWidget_14.setColumnCount(9)
        self.tableWidget_14.setHorizontalHeaderLabels(
            ["Product", "HSN Code", "Batch", "MRP", "Quantity", "Expiry Date", "GST", "Amount","PID"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_14.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_14.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number!=4:
                    self.tableWidget_14.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.show_to_select_product_modify_sale()


    def show_to_select_product_modify_sale(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT PID, PName, Batch, MRP, Rate, Exp, HSN,GST, Quantity, RackNo FROM Stock WHERE PName = '{}'".format(
            self.product_2.currentText())
        self.result = self.conn.execute(self.query)
        self.tableWidget_15.setRowCount(0)
        self.tableWidget_15.setColumnCount(11)
        self.tableWidget_15.setHorizontalHeaderLabels(
            ["PID", "Product ", "Batch", "MRP", "Rate", "Expiry Date", "HSN", "GST", "Available", "Rack",
             "Quantity"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_15.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_15.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget_15.setItem(row_number, 10, QtWidgets.QTableWidgetItem(str("0")))
                if column_number!=10:
                    self.tableWidget_15.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.tableWidget_15.setColumnWidth(0, 50)
        self.tableWidget_15.setColumnWidth(1, 200)
        self.tableWidget_15.setColumnWidth(2, 100)
        self.tableWidget_15.setColumnWidth(3, 80)
        self.tableWidget_15.setColumnWidth(4, 80)
        self.tableWidget_15.setColumnWidth(5, 200)
        self.tableWidget_15.setColumnWidth(6, 100)
        self.tableWidget_15.setColumnWidth(7, 70)
        self.tableWidget_15.setColumnWidth(8, 90)

    def stock_xlsx(self):
        ##print("Enter")

        self.list = []
        self.stock_lol = []
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.list.append(self.tableWidget.item(i, j).text())
            self.stock_lol.append(self.list)
            self.list = []

        self.filename = "MTA_Stock_Table.xlsx"
        ##print("Enter")

        df = pd.DataFrame(self.stock_lol,
                          columns=["PID","Product ", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date", "HSN Code","Rack"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:L', 30)
        writer.save()
        self.stock_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    def search_bill(self):
        self.filename = self.comboBox_3.currentText()
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    def duplicate(self):

        self.Pname_ = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
        self.batch_ = self.tableWidget.item(self.tableWidget.currentRow(), 2).text()
        self.mrp_ = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
        self.rate_ = self.tableWidget.item(self.tableWidget.currentRow(), 4).text()
        self.dealer_ = self.tableWidget.item(self.tableWidget.currentRow(), 5).text()
        self.company_ = self.tableWidget.item(self.tableWidget.currentRow(), 6).text()
        self.gst_ = self.tableWidget.item(self.tableWidget.currentRow(), 7).text()
        self.quantity_ = 0
        self.exp_ = self.tableWidget.item(self.tableWidget.currentRow(), 9).text()
        self.hsn_ = self.tableWidget.item(self.tableWidget.currentRow(), 10).text()
        self.rack_ = self.tableWidget.item(self.tableWidget.currentRow(), 11).text()

        self.conn = sqlite3.connect("mta.db")
        self.query = "INSERT INTO Stock(PName, Batch, MRP, Rate, DEALER, Company, GST, Quantity, Exp, HSN,RackNo) VALUES ('{}','{}',{},{},'{}','{}',{},{},'{}','{}','{}')".format(
            self.Pname_, self.batch.text(), self.mrp_, self.rate_, self.dealer_,
            self.company_, self.gst_, self.quantity_, str(self.exp_), self.hsn_,
            self.rack_)
        self.conn.execute(self.query)
        self.conn.commit()

        self.show_stock()
        self.show_summery()
        self.show_to_search()

    def update_purchase_ledger(self):
        ##print("Here")
        self.debit = int(self.tableWidget_8.item(self.tableWidget_8.currentRow(), 6).text())
        ##print(self.debit)
        self.credit = float(self.tableWidget_8.item(self.tableWidget_8.currentRow(), 5).text())
        ##print(self.credit)
        self.date_ = self.tableWidget_8.item(self.tableWidget_8.currentRow(), 0).text()
        ##print(self.date_)
        if self.tableWidget_8.item(self.tableWidget_8.currentRow(), 1).text()!=None:
            self.invoiceno_ = self.tableWidget_8.item(self.tableWidget_8.currentRow(), 1).text()
            ##print(self.invoiceno_)
        self.party_ = self.tableWidget_8.item(self.tableWidget_8.currentRow(), 2).text()
        ##print(self.party_)
        self.amount_ = float(self.tableWidget_8.item(self.tableWidget_8.currentRow(), 3).text())
        ##print(self.amount_)
        self.mode_ = self.tableWidget_8.item(self.tableWidget_8.currentRow(), 4).text()
        ##print("Here")
        if self.credit > self.debit:
            self.balance = self.credit - self.debit
        else:
            self.balance = 0

        self.query = "UPDATE Purchase SET Balance = {} WHERE  Date = '{}' AND InvoiceNo = '{}' AND Dealer = '{}'AND Amount = {} AND Mode = '{}'".format(

            self.balance, self.date_, self.invoiceno_, self.party_, self.amount_, self.mode_
        )
        self.conn.execute(self.query)
        self.query = "UPDATE Purchase SET Debit = {} WHERE  Date = '{}' AND InvoiceNo = '{}' AND Dealer = '{}'AND Amount = {} AND Mode = '{}'".format(

            self.credit-self.balance, self.date_, self.invoiceno_, self.party_, self.amount_, self.mode_
        )
        self.conn.execute(self.query)
        ##print("Here")
        self.conn.commit()
        self.show_purchase_ledger()

    def update_sale_ledger(self):
        self.debit =  int(self.tableWidget_10.item(self.tableWidget_10.currentRow(), 6).text())
        self.credit =  int(self.tableWidget_10.item(self.tableWidget_10.currentRow(), 5).text())
        self.date_ = self.tableWidget_10.item(self.tableWidget_10.currentRow(), 0).text()
        self.invoiceno_ = int(self.tableWidget_10.item(self.tableWidget_10.currentRow(), 1).text())
        self.party_ = self.tableWidget_10.item(self.tableWidget_10.currentRow(), 2).text()
        self.amount_ = float(self.tableWidget_10.item(self.tableWidget_10.currentRow(), 3).text())
        self.mode_ = self.tableWidget_10.item(self.tableWidget_10.currentRow(), 4).text()
        if self.credit > self.debit:
            self.balance = self.credit-self.debit
        else:
            self.balance = 0

        self.query = "UPDATE Sale SET Balance = {} WHERE  Date = '{}' AND InvoiceID = {} AND Customer = '{}'AND Amount = {} AND Mode = '{}'".format(

            self.balance,self.date_, self.invoiceno_, self.party_, self.amount_, self.mode_
        )
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_all_sale_ledger()


    def sale_ledger_xlsx(self):
        ##print("Enter")

        self.list = []
        self.sale_ledger_lol = []
        for i in range(self.tableWidget_10.rowCount()):
            for j in range(self.tableWidget_10.columnCount()):
                self.list.append(self.tableWidget_10.item(i, j).text())
            self.sale_ledger_lol.append(self.list)
            self.list = []

        self.filename = "MTA_Sale_ledger.xlsx"
        ##print("Enter")

        df = pd.DataFrame(self.sale_ledger_lol, columns=["Date", "Invoice No", "Party","Amount", "Mode", "Credit", "Debit", "Balane"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:H', 30)
        writer.save()
        self.sale_ledger_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    def purchase_ledger_xlsx(self):

        self.list = []
        self.purchase_ledger_lol = []
        for i in range(self.tableWidget_8.rowCount()):
            for j in range(self.tableWidget_8.columnCount()):
                self.list.append(self.tableWidget_8.item(i, j).text())
            self.purchase_ledger_lol.append(self.list)
            self.list = []
        self.filename = "MTA_Purchase_ledger.xlsx"

        df = pd.DataFrame(self.purchase_ledger_lol, columns=["Date", "Invoice No", "Dealer", "Amount", "Mode", "Credit", "Debit", "Balane"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:H', 30)
        writer.save()
        self.purchase_ledger_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    def show_sale_ledger(self):

        self.textBrowser_4.clear()

        if self.today_6.isChecked():
            self.query = "SELECT Date, InvoiceID, Customer,Amount, Mode, Credit,Debit, Balance FROM Sale WHERE Customer = '{}' AND Date = DATE('now')".format(self.party.currentText())
        elif self.previous_6.isChecked():
            self.query = "SELECT Date, InvoiceID, Customer, Amount, Mode, Credit,Debit, Balance FROM Sale WHERE Customer = '{}' AND Date BETWEEN DATE('{}') AND DATE('{}')".format(self.party.currentText(),self.from_6.text(),
                                                                                                     self.to_6.text())
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.setColumnCount(8)
        self.tableWidget_10.setHorizontalHeaderLabels(["Date", "Invoice No", "Party","Amount", "Mode", "Credit", "Debit", "Balance"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_10.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_10.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number !=6:
                    self.tableWidget_10.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        """for i in range(self.tableWidget_10.rowCount()):
            if self.tableWidget_10.item(i,4).text() == "Cash":
                self.tableWidget_10.setItem(i, 5, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_10.setItem(i, 6, QtWidgets.QTableWidgetItem(str(self.tableWidget_10.item(i,3).text())))
            elif self.tableWidget_10.item(i,4).text() == "Credit":
                self.tableWidget_10.setItem(i, 6, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_10.setItem(i, 5, QtWidgets.QTableWidgetItem(str(self.tableWidget_10.item(i,3).text())))

        for i in range(self.tableWidget_10.rowCount()):
            if int(self.tableWidget_10.item(i,5).text())>int(self.tableWidget_10.item(i,6).text()):
                balance = int(self.tableWidget_10.item(i,5).text()) - int(self.tableWidget_10.item(i,6).text())
            else:
                balance = 0
            self.tableWidget_10.setItem(i, 7, QtWidgets.QTableWidgetItem(str(balance)))
"""

        self.tableWidget_10.setColumnWidth(2, 300)
        self.tableWidget_10.setColumnWidth(1, 150)
        self.tableWidget_10.setColumnWidth(0, 150)
        self.tableWidget_10.setColumnWidth(3, 150)
        self.tableWidget_10.setColumnWidth(4, 150)
        self.tableWidget_10.setColumnWidth(5, 150)
        self.tableWidget_10.setColumnWidth(6, 150)
        self.tableWidget_10.setColumnWidth(7, 150)

        total_balance = 0

        for i in range(self.tableWidget_10.rowCount()):
            if self.tableWidget_10.item(i, 7).text() != None:
                total_balance = float(self.tableWidget_10.item(i, 7).text()) + total_balance

        self.row = int(self.tableWidget_10.rowCount())
        self.tableWidget_10.insertRow(self.row)


        self.tableWidget_10.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str('Total')))
        self.tableWidget_10.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(' ')))
        self.tableWidget_10.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 7, QtWidgets.QTableWidgetItem(str(total_balance)))


        self.textBrowser_4.append("TOTAL BALANCE")
        self.textBrowser_4.append(str(total_balance))


    def show_purchase_ledger(self):
        self.textBrowser_3.clear()

        if self.today_5.isChecked():
            self.query = "SELECT Date, InvoiceNo, Dealer,Amount, Mode, Credit,Debit, Balance FROM Purchase WHERE Dealer = '{}' AND Date = DATE('now')".format(self.deaer.currentText())
        elif self.previous_5.isChecked():
            self.query = "SELECT Date, InvoiceNo, Deaer, Amount, Mode, Credit,Debit, Balance FROM Purchase WHERE Dealer = '{}' ANDDate BETWEEN DATE('{}') AND DATE('{}')".format(
                self.deaer.currentText(),
                self.from_5.text(),
                self.to_5.text())
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget_8.setRowCount(0)
        self.tableWidget_8.setColumnCount(8)
        self.tableWidget_8.setHorizontalHeaderLabels(
            ["Date", "Invoice No", "Dealer", "Amount", "Mode", "Credit", "Debit", "Balance"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_8.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_8.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number !=6:
                    self.tableWidget_8.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        """for i in range(self.tableWidget_8.rowCount()):
            if self.tableWidget_8.item(i, 4).text() == "Cash":
                self.tableWidget_8.setItem(i, 5, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_8.setItem(i, 6,
                                            QtWidgets.QTableWidgetItem(str(self.tableWidget_8.item(i, 3).text())))
            elif self.tableWidget_8.item(i, 4).text() == "Credit":
                self.tableWidget_8.setItem(i, 6, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_8.setItem(i, 5,
                                            QtWidgets.QTableWidgetItem(str(self.tableWidget_8.item(i, 3).text())))

        for i in range(self.tableWidget_8.rowCount()):
            if int(self.tableWidget_8.item(i, 5).text()) > int(self.tableWidget_8.item(i, 6).text()):
                balance = int(self.tableWidget_8.item(i, 5).text()) - int(self.tableWidget_8.item(i, 6).text())
            else:
                balance = 0
            self.tableWidget_8.setItem(i, 7, QtWidgets.QTableWidgetItem(str(balance)))
"""
        self.tableWidget_8.setColumnWidth(2, 300)
        self.tableWidget_8.setColumnWidth(1, 150)
        self.tableWidget_8.setColumnWidth(0, 150)
        self.tableWidget_8.setColumnWidth(3, 150)
        self.tableWidget_8.setColumnWidth(4, 150)
        self.tableWidget_8.setColumnWidth(5, 150)
        self.tableWidget_8.setColumnWidth(6, 150)
        self.tableWidget_8.setColumnWidth(7, 150)

        total_balance = 0

        for i in range(self.tableWidget_8.rowCount()):
            if self.tableWidget_8.item(i, 7).text() != None:
                total_balance = float(self.tableWidget_8.item(i, 7).text()) + total_balance

        self.row = int(self.tableWidget_8.rowCount())
        self.tableWidget_8.insertRow(self.row)


        self.tableWidget_8.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str('Total')))
        self.tableWidget_8.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(' ')))
        self.tableWidget_8.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 7, QtWidgets.QTableWidgetItem(str(total_balance)))

        self.textBrowser_3.append("TOTAL BALANCE")
        self.textBrowser_3.append(str(total_balance))

    def show_all_purchase_ledger(self):

        self.textBrowser_3.clear()

        if self.today_5.isChecked():
            self.query = "SELECT Date, InvoiceNo, Dealer,Amount, Mode, Credit,Debit, Balance FROM Purchase WHERE Date = DATE('now')"
        elif self.previous_5.isChecked():
            self.query = "SELECT Date, InvoiceNo, Dealer, Amount, Mode, Credit,Debit, Balance FROM Purchase WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(
                self.from_5.text(),
                self.to_5.text())

        self.conn = sqlite3.connect("mta.db")

        self.result = self.conn.execute(self.query)

        self.tableWidget_8.setRowCount(0)
        self.tableWidget_8.setColumnCount(8)
        self.tableWidget_8.setHorizontalHeaderLabels(
            ["Date", "Invoice No", "Dealer", "Amount", "Mode", "Credit", "Debit", "Balance"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_8.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_8.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number!= 6:
                    self.tableWidget_8.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        """for i in range(self.tableWidget_8.rowCount()):
            if self.tableWidget_8.item(i, 4).text() == "Cash":
                self.tableWidget_8.setItem(i, 5, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_8.setItem(i, 6,
                                            QtWidgets.QTableWidgetItem(str(self.tableWidget_8.item(i, 3).text())))
            elif self.tableWidget_8.item(i, 4).text() == "Credit":
                self.tableWidget_8.setItem(i, 6, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_8.setItem(i, 5,
                                            QtWidgets.QTableWidgetItem(str(self.tableWidget_8.item(i, 3).text())))

        for i in range(self.tableWidget_8.rowCount()):
            if int(self.tableWidget_8.item(i, 5).text()) > int(self.tableWidget_8.item(i, 6).text()):
                balance = int(self.tableWidget_8.item(i, 5).text()) - int(self.tableWidget_8.item(i, 6).text())
            else:
                balance = 0
            self.tableWidget_8.setItem(i, 7, QtWidgets.QTableWidgetItem(str(balance)))
"""
        self.tableWidget_8.setColumnWidth(2, 300)
        self.tableWidget_8.setColumnWidth(1, 150)
        self.tableWidget_8.setColumnWidth(0, 150)
        self.tableWidget_8.setColumnWidth(3, 150)
        self.tableWidget_8.setColumnWidth(4, 150)
        self.tableWidget_8.setColumnWidth(5, 150)
        self.tableWidget_8.setColumnWidth(6, 150)
        self.tableWidget_8.setColumnWidth(7, 150)

        total_balance = 0
        for i in range(self.tableWidget_8.rowCount()):
            if self.tableWidget_8.item(i, 7).text() != None:
                total_balance =  float(self.tableWidget_8.item(i, 7).text()) + total_balance

        self.row = int(self.tableWidget_8.rowCount())
        self.tableWidget_8.insertRow(self.row)

        self.tableWidget_8.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str('Total')))
        self.tableWidget_8.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(' ')))
        self.tableWidget_8.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_8.setItem(self.row, 7, QtWidgets.QTableWidgetItem(str(total_balance)))

        self.textBrowser_3.setText("TOTAL BALANCE")
        self.textBrowser_3.append(str(total_balance))


    def show_all_sale_ledger(self):

        self.textBrowser_4.clear()

        if self.today_6.isChecked():
            self.query = "SELECT Date, InvoiceID, Customer,Amount, Mode, Credit,Debit, Balance FROM Sale WHERE Date = DATE('now')"
        elif self.previous_6.isChecked():
            self.query = "SELECT Date, InvoiceID, Customer,Amount, Mode, Credit,Debit, Balance FROM Sale WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(self.from_6.text(),
                                                                                                     self.to_6.text())
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.setColumnCount(8)
        self.tableWidget_10.setHorizontalHeaderLabels(["Date", "Invoice No", "Party","Amount", "Mode", "Credit", "Debit", "Balance"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_10.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_10.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number != 6:
                    self.tableWidget_10.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        """for i in range(self.tableWidget_10.rowCount()):
            if self.tableWidget_10.item(i,4).text() == "Cash":
                self.tableWidget_10.setItem(i, 5, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_10.setItem(i, 6, QtWidgets.QTableWidgetItem(str(self.tableWidget_10.item(i,3).text())))
            elif self.tableWidget_10.item(i,4).text() == "Credit":
                self.tableWidget_10.setItem(i, 6, QtWidgets.QTableWidgetItem(str("0")))
                self.tableWidget_10.setItem(i, 5, QtWidgets.QTableWidgetItem(str(self.tableWidget_10.item(i,3).text())))

        for i in range(self.tableWidget_10.rowCount()):
            if int(self.tableWidget_10.item(i,5).text())>int(self.tableWidget_10.item(i,6).text()):
                balance = int(self.tableWidget_10.item(i,5).text()) - int(self.tableWidget_10.item(i,6).text())
            else:
                balance = 0
            self.tableWidget_10.setItem(i, 7, QtWidgets.QTableWidgetItem(str(balance)))
"""

        self.tableWidget_10.setColumnWidth(2, 300)
        self.tableWidget_10.setColumnWidth(1, 150)
        self.tableWidget_10.setColumnWidth(0, 150)
        self.tableWidget_10.setColumnWidth(3, 150)
        self.tableWidget_10.setColumnWidth(4, 150)
        self.tableWidget_10.setColumnWidth(5, 150)
        self.tableWidget_10.setColumnWidth(6, 150)
        self.tableWidget_10.setColumnWidth(7, 150)

        total_balance = 0
        for i in range(self.tableWidget_10.rowCount()):
            if self.tableWidget_10.item(i, 7).text() != None:
                total_balance =  float(self.tableWidget_10.item(i, 7).text()) + total_balance

        self.row = int(self.tableWidget_10.rowCount())
        self.tableWidget_10.insertRow(self.row)



        self.tableWidget_10.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str('Total')))
        self.tableWidget_10.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(' ')))
        self.tableWidget_10.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str('')))
        self.tableWidget_10.setItem(self.row, 7, QtWidgets.QTableWidgetItem(str(total_balance)))


        self.textBrowser_4.append("TOTAL BALANCE")
        self.textBrowser_4.append(str(total_balance))

    def open_pdf(self):

        self.fileName = self.comboBox_3.currentText()
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.fileName))

    def day_book_xlsx(self):

        self.list = []
        self.day_book_lol = []
        for i in range(self.tableWidget_4.rowCount()):
            for j in range(self.tableWidget_4.columnCount()):
                self.list.append(self.tableWidget_4.item(i, j).text())
            self.day_book_lol.append(self.list)
            self.list = []

        self.filename = "MTA_Day_Book.xlsx"

        df = pd.DataFrame(self.day_book_lol, columns=["Date", "Invoice No", "Party", "Event", "Amount", "GST"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:F', 30)
        writer.save()
        self.day_book_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))
    def sale_book_xlsx(self):

        self.list = []
        self.sale_book_lol = []
        for i in range(self.tableWidget_7.rowCount()):
            for j in range(self.tableWidget_7.columnCount()):
                self.list.append(self.tableWidget_7.item(i, j).text())
            self.sale_book_lol.append(self.list)
            self.list = []

        self.filename = "MTA_Sale_Book.xlsx"


        df = pd.DataFrame(self.sale_book_lol, columns=["Date", "Invoice No", "Customer", "Anount Paid", "Discount", "Total GST", "12% GST", "18% GST", "5% GST"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:I', 30)
        writer.save()
        self.sale_book_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    def purchase_book_xlsx(self):

        self.list = []
        self.purchase_book_lol = []
        for i in range(self.tableWidget_6.rowCount()):
            for j in range(self.tableWidget_6.columnCount()):
                self.list.append(self.tableWidget_6.item(i, j).text())
            self.purchase_book_lol.append(self.list)
            self.list = []
        self.filename = "MTA_Purchase_Book.xlsx"

        df = pd.DataFrame(self.purchase_book_lol, columns=["ID", "Date", "Invoice No", "Invoice Date", "Dealer", "Total Amount", "GST Paid", "12% GST", "18% GST",
             "5% GST"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:I', 30)
        writer.save()
        self.purchase_book_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    def tax_book_xlsx(self):

        self.list = []
        self.tax_book_lol = []
        for i in range(self.tableWidget_5.rowCount()):
            for j in range(self.tableWidget_5.columnCount()):
                self.list.append(self.tableWidget_5.item(i, j).text())
            self.tax_book_lol.append(self.list)
            self.list = []
        self.filename = "MTA_Tax_Book.xlsx"

        df = pd.DataFrame(self.tax_book_lol, columns=["Date", "12% GST\n SALE", "18% GST\n SALE", "5% GST\n SALE", "12% GST\n PURCHASE", "18% GST\n PURCHASE",
             "5% GST\n PURCHASE"])
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']
        worksheet.set_column('A:G', 30)
        writer.save()
        self.tax_book_lol = []
        wb.open_new(r'{}/{}'.format(os.getcwd(), self.filename))

    """def from_to_day_book(self):
        ##print("Entered1")
        self.tableWidget_4.clear()
        self.conn = sqlite3.connect('mta.db')
        self.query  = "SELECT * from DayBook WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(self.from_.text(), self.to.text())
        self.result = self.conn.execute(self.query)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(7)
        self.tableWidget_4.setHorizontalHeaderLabels(["Date","Invoice No", "Party",  "Event", "Amount", "GST"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_4.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.conn.commit()"""

    def calculate_report(self):

        #print("Entered")
        self.show_gst_table()
        #print("Entered1")
        self.day_book()
        #print("Entered1")
        self.sale_book()
        self.purchase_book()
        #print("Entered1")


        self.total.clear()
        self.total_2.clear()
        self.total_3.clear()
        self.total_4.clear()
        #print("Entered2")

        self.amount_sold_worth = 0.0
        self.GST_paid = 0.0
        self.GST_collected = 0.0
        self.amount_purchase_worth = 0.0

        for i in range(self.tableWidget_4.rowCount()):
            #print("Entered3")
            if str(self.tableWidget_4.item(i, 3).text()) == "Sale":
                self.amount_sold_worth = self.amount_sold_worth + float(self.tableWidget_4.item(i, 4).text())
                self.GST_collected = self.GST_collected + float(self.tableWidget_4.item(i, 5).text())
            elif str(self.tableWidget_4.item(i, 3).text()) == "Purchase":
                self.amount_purchase_worth = self.amount_purchase_worth + float(self.tableWidget_4.item(i, 4).text())
                self.GST_paid = self.GST_paid + float(self.tableWidget_4.item(i, 5).text())

        self.total.append("Total Sale Worth : " + str(self.amount_sold_worth))
        self.total.append("Total GST Collected : " + str(round(self.GST_collected,2)))
        self.total.append("Total Purchase Worth : " + str(self.amount_purchase_worth))
        self.total.append("Total GST Paid : " + str(self.GST_paid))
        #print("Entered4")

        self.row = int(self.tableWidget_4.rowCount())
        self.tableWidget_4.insertRow(self.row)
        #self.tableWidget_4.insertRow(self.row+1)

        self.tableWidget_4.setRowHeight(self.row, 100)
        self.tableWidget_4.setRowHeight(self.row, 100)
        self.tableWidget_4.setRowHeight(self.row, 100)
        self.tableWidget_4.setRowHeight(self.row, 100)
        self.tableWidget_4.setRowHeight(self.row, 100)
        #print("Entered5")

        self.tableWidget_4.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str("Total")))
        self.tableWidget_4.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str("Total Sale : " + str(self.amount_sold_worth)+"\n"+"Total Purchase : " + str(self.amount_purchase_worth))))
        #self.tableWidget_4.setItem(self.row+1, 4, QtWidgets.QTableWidgetItem(str("Total Purchase : " + str(self.amount_purchase_worth))))
        self.tableWidget_4.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str("Total GST Collected : " + str(round(self.GST_collected,2)))+"\n"+"Total GST Paid : " + str(self.GST_paid)))
        #self.tableWidget_4.setItem(self.row+1, 5, QtWidgets.QTableWidgetItem(str("Total GST Paid : " + str(self.GST_paid))))
        self.tableWidget_4.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_4.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_4.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(" ")))

        #print("Entered6")
        self.amount_purchase_worth = 0.0
        self.GST_paid = 0.0
        self.GST_paid12 = 0.0
        self.GST_paid18 = 0.0
        self.GST_paid5 = 0.0

        for i in range(self.tableWidget_6.rowCount()):
            self.amount_purchase_worth = self.amount_purchase_worth + float(self.tableWidget_6.item(i, 6).text())
            self.GST_paid = self.GST_paid + float(self.tableWidget_6.item(i, 7).text())
            self.GST_paid12 = self.GST_paid12 + float(self.tableWidget_6.item(i, 8).text())
            self.GST_paid18 = self.GST_paid18 + float(self.tableWidget_6.item(i, 9).text())
            self.GST_paid5 = self.GST_paid5 + float(self.tableWidget_6.item(i, 10).text())

        #print("Entered7")
        self.total_3.append("Total Purchase Worth : " + str(round(self.amount_purchase_worth,2)))
        self.total_3.append("Total 12% GST Paid : " + str(self.GST_paid12))
        self.total_3.append("Total 18% GST Paid : " + str(self.GST_paid18))
        self.total_3.append("Total 5% GST Paid : " + str(self.GST_paid5))
        self.total_3.append("Total GST Paid : " + str(round(self.GST_paid,2)))

        self.row = int(self.tableWidget_6.rowCount())
        self.tableWidget_6.insertRow(self.row)
        self.tableWidget_6.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str("Total")))
        self.tableWidget_6.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str(round(self.amount_purchase_worth,2))))
        self.tableWidget_6.setItem(self.row, 7, QtWidgets.QTableWidgetItem(str(round(self.GST_paid,2))))
        self.tableWidget_6.setItem(self.row, 8, QtWidgets.QTableWidgetItem(str(self.GST_paid12)))
        self.tableWidget_6.setItem(self.row, 9, QtWidgets.QTableWidgetItem(str(self.GST_paid18)))
        self.tableWidget_6.setItem(self.row, 10, QtWidgets.QTableWidgetItem(str(self.GST_paid5)))
        self.tableWidget_6.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_6.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_6.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_6.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_6.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str(" ")))

        #print("Entered8")
        self.amount_sold_worth = 0.0
        self.GST_collect = 0.0
        self.GST_collect12 = 0.0
        self.GST_collect18 = 0.0
        self.GST_collect5 = 0.0

        for i in range(self.tableWidget_7.rowCount()):
            self.amount_sold_worth =  self.amount_sold_worth + float(self.tableWidget_7.item(i, 3).text())
            self.GST_collect = self.GST_collect + float(self.tableWidget_7.item(i, 5).text())
            self.GST_collect12 = self.GST_collect12 + float(self.tableWidget_7.item(i, 6).text())
            self.GST_collect18 = self.GST_collect18 + float(self.tableWidget_7.item(i, 7).text())
            self.GST_collect5 = self.GST_collect5 + float(self.tableWidget_7.item(i, 8).text())
        ##print("Entered9")
        self.total_4.append("Total Sale Worth : " + str(self.amount_sold_worth))
        self.total_4.append("Total 12% GST Collected : " + str(self.GST_collect12))
        self.total_4.append("Total 18% GST Collected : " + str(self.GST_collect18))
        self.total_4.append("Total 5% GST Collected : " + str(self.GST_collect5))
        self.total_4.append("Total GST Collected : " + str(round(self.GST_collect,2)))

        self.row = int(self.tableWidget_7.rowCount())
        self.tableWidget_7.insertRow(self.row)
        self.tableWidget_7.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str("Total")))
        self.tableWidget_7.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(self.amount_sold_worth)))
        self.tableWidget_7.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str(round(self.GST_collect,2))))
        self.tableWidget_7.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str(self.GST_collect12)))
        self.tableWidget_7.setItem(self.row, 7, QtWidgets.QTableWidgetItem(str(self.GST_collect18)))
        self.tableWidget_7.setItem(self.row, 8, QtWidgets.QTableWidgetItem(str(self.GST_collect5)))
        self.tableWidget_7.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_7.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str(" ")))
        self.tableWidget_7.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str(" ")))

        ##print("Entered10")

        self.GST_12_sale = 0.0
        self.GST_18_sale = 0.0
        self.GST_5_sale = 0.0
        self.GST_12_purchase = 0.0
        self.GST_18_purchase = 0.0
        self.GST_5_purchase = 0.0
        self.liability = 0.0
        self.ITC = 0.0

        self.show_gst_table()
        for i in range(self.tableWidget_5.rowCount()):
            self.GST_12_sale = self.GST_12_sale + float(self.tableWidget_5.item(i, 1).text())
            self.GST_18_sale = self.GST_18_sale + float(self.tableWidget_5.item(i, 2).text())
            self.GST_5_sale = self.GST_5_sale + float(self.tableWidget_5.item(i, 3).text())
            self.GST_12_purchase = self.GST_12_purchase + float(self.tableWidget_5.item(i, 4).text())
            self.GST_18_purchase = self.GST_18_purchase + float(self.tableWidget_5.item(i, 5).text())
            self.GST_5_purchase = self.GST_5_purchase + float(self.tableWidget_5.item(i, 6).text())

        self.total_2.append("Total 12% GST Sales  : " + str(self.GST_12_sale))
        self.total_2.append("Total 18% GST Sales  : " + str(self.GST_18_sale))
        self.total_2.append("Total 5% GST Sales    : " + str(self.GST_5_sale))
        self.total_2.append("--------------------------------------------------")
        self.total_2.append("Total 12% GST Purchase : " + str(self.GST_12_purchase))
        self.total_2.append("Total 18% GST Purchase : " + str(self.GST_18_purchase))
        self.total_2.append("Total 5% GST  Purchase  : " + str(self.GST_5_purchase))
        self.total_2.append("--------------------------------------------------")
        self.total_2.append("Total 12% Sales GST : " + str(round(self.GST_12_sale * 0.12, 2)))
        self.total_2.append("Total 18% Sales GST : " + str(round(self.GST_18_sale * 0.18, 2)))
        self.total_2.append("Total 5% Sales GST   : " + str(round(self.GST_5_sale * 0.05, 2)))
        self.total_2.append("--------------------------------------------------")
        self.total_2.append("Total GST collected : " + str(
            round(self.GST_12_sale * 0.12, 2) + round(self.GST_18_sale * 0.18, 2) + round(self.GST_5_sale * 0.05, 2)))
        self.total_2.append("--------------------------------------------------")
        self.total_2.append("Total 12% Purchase GST : " + str(round(self.GST_12_purchase * 0.12, 2)))
        self.total_2.append("Total 18% Purchase GST : " + str(round(self.GST_18_purchase * 0.18, 2)))
        self.total_2.append("Total 5% Purchase GST   : " + str(round(self.GST_5_purchase * 0.05, 2)))
        self.total_2.append("--------------------------------------")
        self.total_2.append("Total GST paid : " + str(
            round(self.GST_12_purchase * 0.12, 2) + round(self.GST_18_purchase * 0.18, 2) + round(
                self.GST_5_purchase * 0.05, 2)))

        self.row = int(self.tableWidget_5.rowCount())
        self.tableWidget_5.insertRow(self.row)
        self.tableWidget_5.setItem(self.row, 0, QtWidgets.QTableWidgetItem(str("Total")))
        self.tableWidget_5.setItem(self.row, 1, QtWidgets.QTableWidgetItem(str(self.GST_12_sale)))
        self.tableWidget_5.setItem(self.row, 2, QtWidgets.QTableWidgetItem(str(self.GST_18_sale)))
        self.tableWidget_5.setItem(self.row, 3, QtWidgets.QTableWidgetItem(str(self.GST_5_sale)))
        self.tableWidget_5.setItem(self.row, 4, QtWidgets.QTableWidgetItem(str(self.GST_12_purchase)))
        self.tableWidget_5.setItem(self.row, 5, QtWidgets.QTableWidgetItem(str(self.GST_18_purchase)))
        self.tableWidget_5.setItem(self.row, 6, QtWidgets.QTableWidgetItem(str(self.GST_5_purchase)))


    def show_gst_table(self):
        if self.today_2.isChecked():
            self.query = "SELECT * FROM GST WHERE Date = DATE('now')"
        elif self.previous_2.isChecked():
            self.query = "SELECT * from GST WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(self.from_2.text(),
                                                                                                 self.to_2.text())

        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.setColumnCount(8)
        self.tableWidget_5.setHorizontalHeaderLabels(
            ["Date", "12% GST\n SALE", "18% GST\n SALE", "5% GST\n SALE", "12% GST\n PURCHASE", "18% GST\n PURCHASE",
             "5% GST\n PURCHASE", "Invoice No"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_5.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_5.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in range(7):
                self.tableWidget_5.item(row_number, i).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.tableWidget_5.setColumnWidth(1, 150)
        self.tableWidget_5.setColumnWidth(2, 150)
        self.tableWidget_5.setColumnWidth(3, 150)
        self.tableWidget_5.setColumnWidth(4, 150)
        self.tableWidget_5.setColumnWidth(5, 150)
        self.tableWidget_5.setColumnWidth(6, 150)

        # self.calculate_report()

        """
        for i in range(self.tableWidget_5.rowCount()):
            self.taxcollected = float(self.tableWidget_5.item(i,1).text())+float(self.tableWidget_5.item(i,2).text())+float(self.tableWidget_5.item(i,3).text())
            ##print(self.taxcollected)
            self.taxpaid = float(self.tableWidget_5.item(i, 4).text())+float(self.tableWidget_5.item(i, 5).text())+float(self.tableWidget_5.item(i, 6).text())
            ##print(self.taxpaid)

            if self.taxcollected > self.taxpaid:
                self.tableWidget_5.setItem(i, 7, QtWidgets.QTableWidgetItem(str(self.taxcollected - self.taxpaid)))

            elif self.taxcollected<self.taxpaid:
                self.tableWidget_5.setItem(i, 8, QtWidgets.QTableWidgetItem(str( self.taxpaid - self.taxcollected)))
            elif self.taxcollected == self.taxpaid:
                self.tableWidget_5.setItem(i, 7, QtWidgets.QTableWidgetItem(str(0.00)))
                self.tableWidget_5.setItem(i, 8, QtWidgets.QTableWidgetItem(str(0.00)))
        """

    def day_book(self):
        if self.today.isChecked():
            self.query = "SELECT * FROM DayBook WHERE Date = DATE('now')"
        elif self.previous.isChecked():
            self.query = "SELECT * from DayBook WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(self.from_.text(),
                                                                                                     self.to.text())
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(7)
        self.tableWidget_4.setHorizontalHeaderLabels(["Date", "Invoice No", "Party", "Event", "Amount", "GST","Mode of Payment"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_4.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget_4.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.tableWidget_4.setColumnWidth(2, 300)
        self.tableWidget_4.setColumnWidth(1, 150)
        self.tableWidget_4.setColumnWidth(0, 150)
        self.tableWidget_4.setColumnWidth(3, 150)
        self.tableWidget_4.setColumnWidth(4, 300)
        self.tableWidget_4.setColumnWidth(5, 300)
        self.tableWidget_4.setColumnWidth(6, 150)


        # self.calculate_report()

    def purchase_book(self):
        if self.today_3.isChecked():
            self.query = "SELECT * FROM Purchase WHERE Date = DATE('now')"
        elif self.previous_3.isChecked():
            self.query = "SELECT * from Purchase WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(
                self.from_3.text(),
                self.to_3.text())

        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.setColumnCount(12)
        self.tableWidget_6.setHorizontalHeaderLabels(
            ["ID", "Date", "Invoice No", "Invoice Date", "Dealer","Address", "Total Amount", "GST Paid", "12% GST", "18% GST",
             "5% GST","Mode of Payment"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_6.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_6.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in range(11):
                self.tableWidget_6.item(row_number, i).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()
        self.tableWidget_6.setColumnWidth(0, 100)
        self.tableWidget_6.setColumnWidth(1, 150)
        self.tableWidget_6.setColumnWidth(2, 150)
        self.tableWidget_6.setColumnWidth(3, 150)
        self.tableWidget_6.setColumnWidth(4, 300)
        self.tableWidget_6.setColumnWidth(5, 150)
        self.tableWidget_6.setColumnWidth(6, 150)
        self.tableWidget_6.setColumnWidth(7, 150)
        self.tableWidget_6.setColumnWidth(8, 150)
        self.tableWidget_6.setColumnWidth(9, 150)
        self.tableWidget_6.setColumnWidth(10, 150)
        # self.calculate_report()

    def sale_book(self):
        if self.today_4.isChecked():
            self.query = "SELECT * FROM Sale WHERE Date = DATE('{}')".format(str(datetime.datetime.date(datetime.datetime.today())))
        elif self.previous_4.isChecked():
            self.query = "SELECT * from Sale WHERE Date BETWEEN DATE('{}') AND DATE('{}')".format(self.from_4.text(),
                                                                                                  self.to_4.text())

        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.setColumnCount(10)
        self.tableWidget_7.setHorizontalHeaderLabels(
            ["Date", "Invoice No", "Customer", "Anount Paid", "Discount", "Total GST", "12% GST", "18% GST", "5% GST","Mode of Payment"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_7.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_7.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            for i in range(9):
                self.tableWidget_7.item(row_number, i).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.tableWidget_7.setColumnWidth(0, 100)
        self.tableWidget_7.setColumnWidth(1, 150)
        self.tableWidget_7.setColumnWidth(2, 150)
        self.tableWidget_7.setColumnWidth(3, 150)
        self.tableWidget_7.setColumnWidth(4, 150)
        self.tableWidget_7.setColumnWidth(5, 150)
        self.tableWidget_7.setColumnWidth(6, 150)
        self.tableWidget_7.setColumnWidth(7, 150)
        self.tableWidget_7.setColumnWidth(8, 150)
        self.tableWidget_7.setColumnWidth(9, 150)

        self.tableWidget_7.cellEntered.connect(self.message)

    def message(self):
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
        msg.setWindowTitle("Purchase")
        msg.setText("Purchase Saved Successfully!!!")
        msg.setStandardButtons(QMessageBox.Close)
        x = msg.exec_()


    def add_company(self):

        self.conn = sqlite3.connect("mta.db")
        self.query = "INSERT INTO Companies (Company) VALUES ('{}')".format(self.companyentry.text().upper())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()

        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Company FROM Companies"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.company.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.company.addItem(str(k).strip("(',')"))


    def delete_company(self):
        self.query = "DELETE FROM Companies WHERE ID ={}".format(self.companytable.item(self.companytable.currentRow(),0).text())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()

        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Company FROM Companies"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.company.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.company.addItem(str(k).strip("(',')"))

    def edit_company(self):
        self.query = "UPDATE Companies SET Company = '{}' WHERE ID = {} ".format(self.companytable.item(self.companytable.currentRow(),1).text(), self.companytable.item(self.companytable.currentRow(),0).text())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()

        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Company FROM Companies"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.company.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.company.addItem(str(k).strip("(',')"))

    def delete_dealer(self):
        row = self.dealertable.currentRow()
        self.query = "Delete FROM Dealers WHERE ID = {} ".format(self.dealertable.item(row,0).text())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()

        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Dealers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.dealer.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.dealer.addItem(str(k).strip("(',')"))


    def edit_dealer(self):
        row = self.dealertable.currentRow()
        self.query = "UPDATE Dealers SET Dealer ='{}',Contact='{}',GSTIN='{}',Address='{}' WHERE ID = {} ".format(self.dealertable.item(row,1).text(),
                                                                                                                  self.dealertable.item(row,2).text(),
                                                                                                                  self.dealertable.item(row,3).text(),
                                                                                                                  self.dealertable.item(row,4).text(),
                                                                                                                  self.dealertable.item(row,0).text())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()

        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Dealers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.dealer.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.dealer.addItem(str(k).strip("(',')"))

    def add_dealer(self):

        self.conn = sqlite3.connect("mta.db")
        self.query = "INSERT INTO Dealers (Dealer,Contact,GSTIN,Address) VALUES ('{}',{},'{}','{}')".format(self.dealer_3.text().upper(),
                                                                             self.dealercontact.text(),
                                                                             self.dealergst.text().upper(),
                                                                             self.dealeraddress.text().upper())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Dealers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.dealer.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.dealer.addItem(str(k).strip("(',')"))

        self.show_to_select_dealer()
    """def add_rack(self):
        self.query = "INSERT INTO Racks VALUES ()".format(self.rackno.value(), self.product_2.currentText())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()

    def edit_rack(self):
        self.query = "UPDATE Racks SET Rackno = {} WHERE Products = '{}'".format(self.racktable.item(self.racktable.currentRow(),1),self.racktable.item(self.racktable.currentRow(), 0))
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_other()"""



    def show_other(self):

        self.query = "SELECT PName FROM Stock"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.product_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.product_2.addItem(str(k).strip("(',')"))
            self.product_3.addItem(str(k).strip("(',')"))

        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Name FROM Customers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.party.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.party.addItem(str(k).strip("(',')"))

        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Dealers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.deaer.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.deaer.addItem(str(k).strip("(',')"))

        """self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT * FROM Stock"
        self.result = self.conn.execute(self.query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Product ", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date", "HSN Code"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.conn.commit()"""

        self.query = "SELECT InvoiceID FROM Sales"
        self.lis = self.conn.cursor().execute(self.query)
        self.Invoiceno.clear()
        self.comboBox_3.clear()
        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.comboBox_3.addItem('MTA'+(str(k).strip("(',')"))+".pdf")
            self.Invoiceno.addItem(str(k).strip("(',')"))

        self.query = "SELECT InvoiceNo FROM Purchase"
        self.lis = self.conn.cursor().execute(self.query)
        self.invoiceno_2.clear()
        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.invoiceno_2.addItem(str(k).strip("(',')"))

        """self.query = "SELECT PName FROM Stock"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.product_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.product_2.addItem(str(k).strip("(',')"))

        self.racktable.clear()
        self.racktable.setColumnCount(3)
        self.racktable.setRowCount(0)
        self.racktable.setHorizontalHeaderLabels(["ID","Product ", "Rack"])
        self.query = "SELECT PID,PName,RackNo FROM Stock"
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        for row_number, row_data in enumerate(self.result):
            self.racktable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.racktable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.conn.commit()

        self.racktable.setColumnWidth(0, 50)
        self.racktable.setColumnWidth(1, 400)
        self.racktable.setColumnWidth(2, 150)"""

        self.customertable.clear()
        self.customertable.setColumnCount(2)
        self.customertable.setRowCount(0)
        self.customertable.setHorizontalHeaderLabels(["Customer ", "Contact"])
        self.query = "SELECT * FROM Customers "
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.conn.commit()
        for row_number, row_data in enumerate(self.result):
            self.customertable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.customertable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.customertable.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()
        self.customertable.setColumnWidth(0, 300)
        self.customertable.setColumnWidth(1, 300)

        self.query = "SELECT Name FROM Customers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.comboBox_5.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.comboBox_5.addItem(str(k).strip("(',')"))

        self.companytable.clear()
        self.companytable.setColumnCount(2)
        self.companytable.setRowCount(0)
        self.companytable.setHorizontalHeaderLabels(["ID","Company"])
        self.query = "SELECT * FROM Companies "
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.conn.commit()
        for row_number, row_data in enumerate(self.result):
            self.companytable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.companytable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number == 0:
                    self.companytable.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()
        self.companytable.setColumnWidth(0, 50)
        self.companytable.setColumnWidth(1, 550)

        self.dealertable.clear()
        self.dealertable.setColumnCount(5)
        self.dealertable.setRowCount(0)
        self.dealertable.setHorizontalHeaderLabels(["ID","Dealer", "Contact", "GSTIN", "Address"])
        self.query = "SELECT * FROM Dealers "
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        for row_number, row_data in enumerate(self.result):
            self.dealertable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dealertable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                if column_number == 0:
                    self.dealertable.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)


        self.conn.commit()
        self.dealertable.setColumnWidth(0, 50)
        self.dealertable.setColumnWidth(1, 200)
        self.dealertable.setColumnWidth(2, 150)
        self.dealertable.setColumnWidth(3, 150)
        self.dealertable.setColumnWidth(4, 200)


    def search_customer(self):
        self.customertable.clear()
        self.query = "SELECT * FROM Customers WHERE Name = '{}'".format(self.comboBox_5.currentText())
        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.conn.commit()
        for row_number, row_data in enumerate(self.result):
            self.customertable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.customertable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.customertable.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()


    def select_dealer(self):
        row = self.tableWidget_13.currentRow()
        self.dealerIDselect = int(self.tableWidget_13.item(row, 0).text())
        self.dealerselect = self.tableWidget_13.item(row, 1).text()
        self.dealeraddressselect = self.tableWidget_13.item(row, 4).text()
        self.invoicedate.setFocus()
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.setColumnCount(0)

    def save_purchase(self):

        self.conn = sqlite3.connect("mta.db")
        # ##print('here')

        if self.paymentmode.currentText() == 'Cash':
            self.query = "INSERT INTO Purchase (Date, InvoiceNo, InvoiceDate, Dealer, Tax, Amount,Mode,Credit,Debit,Balance, Address) VALUES ('{}','{}','{}','{}',{},{},'{}',{},{},{},'{}')".format \
            (str(datetime.datetime.date(datetime.datetime.today())), self.invoiceno.text(), self.invoicedate.text(),
             self.dealerselect, self.tax_purchase, self.total_payable_purchase,self.paymentmode.currentText(),0,self.total_payable_purchase,0, self.dealeraddressselect)
            ##print(self.query)
        elif self.paymentmode.currentText() == 'Credit':
            self.query = "INSERT INTO Purchase (Date, InvoiceNo, InvoiceDate, Dealer, Tax, Amount,Mode,Credit,Debit,Balance,Address) VALUES ('{}','{}','{}','{}',{},{},'{}',{},{},{},'{}')".format \
            (str(datetime.datetime.date(datetime.datetime.today())), self.invoiceno.text(), self.invoicedate.text(),
             self.dealerselect, self.tax_purchase, self.total_payable_purchase,self.paymentmode.currentText(),self.total_payable_purchase,0,self.total_payable_purchase, self.dealeraddressselect)

        self.conn.cursor().execute(self.query)
        self.conn.commit()

        self.stockQlist = []
        ##print("herer")
        for i in range(len(self.pur_productlist)):
            self.query = "SELECT Quantity FROM Stock WHERE PID = {}".format(
                self.pur_pidlist[i])
            ##print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            ##print("herer")
            self.conn.commit()
            self.m = self.lis.fetchall()
            self.m = list(dict.fromkeys(self.m))
            for k in self.m:
                self.stockQlist.append(int((str(k).strip("(',')"))))

        self.modifiedQlist = []
        ##print("herer")
        for i in range(len(self.stockQlist)):
            self.modifiedQlist.append(
                int(self.stockQlist[i]) + int(self.pur_quantitylist[i]) + int(self.pur_freelist[i]))

        # ##print(self.modifiedQlist)

        for i in range(len(self.pur_productlist)):
            self.query = "UPDATE Stock SET Quantity = {} WHERE PID = {}".format(
                self.modifiedQlist[i], self.pur_pidlist[i])
            ##print(self.query)
            self.conn.cursor().execute(self.query)
            self.conn.commit()


        self.show_stock()

        self.query = "SELECT PurchaseID FROM Purchase WHERE Date = '{}' AND InvoiceNo= '{}' AND InvoiceDate= '{}' AND Dealer= '{}' AND Tax= {} AND Amount = {}".format(
            str(datetime.datetime.date(datetime.datetime.today())), self.invoiceno.text(), self.invoicedate.text(),
            self.dealerselect, self.tax_purchase, self.total_payable_purchase)
        ##print(self.query)
        self.lis = self.conn.cursor().execute(self.query)



        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.purchaseID = (str(k).strip("(',')"))

        self.Localpurchase12 = 0.0
        self.Localpurchase18 = 0.0
        self.Localpurchase5 = 0.0

        for i in range(len(self.pur_productlist)):
            self.query = "INSERT INTO PurchaseData VALUES('{}','{}',{},'{}','{}','{}','{}','{}',{},{},{},{},'{}',{},{},{},{})".format(

                self.dealerselect,
                self.dealeraddressselect,
                self.purchaseID,
                str(datetime.datetime.date(datetime.datetime.today())),
                self.invoicedate.text(),
                self.pur_productlist[i],
                self.pur_hsnlist[i],
                self.pur_batchlist[i],
                self.pur_mrplist[i],
                self.pur_ratelist[i],

                self.pur_quantitylist[i],
                self.pur_freelist[i],
                self.pur_explist[i],
                self.pur_discountlist[i],
                self.pur_gstlist[i],
                self.pur_amountlist[i],self.pur_pidlist[i])

            ##print(self.query)
            if int(self.pur_gstlist[i]) == 12:
                self.Localpurchase12 = self.Localpurchase12 + float(self.pur_amountlist[i])
            elif int(self.pur_gstlist[i]) == 18:
                self.Localpurchase18 = self.Localpurchase18 + float(self.pur_amountlist[i])
            elif int(self.pur_gstlist[i]) == 5:
                self.Localpurchase5 = self.Localpurchase5 + float(self.pur_amountlist[i])

            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
        self.query = "UPDATE Purchase SET Local12 = {}, Local18={}, Local5={}  WHERE PurchaseID = {}".format(
            round(self.Localpurchase12 * 0.12, 2),
            round(self.Localpurchase18 * 0.18, 2),
            round(self.Localpurchase5 * 0.05, 2),
            self.purchaseID)

        self.conn.cursor().execute(self.query)
        self.conn.commit()

        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
        msg.setWindowTitle("Purchase")
        msg.setText("Purchase Saved Successfully!!!")
        msg.setStandardButtons(QMessageBox.Close)
        x = msg.exec_()

        try:
            self.query = "INSERT INTO DayBook VALUES('{}','{}','{}','Purchase',{},{},'{}')".format(
                str(datetime.datetime.date(datetime.datetime.today())), self.invoiceno.text(), self.dealerselect,
                self.total_payable_purchase,
                round(self.tax_purchase, 2),self.paymentmode.currentText())
            self.conn.cursor().execute(self.query)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Purchase")
            msg.setText("ERROR1")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        try:

            self.query = "INSERT INTO GST VALUES('{}',0,0,0,{},{},{},{})".format(
                str(datetime.datetime.date(datetime.datetime.today())), self.Localpurchase12, self.Localpurchase18,
                self.Localpurchase5,self.invoiceno.text())
            print(self.query)
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Purchase")
            msg.setText("ERROR2")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
        try:


            self.conn.cursor().execute(self.query)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Purchase")
            msg.setText("ERROR4")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

        try:

            self.Localpurchase12 = 0.0
            self.Localpurchase18 = 0.0
            self.Localpurchase5 = 0.0
            #self.calculate_report()
            self.cancel_purchase()
            self.show_other()
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Purchase")
            msg.setText("ERROR3")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()
    def cancel_purchase(self):
        self.tableWidget_3.clear()
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.setColumnCount(0)
        self.textBrowser_2.clear()
        self.invoiceno.clear()

    def calculate_purchase(self):

        ###print("Entered")
        self.textBrowser_2.clear()
        ###print("Entered")
        self.total_taxable_purchase = 0.00
        self.total_payable_purchase = 0.00
        self.tax_purchase = 0.00
        self.discount_purchase = 0.00
        self.Wdiscount_purchase = 0.0

        for i in range(self.tableWidget_3.rowCount()):
            # ##print(int(self.tableWidget_2.item(i, 6).text()))
            # ##print('here')

            """self.total_taxable_purchase = float(self.tableWidget_3.item(i, 7).text()) / (
                        1 + (float(self.tableWidget_2.item(i, 6).text())) / 100) + self.total_taxable"""
            ###print("Entered0")
            self.total_taxable_purchase = self.total_taxable_purchase + float(self.tableWidget_3.item(i, 10).text())
            self.tax_purchase = round(
                float(self.tableWidget_3.item(i, 10).text()) * float(self.tableWidget_3.item(i, 9).text()) / 100,
                2) + self.tax_purchase
            self.Wdiscount_purchase = self.Wdiscount_purchase + float(float(self.tableWidget_3.item(i, 4).text()) * float(self.tableWidget_3.item(i, 5).text()))

        ###print("Entered1")
        self.total_payable_purchase = self.total_taxable_purchase + self.tax_purchase
        self.discount_purchase = self.Wdiscount_purchase - self.total_taxable_purchase
        ###print("Entered2")

        self.textBrowser_2.setText("Total Taxable Amount : {}".format(round(self.total_taxable_purchase)))
        self.textBrowser_2.append("Total SGST           : {}".format(round(self.tax_purchase / 2), 2))
        self.textBrowser_2.append("Total CGST           : {}".format(round(self.tax_purchase / 2), 2))
        self.textBrowser_2.append("Discount             : {}".format(round(self.discount_purchase, 2)))
        self.textBrowser_2.append("Amount To Pay        : {}".format(round(self.total_payable_purchase, 2)))

    def delete_from_purchase(self):

        global dummy2
        self.tableWidget_3.removeRow(self.tableWidget_3.currentRow())
        if int(dummy2) > 0:
            self.pur_productlist.pop(self.tableWidget_3.currentRow())
            self.pur_mrplist.pop(self.tableWidget_3.currentRow())
            self.pur_ratelist.pop(self.tableWidget_3.currentRow())
            self.pur_hsnlist.pop(self.tableWidget_3.currentRow())
            self.pur_batchlist.pop(self.tableWidget_3.currentRow())
            self.pur_quantitylist.pop(self.tableWidget_3.currentRow())
            self.pur_freelist.pop(self.tableWidget_3.currentRow())
            self.pur_explist.pop(self.tableWidget_3.currentRow())
            self.pur_discountlist.pop(self.tableWidget_3.currentRow())
            self.pur_gstlist.pop(self.tableWidget_3.currentRow())
            self.pur_amountlist.pop(self.tableWidget_3.currentRow())
            self.pur_pidlist.pop(self.tableWidget_3.currentRow())
            dummy2 = dummy2 - 1


    def show_to_search_purchase(self):

        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT PName FROM Stock ORDER BY PName ASC"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.product.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.product.addItem(str(k).strip("(',')"))

    def show_dealer(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Dealers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.dealer_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.dealer_2.addItem(str(k).strip("(',')"))
        ############################################################################## UPDATE

    def show_to_select_dealer(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT * FROM Dealers WHERE Dealer = '{}'".format(self.dealer_2.currentText())
        self.result = self.conn.execute(self.query)
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.setColumnCount(5)
        self.tableWidget_13.setHorizontalHeaderLabels(
            ["ID","Dealer", "Contact", "GSTIN", "Address"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_13.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_13.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget_13.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()


        self.tableWidget_13.setColumnWidth(0, 50)
        self.tableWidget_13.setColumnWidth(1, 400)
        self.tableWidget_13.setColumnWidth(2, 150)
        self.tableWidget_13.setColumnWidth(3, 150)
        self.tableWidget_13.setColumnWidth(4, 400)

    def show_to_select_product(self):
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT PID, PName, Batch, MRP, Rate, Exp, HSN,GST, Quantity, RackNo FROM Stock WHERE PName = '{}'".format(
                self.product.currentText())
            self.result = self.conn.execute(self.query)
            self.tableWidget_12.setRowCount(0)
            self.tableWidget_12.setColumnCount(13)
            self.tableWidget_12.setHorizontalHeaderLabels(
                ["PID", "Product ", "Batch", "MRP", "Rate", "Expiry Date", "HSN", "GST", "Available", "Rack",
                 "Quantity","Free","Discount"])

            for row_number, row_data in enumerate(self.result):
                self.tableWidget_12.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_12.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    self.tableWidget_12.setItem(row_number, 10, QtWidgets.QTableWidgetItem(str("0")))
                    self.tableWidget_12.setItem(row_number, 11, QtWidgets.QTableWidgetItem(str("0")))
                    self.tableWidget_12.setItem(row_number, 12, QtWidgets.QTableWidgetItem(str("0")))
                    if column_number != 10 or 11 or 12:
                        self.tableWidget_12.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)
            self.conn.commit()

            self.tableWidget_12.setColumnWidth(0, 50)
            self.tableWidget_12.setColumnWidth(1, 200)
            self.tableWidget_12.setColumnWidth(2, 100)
            self.tableWidget_12.setColumnWidth(3, 80)
            self.tableWidget_12.setColumnWidth(4, 80)
            self.tableWidget_12.setColumnWidth(5, 200)
            self.tableWidget_12.setColumnWidth(6, 100)
            self.tableWidget_12.setColumnWidth(7, 70)
            self.tableWidget_12.setColumnWidth(8, 90)


    def add_to_purcahse(self):
        ###print('Entered')
        global dummy2

        row = self.tableWidget_12.currentRow()

        self.tableWidget_12.setHorizontalHeaderLabels(
            ["PID", "Product ", "Batch", "MRP", "Rate", "Expiry Date", "HSN", "GST", "Available", "Rack", "Quantity","Free","Discount"])
        self.PIDpur = self.tableWidget_12.item(row, 0).text()
        self.Productpur = self.tableWidget_12.item(row, 1).text()
        self.Batchpur = self.tableWidget_12.item(row, 2).text()
        self.MRPpur = self.tableWidget_12.item(row, 3).text()
        self.Ratepur = self.tableWidget_12.item(row, 4).text()
        self.Exppur = self.tableWidget_12.item(row, 5).text()
        self.HSNpur = self.tableWidget_12.item(row, 6).text()
        self.GSTpur = self.tableWidget_12.item(row, 7).text()
        self.Avlpur = self.tableWidget_12.item(row, 8).text()
        self.Rackpur = self.tableWidget_12.item(row, 9).text()
        self.Quanpur = self.tableWidget_12.item(row, 10).text()
        self.freepur = self.tableWidget_12.item(row, 11).text()
        self.Discountpur = self.tableWidget_12.item(row, 12).text()
        ###print('here1')
        self.amount = str((float(self.Quanpur)*float(self.Ratepur)) - ((float(self.Quanpur)*float(self.Ratepur))*(int(self.Discountpur)/100)))

        ###print(self.amount)

        self.tableWidget_3.setRowCount(int(dummy2) + 1)
        self.tableWidget_3.setColumnCount(12)

        self.tableWidget_3.setHorizontalHeaderLabels(
            ["Product", "HSN Code", "Batch", "MRP", "Rate", "Quantity", "Free", "Expiry Date", "Discount", "GST",
             "Amount","PID"])
        self.tableWidget_3.setItem(dummy2, 0, QtWidgets.QTableWidgetItem(str(self.Productpur)))
        self.tableWidget_3.setItem(dummy2, 1, QtWidgets.QTableWidgetItem(str(self.HSNpur)))
        self.tableWidget_3.setItem(dummy2, 2, QtWidgets.QTableWidgetItem(str(self.Batchpur)))
        self.tableWidget_3.setItem(dummy2, 3, QtWidgets.QTableWidgetItem(str(self.MRPpur)))
        self.tableWidget_3.setItem(dummy2, 4, QtWidgets.QTableWidgetItem(str(self.Ratepur)))
        self.tableWidget_3.setItem(dummy2, 5, QtWidgets.QTableWidgetItem(str(self.Quanpur)))
        self.tableWidget_3.setItem(dummy2, 6, QtWidgets.QTableWidgetItem(str(self.freepur)))
        self.tableWidget_3.setItem(dummy2, 7, QtWidgets.QTableWidgetItem(str(self.Exppur)))
        self.tableWidget_3.setItem(dummy2, 8, QtWidgets.QTableWidgetItem(str(self.Discountpur)))
        self.tableWidget_3.setItem(dummy2, 9, QtWidgets.QTableWidgetItem(str(self.GSTpur)))
        self.tableWidget_3.setItem(dummy2, 10, QtWidgets.QTableWidgetItem(self.amount))
        self.tableWidget_3.setItem(dummy2, 11, QtWidgets.QTableWidgetItem(str(self.PIDpur)))


        dummy2 = dummy2 + 1
        ###print("here2")
        self.calculate_purchase()
        ###print("here3")
        self.pur_productlist = []
        self.pur_mrplist = []
        self.pur_ratelist = []
        self.pur_hsnlist = []
        self.pur_batchlist = []
        self.pur_quantitylist = []
        self.pur_freelist = []
        self.pur_explist = []
        self.pur_discountlist = []
        self.pur_gstlist = []
        self.pur_amountlist = []
        self.pur_pidlist = []

        for i in range(self.tableWidget_3.rowCount()):
            self.pur_productlist.append(self.tableWidget_3.item(i, 0).text())
            self.pur_hsnlist.append(self.tableWidget_3.item(i, 1).text())
            self.pur_batchlist.append(self.tableWidget_3.item(i, 2).text())
            self.pur_mrplist.append(self.tableWidget_3.item(i, 3).text())
            self.pur_ratelist.append(self.tableWidget_3.item(i, 4).text())
            self.pur_quantitylist.append(self.tableWidget_3.item(i, 5).text())
            self.pur_freelist.append(self.tableWidget_3.item(i, 6).text())
            self.pur_explist.append(self.tableWidget_3.item(i, 7).text())
            self.pur_discountlist.append(self.tableWidget_3.item(i, 8).text())
            self.pur_gstlist.append(self.tableWidget_3.item(i, 9).text())
            self.pur_amountlist.append(self.tableWidget_3.item(i, 10).text())
            self.pur_pidlist.append(self.tableWidget_3.item(i, 11).text())

        self.product.setFocus()
    def save_bill(self):
        self.show_bill()

        # ##print('here')

        self.conn = sqlite3.connect("mta.db")
        self.query = "INSERT INTO Customers (Name, Contact) VALUES('{}',{})".format(self.patientname.text(),
                                                                                    int(self.lineEdit_11.text()))
        self.conn.cursor().execute(self.query)
        self.conn.commit()

        # ##print('here')
        # ##print(self.query)

        # self.query = "SELECT Amount FROM Sales WHERE Customer = '{}' AND Tax = {} AND Amount = {}".format(self.patientname.text(), round(self.tax, 2), self.total_amount)

        if self.comboBox_7.currentText() == "Cash":
            self.query = "INSERT INTO Sale (Date, Customer, Tax, Discount, Amount,Mode,Credit,Debit,Balance) VALUES('{}','{}',{},{},{},'{}',{},{},{})".format(
            str(datetime.datetime.date(datetime.datetime.today())), self.patientname.text(), round(self.tax, 2),
            round((self.total_amount_wod * float(self.Odiscount.value()) / 100), 2), self.total_amount,self.comboBox_7.currentText(), 0,self.total_amount,0)

            ##print("here")
        elif self.comboBox_7.currentText() == "Credit":
            self.query = "INSERT INTO Sale (Date, Customer, Tax, Discount, Amount,Mode,Credit,Debit,Balance) VALUES('{}','{}',{},{},{},'{}',{},{},{})".format(
            str(datetime.datetime.date(datetime.datetime.today())), self.patientname.text(), round(self.tax, 2),
            round((self.total_amount_wod * float(self.Odiscount.value()) / 100), 2), self.total_amount,self.comboBox_7.currentText(),self.total_amount,0,self.total_amount)
            ##print("here")
        self.conn.cursor().execute(self.query)
        self.conn.commit()

        self.query = "SELECT InvoiceID FROM Sale WHERE Customer = '{}' AND Tax = {} AND Amount = {}".format(
            self.patientname.text(), round(self.tax, 2), self.total_amount)

        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.InvoiceID = (str(k).strip("(',')"))

        self.stockQlist = []

        for i in range(len(self.productlist)):
            self.query = "SELECT Quantity FROM Stock WHERE PID = {}".format(self.pidlist[i])
            # ##print(self.query)
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.m = self.lis.fetchall()
            self.m = list(dict.fromkeys(self.m))
            for k in self.m:
                self.stockQlist.append(int((str(k).strip("(',')"))))
        # ##print(self.stockQlist)

        self.modifiedQlist = []
        for i in range(len(self.stockQlist)):
            self.modifiedQlist.append(int(self.stockQlist[i] - int(self.quantitylist[i])))

        # ##print(self.modifiedQlist)

        for i in range(len(self.productlist)):
            self.query = "UPDATE Stock SET Quantity = {} WHERE PID = {}".format(self.modifiedQlist[i],self.pidlist[i])
            # ##print(self.query)
            self.conn.cursor().execute(self.query)
            self.conn.commit()
        self.show_stock()

        self.Localsale12 = 0.0
        self.Localsale18 = 0.0
        self.Localsale5 = 0.0


        for i in range(len(self.productlist)):
            self.query = "INSERT INTO Sales VALUES({},'{}','{}',{},'{}',{},{},'{}',{},{},{},'{}','{}','{}',{})".format(
                self.InvoiceID,
                str(datetime.datetime.date(datetime.datetime.today())),
                self.productlist[i],
                self.hsnlist[i],
                self.batchlist[i],
                self.mrplist[i],
                self.quantitylist[i],
                self.explist[i],
                self.gstlist[i],
                self.Odiscount.value(),
                self.amountlist[i],
                self.doctor.currentText(),
                self.patientname.text(),
                self.lineEdit_11.text(),
                self.pidlist[i])

            if int(self.gstlist[i]) == 12:
                self.Localsale12 = self.Localsale12 + float(self.amountlist[i])

            elif int(self.gstlist[i]) == 18:

                self.Localsale18 = self.Localsale18 + float(self.amountlist[i])
            elif int(self.gstlist[i]) == 5:

                self.Localsale5 = self.Localsale5 + float(self.amountlist[i])
            self.lis = self.conn.cursor().execute(self.query)

            self.conn.commit()


        self.query = "UPDATE Sale SET Local12 = {}, Local18={}, Local5={}  WHERE InvoiceID = {}".format(
            round(self.Localsale12 * 0.12, 2),
            round(self.Localsale18 * 0.18, 2),
            round(self.Localsale5 * 0.05, 2),
            self.InvoiceID)
        self.conn.cursor().execute(self.query)
        self.conn.commit()


        self.query = "INSERT INTO DayBook VALUES('{}','{}','{}','Sale',{},{},'{}')".format(
            str(datetime.datetime.date(datetime.datetime.today())), self.InvoiceID, self.patientname.text(),
            self.total_amount, round(self.tax, 2),self.comboBox_7.currentText())
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()

        self.query = "INSERT INTO GST VALUES('{}',{},{},{},0,0,0,{})".format(
            str(datetime.datetime.date(datetime.datetime.today())), self.Localsale12, self.Localsale18, self.Localsale5,self.InvoiceID)
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
        msg.setWindowTitle("Sale")
        msg.setText("Bill Saved Successfully!!!")
        msg.setStandardButtons(QMessageBox.Close)
        x = msg.exec_()

        self.Localsale12 = 0
        self.Localsale18 = 0
        self.Localsale5 = 0

        self.calculate_report()

        ###################################################################### UPDATE

        self.show_other()
    def show_to_select(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT PID, PName, Batch, MRP, Rate, Exp, HSN,GST, Quantity, RackNo FROM Stock WHERE PName = '{}'".format(self.pname.currentText())
        self.result = self.conn.execute(self.query)
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.setColumnCount(11)
        self.tableWidget_11.setHorizontalHeaderLabels(
            ["PID","Product ", "Batch", "MRP", "Rate",  "Expiry Date","HSN","GST","Available", "Rack","Quantity"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget_11.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_11.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget_11.setItem(row_number, 10, QtWidgets.QTableWidgetItem(str("0")))
                if column_number!=10:
                        self.tableWidget_11.item(row_number, column_number).setFlags(QtCore.Qt.ItemIsEnabled)


        self.conn.commit()


        self.tableWidget_11.setColumnWidth(0, 50)
        self.tableWidget_11.setColumnWidth(1, 200)
        self.tableWidget_11.setColumnWidth(2, 100)
        self.tableWidget_11.setColumnWidth(3, 80)
        self.tableWidget_11.setColumnWidth(4, 80)
        self.tableWidget_11.setColumnWidth(5, 200)
        self.tableWidget_11.setColumnWidth(6, 100)
        self.tableWidget_11.setColumnWidth(7, 70)
        self.tableWidget_11.setColumnWidth(8, 90)

    def add_to_bill(self):

        global dummy1
        row = self.tableWidget_11.currentRow()

        self.tableWidget_11.setHorizontalHeaderLabels(
            ["PID", "Product ", "Batch", "MRP", "Rate", "Expiry Date","HSN","GST","Available", "Rack", "Quantity"])
        self.PIDsale = self.tableWidget_11.item(row,0 ).text()
        self.Productsale = self.tableWidget_11.item(row, 1).text()
        self.Batchsale = self.tableWidget_11.item(row, 2).text()
        self.MRPsale = self.tableWidget_11.item(row, 3).text()
        self.Ratesale = self.tableWidget_11.item(row, 4).text()
        self.Expsale = self.tableWidget_11.item(row, 5).text()
        self.HSNsale = self.tableWidget_11.item(row, 6).text()
        self.GSTsale = self.tableWidget_11.item(row, 7).text()
        self.Avlsale = self.tableWidget_11.item(row, 8).text()
        self.Racksale = self.tableWidget_11.item(row, 9).text()
        self.Quansale = self.tableWidget_11.item(row, 10).text()
        ##print(self.Quansale)
        self.amount = float(self.MRPsale)*float(self.Quansale)
        ##print(self.amount)

        self.tableWidget_2.setRowCount(int(dummy1) + 1)
        self.tableWidget_2.setColumnCount(9)
        self.tableWidget_2.setHorizontalHeaderLabels(
            ["Product", "HSN Code", "Batch", "MRP", "Quantity", "Expiry Date", "GST", "Amount","PID"])

        self.tableWidget_2.setItem(dummy1, 0, QtWidgets.QTableWidgetItem(str(self.Productsale)))
        self.tableWidget_2.setItem(dummy1, 1, QtWidgets.QTableWidgetItem(str(self.HSNsale)))
        self.tableWidget_2.setItem(dummy1, 2, QtWidgets.QTableWidgetItem(str(self.Batchsale)))
        self.tableWidget_2.setItem(dummy1, 3, QtWidgets.QTableWidgetItem(str(self.MRPsale)))
        self.tableWidget_2.setItem(dummy1, 4, QtWidgets.QTableWidgetItem(str(self.Quansale)))
        self.tableWidget_2.setItem(dummy1, 5, QtWidgets.QTableWidgetItem(str(self.Expsale)))
        self.tableWidget_2.setItem(dummy1, 6, QtWidgets.QTableWidgetItem(str(self.GSTsale)))
        self.tableWidget_2.setItem(dummy1, 7, QtWidgets.QTableWidgetItem(str(self.amount)))
        self.tableWidget_2.setItem(dummy1, 8, QtWidgets.QTableWidgetItem(str(self.PIDsale)))
        dummy1 = dummy1 + 1

        self.productlist = []
        self.hsnlist = []
        self.mrplist = []
        self.batchlist = []
        self.quantitylist = []
        self.explist = []
        self.gstlist = []
        self.amountlist = []
        self.pidlist = []
        for i in range(self.tableWidget_2.rowCount()):
            self.productlist.append(self.tableWidget_2.item(i, 0).text())
            self.hsnlist.append(self.tableWidget_2.item(i, 1).text())
            self.batchlist.append(self.tableWidget_2.item(i, 2).text())
            self.mrplist.append(self.tableWidget_2.item(i, 3).text())
            self.quantitylist.append(self.tableWidget_2.item(i, 4).text())
            self.explist.append(self.tableWidget_2.item(i, 5).text())
            self.gstlist.append(self.tableWidget_2.item(i, 6).text())
            self.amountlist.append(self.tableWidget_2.item(i, 7).text())
            self.pidlist.append(self.tableWidget_2.item(i, 8).text())

        self.pname.setFocus()

    def show_bill(self):
        self.textBrowser.clear()
        # self.save_last_invoice()
        # self.textBrowser.setText("Invoice No : "+str(datetime.datetime.date(datetime.datetime.today()))+str(self.subscript)+" "*100+str(datetime.datetime.date(datetime.datetime.today()))+"\n"*2)
        self.textBrowser.append("Maa Tara Ayurveda")
        self.textBrowser.append("Melarmath, H.G.B Road, Agartala ")
        self.textBrowser.append("Tripura(West), PIN - 799001" + "\n")
        self.textBrowser.append("Patient Name  : " + self.patientname.text())
        self.textBrowser.append("Prescribed by : " + self.doctor.currentText())
        self.textBrowser.append(":" * 150)
        self.textBrowser.append(
            "SL".center(5, " ") + "|" + "Product".center(40, " ") + "|" + "Batch".center(15, " ") + "|" + "MRP".center(
                10, " ") + "|" + "Qty".center(10, " ") + "|" + "Exp".center(15, " ") + "|" + "Amount".center(20,
                                                                                                                     " "))
        self.textBrowser.append(":" * 150)
        # ##print(self.textBrowser.toPlainText())
        self.list = []
        self.list_of_list = []
        for i in range(self.tableWidget_2.rowCount()):
            for j in range(self.tableWidget_2.columnCount()-1):
                self.list.append(self.tableWidget_2.item(i, j).text())
            self.list_of_list.append(self.list)
            self.list = []

        # ##print(self.list_of_list)
        for i, list1 in enumerate(self.list_of_list):
            self.textBrowser.append(str(i).center(5, " ") + "|" +
                                    str(list1[0])[:40].center(40, " ") + "|" +
                                    str(list1[2]).center(15, " ") + "|" +
                                    str(list1[3]).center(10, " ") + "|" +
                                    str(list1[4]).center(10, " ") + "|" +
                                    str(list1[5]).center(15, " ") + "|" +
                                    str(list1[7]).center(20, " "))

            self.list_of_list[i].insert(0, i)
            self.textBrowser.append("-" * 130)

        self.total_taxable = 0.00
        self.total_amount = 0.00
        self.total_amount_wod = 0.00
        self.tax = 0.0
        for i in range(self.tableWidget_2.rowCount()):
            # ##print(int(self.tableWidget_2.item(i, 6).text()))
            # ##print('here')

            self.total_taxable = float(self.tableWidget_2.item(i, 7).text()) / (
                        1 + (float(self.tableWidget_2.item(i, 6).text())) / 100) + self.total_taxable
            self.total_amount_wod = self.total_amount_wod + float(self.tableWidget_2.item(i, 7).text())

        self.total_amount = self.total_amount_wod - round((self.total_amount_wod * float(self.Odiscount.value()) / 100),
                                                          2)
        self.tax = self.total_amount_wod - self.total_taxable
        self.textBrowser.append("Total Taxable Amount : {}".rjust(110, " ").format(round(self.total_taxable, 2)))
        self.textBrowser.append("Total SGST           : {}".rjust(110, " ").format(round(self.tax, 4) / 2))
        self.textBrowser.append("Total SGST           : {}".rjust(110, " ").format(round(self.tax, 4) / 2))
        self.textBrowser.append("Discount             : {}".rjust(110, " ").format(
            round((self.total_amount_wod * float(self.Odiscount.value()) / 100)), 2))
        self.textBrowser.append("Total  Amount        : {}".rjust(110, " ").format(round(self.total_amount_wod, 2)))
        self.textBrowser.append("Amount to pay        : {}".rjust(110, " ").format(round(self.total_amount, 2)))

    def show_pdf(self):
        global dummy1

        # ##print(self.InvoiceID)

        self.info = [
            ['Invoice No : {}'.format(self.InvoiceID), 'Patient name : {}'.format(self.patientname.text().upper())],
            ['Date : {}'.format(str(datetime.datetime.date(datetime.datetime.today()))),
             'Patient Contact : {}'.format(self.lineEdit_11.text())],
            ['', 'Prescribed By : {}'.format(self.doctor.currentText())]
        ]

        self.amount_info = [['Taxable Amount :' + str(round(self.total_taxable, 2)), 'SGST :' + str(round(self.tax, 2) / 2),
                             'CGST :' + str(round(self.tax / 2, 2)),
                             'Discount :' + str(
                                 round((self.total_amount_wod * float(self.Odiscount.value()) / 100), 2)),
                             'Amount To Pay :' + str(round(self.total_amount))]]

        self.header = [["Sl", "Product", "HSN Code", "Batch", "MRP", "Quantity", "Expiry Date", "GST",
                        "Amount"]]  # .append(self.list_of_list)

        for i in range(len(self.list_of_list)):
            self.header.append(self.list_of_list[i])

        # self.list_of_list = [self.header,self.list_of_list[0],self.list_of_list[1],self.list_of_list[2],self.list_of_list[3],self.list_of_list[4],self.list_of_list[5],self.list_of_list[6],self.list_of_list[7],self.list_of_list[8]]
        # self.header.append(self.list_of_list)
        # self.header.append(self.amount_info)

        self.buffer = 'buffer.pdf'
        self.fileName = '{}.pdf'.format("mta" + str(self.InvoiceID))
        self.pdf = SimpleDocTemplate(self.buffer, pagesize=landscape(A5), leftMargin=0, rightMargin=0,
                                     topMargin=80, bottomMargin=20)

        self.info_table = Table(self.info, hAlign="CENTER")
        self.product_table = Table(self.header, hAlign="CENTER")
        self.amount_table = Table(self.amount_info, hAlign="CENTER")

        # add style
        self.info_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), -5),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 5)

        ])

        self.product_style1 = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ])

        # 3) Add borders('GRID', (0, 0), (-1, -1), 1, colors.purple),
        self.product_style2 = TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        self.info_table.setStyle(self.info_style)
        self.product_table.setStyle(self.product_style2)
        self.amount_table.setStyle(self.product_style1)

        # ##print("Style created")

        self.elems = []

        self.elems.append(self.info_table)
        self.elems.append(self.product_table)
        self.elems.append(self.amount_table)

        # ##print("Appended")

        self.pdf.build(self.elems)
        # wb.open_new(r'{}/{}'.format(os.getcwd(), self.buffer))

        pdf_file = "Watermark.pdf"
        watermark = self.buffer
        merged_file = self.fileName
        input_file = open(pdf_file, 'rb')
        input_pdf = PyPDF2.PdfFileReader(pdf_file)
        watermark_file = open(watermark, 'rb')
        watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
        pdf_page = input_pdf.getPage(0)
        watermark_page = watermark_pdf.getPage(0)
        pdf_page.mergePage(watermark_page)
        output = PyPDF2.PdfFileWriter()
        output.addPage(pdf_page)
        merged_file = open(self.fileName, 'wb')
        output.write(merged_file)
        merged_file.close()
        watermark_file.close()
        input_file.close()

        wb.open_new(r'{}/{}'.format(os.getcwd(), self.fileName))

        self.textBrowser.clear()
        self.tableWidget_2.clear()
        self.tableWidget_11.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_11.setColumnCount(0)
        self.patientname.clear()
        self.lineEdit_11.clear()
        self.Odiscount.clear()
        self.patientname.setFocus()
        dummy1 = 0

    def delete_from_bill(self):
        global dummy1
        try:
            self.tableWidget_2.removeRow(self.tableWidget_2.currentRow())
            if dummy1 > 0:
                self.productlist.pop(self.tableWidget_2.currentRow())
                self.mrplist.pop(self.tableWidget_2.currentRow())
                self.batchlist.pop(self.tableWidget_2.currentRow())
                self.quantitylist.pop(self.tableWidget_2.currentRow())
                dummy1 = dummy1 - 1

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('SmoothLogo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Couldn't Delete!!!")  # Add Error line no.
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

    """def show_batch(self):
        self.item = self.pname.currentText()
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Batch FROM Stock WHERE PName = '{}'".format(self.item)
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.batch_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.batch_2.addItem(str(k).strip("(',')"))
        self.show_mrp()

    def show_mrp(self):
        self.query = "SELECT MRP FROM Stock WHERE PName = '{}' AND Batch = '{}'".format(self.item,
                                                                                        self.batch_2.currentText())
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        #self.mrp_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.mrp_2.addItem(str(k).strip("(',')"))

        self.query = "SELECT Exp FROM Stock WHERE PName = '{}' AND Batch = '{}'".format(self.item,
                                                                                        self.batch_2.currentText())
        self.lis = self.conn.cursor().execute(self.query)

        self.conn.commit()
        self.comboBox_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))

        for k in self.m:
            self.comboBox_2.addItem(str(k).strip("(',')"))

        self.query = "SELECT GST FROM Stock WHERE PName = '{}' AND Batch = '{}'".format(self.item,
                                                                                        self.batch_2.currentText())
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.gst_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.gst_2.addItem(str(k).strip("(',')"))

        self.show_quantity()

    def show_quantity(self):
        self.query = "SELECT Quantity FROM Stock WHERE  PName = '{}' AND Batch = '{}'".format(self.item,
                                                                                              self.batch_2.currentText())
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.quantity_2.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))

        for k in self.m:
            k = int(str(k).strip("(',')"))
            for i in range(k):
                self.quantity_2.addItem(str(i).strip("(',')"))"""

    def show_to_search(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT PName FROM Stock ORDER BY PName ASC"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.pname.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.pname.addItem(str(k).strip("(',')"))
        self.conn.commit()

    def show_doc(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT * FROM Doctors"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.doctor.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.doctor.addItem(str(k).strip("(',')"))

    def add_doctor(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "INSERT INTO Doctors VALUES ('{}')".format(str(self.adddoctor.text()))
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_doc()

    def short_date(self):

        self.query = "SELECT * FROM Stock WHERE Exp BETWEEN DATE('now') AND DATE('now','+4 month')"

        self.conn = sqlite3.connect("mta.db")
        self.result = self.conn.execute(self.query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setHorizontalHeaderLabels(
            ["PID", "Product", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date",
             "HSN Code", "Rack No"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()
        self.show_summery()

    def short_list(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT * FROM Stock WHERE Quantity <= 5"
        self.result = self.conn.execute(self.query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setHorizontalHeaderLabels(
            ["PID", "Product", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date",
             "HSN Code", "Rack No"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()
        self.show_summery()
    def exp_list(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT * FROM Stock WHERE Exp BETWEEN DATE('now','-4 month') AND DATE('now')"
        self.result = self.conn.execute(self.query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setHorizontalHeaderLabels(
            ["PID", "Product", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date",
             "HSN Code", "Rack No"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                self.tableWidget.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()
        self.show_summery()
    def toggled(self):
        self.conn = sqlite3.connect("mta.db")

        if self.companywise.isChecked():
            self.search_by = "Company"
            self.query = "SELECT Company FROM Stock"
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.comboBox.clear()
            self.m = self.lis.fetchall()
            self.m = list(dict.fromkeys(self.m))
            for k in self.m:
                self.comboBox.addItem(str(k).strip("(',')"))


        elif self.dealerwise.isChecked():
            self.search_by = "DEALER"
            self.query = "SELECT DEALER FROM Stock"
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.comboBox.clear()
            self.m = self.lis.fetchall()
            self.m = list(dict.fromkeys(self.m))
            for k in self.m:
                self.comboBox.addItem(str(k).strip("(',')"))


        else:
            self.search_by = "PName"
            self.query = "SELECT PName FROM Stock ORDER BY PName ASC"
            self.lis = self.conn.cursor().execute(self.query)
            self.conn.commit()
            self.comboBox.clear()
            for k in self.lis.fetchall():
                self.comboBox.addItem(str(k).strip("(',')"))

        self.conn.commit()

    def search_product(self):
        try:
            self.conn = sqlite3.connect("mta.db")
            self.query = "SELECT * FROM Stock WHERE {} LIKE '{}%'".format(self.search_by, self.comboBox.currentText())
            self.result = self.conn.execute(self.query)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(12)
            self.tableWidget.setHorizontalHeaderLabels(
                ["PID","Product", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date", "HSN Code","Rack No"])

            for row_number, row_data in enumerate(self.result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    self.tableWidget.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
            self.conn.commit()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("I guess, Search Box is Empty!!!")
            msg.setStandardButtons(QMessageBox.Close)
            x = msg.exec_()

    def delete_product(self):
        self.conn = sqlite3.connect('mta.db')
        r = self.tableWidget.currentRow()

        self.query = "DELETE FROM Stock WHERE PID = '{}'".format(self.tableWidget.item(r, 0).text())

        self.conn.execute(self.query)
        self.conn.commit()

        self.show_stock()
        self.show_to_search()
        self.show_summery()

    def edit_stock(self):
        self.conn = sqlite3.connect('mta.db')
        r = self.tableWidget.currentRow()
        """##print(r)
        ##print(self.tableWidget.currentColumn())
        ##print(self.tableWidget.item(3, 5).text())"""

        self.query = "UPDATE Stock SET PName = '{}', Batch = '{}', MRP = {}, Rate={}, DEALER='{}', " \
                     "Company='{}', GST={}, Quantity={}, Exp='{}', HSN='{}'  " \
                     "RackNo = '{}' WHERE PID = '{}'".format(
            float(self.tableWidget.item(r, 1).text()),
            float(self.tableWidget.item(r, 2).text()),
            self.tableWidget.item(r, 3).text(),
            self.tableWidget.item(r, 4).text(),
            int(self.tableWidget.item(r, 5).text()),
            int(self.tableWidget.item(r, 6).text()),
            self.tableWidget.item(r, 7).text(),
            self.tableWidget.item(r, 8).text(),

            self.tableWidget.item(r, 9).text(),self.tableWidget.item(r, 10).text(),self.tableWidget.item(r, 11).text(), self.tableWidget.item(r, 0).text())
        self.conn.execute(self.query)
        self.conn.commit()

        self.show_to_search()
        self.show_summery()

    def show_summery(self):
        self.conn = sqlite3.connect('mta.db')
        self.query = 'SELECT MRP,Quantity,Rate FROM Stock'
        self.lis = self.conn.cursor().execute(self.query)
        totalvalueMRP = 00.0
        totalvalueRate = 00.0
        for k in self.lis:
            valueMRP = k[0] * k[1]
            valueRate = k[1] * k[2]
            totalvalueMRP = totalvalueMRP + valueMRP
            totalvalueRate = totalvalueRate + valueRate
        self.summery.setText("Total value of all the products : {}".format(
            totalvalueMRP) + "\n" + "Total Rate of all the products : {}".format(totalvalueRate))

    def add_product_to_stock(self):

        self.conn = sqlite3.connect("mta.db")
        self.query = "INSERT INTO Stock(PName, Batch, MRP, Rate, DEALER, Company, GST, Quantity, Exp, HSN,RackNo) VALUES ('{}','{}',{},{},'{}','{}',{},{},'{}','{}','{}')".format(
            self.name.text().upper(), self.batch.text(), self.mrp.value(), self.rate.value(), self.dealer.currentText(),
            self.company.currentText(), self.gst.value(), self.quantity.value(), str(self.exp.text()), self.hsn.text(),self.lineEdit.text())
        self.conn.execute(self.query)
        self.conn.commit()

        self.show_stock()
        self.show_summery()
        self.show_to_search()
        self.show_to_select_product()

    def show_stock(self):
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT * FROM Stock ORDER BY PName ASC"
        self.result = self.conn.execute(self.query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setHorizontalHeaderLabels(
            ["PID","Product ", "Batch", "MRP", "Rate", "Dealer", "Company", "GST", "Quantity", "Expiry Date", "HSN Code","Rack"])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):

                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

                self.tableWidget.item(row_number, 0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.conn.commit()

        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 80)
        self.tableWidget.setColumnWidth(5, 200)
        self.tableWidget.setColumnWidth(6, 100)
        self.tableWidget.setColumnWidth(7, 70)
        self.tableWidget.setColumnWidth(8, 90)
        self.tableWidget.setColumnWidth(9, 110)
        self.tableWidget.setColumnWidth(10, 100)
        self.tableWidget.setColumnWidth(11, 80)


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(890, 830)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/SmoothLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("background:url(:/newPrefix/bg5.jpg)")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("QLabel{background:transparent}\n"
                                     "QPushButton { color: black; background-color: white;background: rgba(255,255,255,50%) }\n"
                                     "\n"
                                     "QLineEdit:hover{ border-style: outset;\n"
                                     "    border-width: 2px;\n"
                                     "    border-color: beige; }\n"
                                     "QPushButton:hover { color:white }\n"
                                     "QRadioButton:!hover { color: black;background: transparent }\n"
                                     "QRadioButton:hover { color:white }\n"
                                     "/*QTableWidget:!hover{background: qlineargradient(spread:pad, x1:0.45911, y1:0.007, x2:0.463873, y2:1, stop:0 rgba(51, 71, 228, 233), stop:1 rgba(255, 255, 255, 255));background: transparent}*/\n"
                                     "/*QTextBrowser:!hover{background:qlineargradient(spread:pad, x1:0.432, y1:1, x2:0.506, y2:0, stop:0 rgba(57, 162, 25, 133), stop:1 rgba(255, 255, 255, 255));background: transparent}*/\n"
                                     "\n"
                                     "QTableWidget:!hover{background: rgba(255,255,255,50%)}\n"
                                     "QTextBrowser:!hover{background: rgba(255,255,255,50%)}\n"
                                     "\n"
                                     "QTableWidget:hover{background: rgb(255,255,255)}\n"
                                     "QTextBrowser:hover{background: rgb(255,255,255)}\n"
                                     "\n"
                                     "QTabBar::tab:selected {background: rgba(255,255,255,50%)}\n"
                                     "QTabBar::tab:!selected:hover { background:transparent}\n"
                                     "QTabBar::tab:top, QTabBar::tab:bottom {\n"
                                     "    min-width: 8ex;\n"
                                     "    margin-right: -1px;\n"
                                     "    padding: 5px 10px 5px 10px;\n"
                                     "}\n"
                                     "QSpinBox:hover{border-style: outset;\n"
                                     "    border-width: 2px;\n"
                                     "    border-color: beige; background: rgba(255,255,255,50%) }\n"
                                     "QDoubleSpinBox:hover{border-style: outset;\n"
                                     "    border-width: 2px;\n"
                                     "    border-color: beige; background: rgba(255,255,255,50%) }\n"
                                     "QSpinBox:!hover{ background:rgba(255,255,255,50%)}\n"
                                     "QComboBox:!hover{ background:  rgba(255,255,255,50%) }\n"
                                     "QComboBox:hover{ background:  rgba(255,255,255,100%) }\n"
                                     "QDoubleSpinBox:!hover{ background: rgba(255,255,255,50%) }\n"
                                     "QDateEdit:!hover{ background: rgba(255,255,255,50%)}\n"
                                     "QDateEdit:hover{ border-style: outset;\n"
                                     "    border-width: 2px;\n"
                                     "    border-color: beige; background: rgba(255,255,255,50%) }\n"
                                     "QLineEdit{font-style: italic}\n"
                                     "QTextBrowser{font-style: italic;}\n"
                                     "QLabel{ font-family: Helvetica;font-weight: bold}\n"
                                     "QLineEdit{border: none; border-bottom: 1px solid #717072 }\n"
                                     "QDateEdit{border: none; border-bottom: 1px solid #717072;background: rgba(255,255,255,50%)}\n"
                                     "QSpinBox{border: none; border-bottom: 1px solid #717072;background: rgba(255,255,255,50%) }\n"
                                     "\n"
                                     "QDoubleSpinBox{border: none; border-bottom: 1px solid #717072 }\n"
                                     "\n"
                                     "QTabWidget::pane {\n"
                                     "    border:none;\n"
                                     "    background:url(:/newPrefix/bg5.jpg)}\n"
                                     "\n"
                                     "QWidget{font-style: italic;font-weight: 500; font-family: Helvetica;font-size:18px}\n"
                                     "QLineEdit:!hover{background: rgba(255,255,255,50%)}\n"
                                     "QComboBox{background: rgba(255,255,255,50%)}\n"
                                     "QTextEdit:!hover{background: rgba(255,255,255,50%)}\n"
                                     "QTextEdit:hover{background: rgba(255,255,255,100%)}\n"
                                     "QLineEdit:hover{ background: rgba(255,255,255,50%) }\n"
                                     "QTableWidget:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QLineEdit:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QDateEdit:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QComboBox:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QSpinBox:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QDoubleSpinBox:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QPushButton:focus{ background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "QTextBrowser:focus{  background-color: white;background: rgba(255,255,255,100%) }\n"
                                     "\n"
                                     "\n"
                                     "")

        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setMinimumSize(QtCore.QSize(450, 0))
        self.name.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.name.setFont(font)
        self.name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout.addWidget(self.name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.batch = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.batch.sizePolicy().hasHeightForWidth())
        self.batch.setSizePolicy(sizePolicy)
        self.batch.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_2.setFont(font)
        self.batch.setObjectName("batch")
        self.batch.setText('00000')
        self.batch.setFont(font)

        self.horizontalLayout_2.addWidget(self.batch)
        self.batch.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.mrp = QtWidgets.QDoubleSpinBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mrp.sizePolicy().hasHeightForWidth())
        self.mrp.setSizePolicy(sizePolicy)
        self.mrp.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.mrp.setFont(font)

        self.mrp.setObjectName("mrp")
        self.mrp.setMaximum(999999.00)

        self.horizontalLayout_3.addWidget(self.mrp)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_4.setFont(font)

        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.exp = QtWidgets.QDateEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exp.sizePolicy().hasHeightForWidth())
        self.exp.setSizePolicy(sizePolicy)
        self.exp.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.exp.setFont(font)
        self.exp.setCurrentSection(QtWidgets.QDateTimeEdit.MonthSection)
        self.exp.setObjectName("exp")
        self.horizontalLayout_4.addWidget(self.exp)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_5.setFont(font)

        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.quantity = QtWidgets.QSpinBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantity.sizePolicy().hasHeightForWidth())
        self.quantity.setSizePolicy(sizePolicy)
        self.quantity.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.quantity.setFont(font)
        self.quantity.setMaximum(999999999)
        self.quantity.setObjectName("quantity")
        self.horizontalLayout_5.addWidget(self.quantity)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_6.setFont(font)

        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.hsn = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hsn.sizePolicy().hasHeightForWidth())
        self.hsn.setSizePolicy(sizePolicy)
        self.hsn.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.hsn.setFont(font)

        self.hsn.setObjectName("hsn")
        self.hsn.setText('00000')
        self.hsn.setValidator(QtGui.QIntValidator())

        self.horizontalLayout_6.addWidget(self.hsn)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_7.setFont(font)

        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.rate = QtWidgets.QDoubleSpinBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rate.sizePolicy().hasHeightForWidth())
        self.rate.setSizePolicy(sizePolicy)
        self.rate.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.rate.setFont(font)
        self.rate.setMaximum(999999.00)

        self.rate.setObjectName("rate")
        self.horizontalLayout_7.addWidget(self.rate)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.gst = QtWidgets.QSpinBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gst.sizePolicy().hasHeightForWidth())
        self.gst.setSizePolicy(sizePolicy)
        self.gst.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.gst.setFont(font)
        self.gst.setObjectName("gst")
        self.gst.setValue(12)

        self.horizontalLayout_8.addWidget(self.gst)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        self.dealer = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dealer.sizePolicy().hasHeightForWidth())
        self.dealer.setSizePolicy(sizePolicy)
        self.dealer.setMinimumSize(QtCore.QSize(450, 0))
        self.dealer.setObjectName("dealer")
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Dealer FROM Dealers"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.dealer.addItem((str(k).strip("(',')")))

        # self.dealer.setText('Not Entered')

        self.horizontalLayout_11.addWidget(self.dealer)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_11 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_13.addWidget(self.label_11)
        self.company = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.company.sizePolicy().hasHeightForWidth())
        self.company.setSizePolicy(sizePolicy)
        self.company.setMinimumSize(QtCore.QSize(450, 0))
        self.company.setObjectName("company")
        # self.company.setText('Not Entered')
        self.conn = sqlite3.connect("mta.db")
        self.query = "SELECT Company FROM Companies"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.company.addItem((str(k).strip("(',')")))

        self.horizontalLayout_13.addWidget(self.company)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_77 = QtWidgets.QLabel(self.tab)
        self.label_77.setObjectName("label_77")
        self.horizontalLayout_9.addWidget(self.label_77)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(450, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout_9.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.line_42 = QtWidgets.QFrame(self.tab)
        self.line_42.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_42.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_42.setObjectName("line_42")
        self.verticalLayout.addWidget(self.line_42)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.companywise = QtWidgets.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.companywise.setFont(font)
        self.companywise.setObjectName("companywise")
        self.companywise.clicked.connect(self.toggled)

        self.horizontalLayout_10.addWidget(self.companywise)
        self.dealerwise = QtWidgets.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealerwise.setFont(font)
        self.dealerwise.setObjectName("dealerwise")
        self.dealerwise.clicked.connect(self.toggled)

        self.horizontalLayout_10.addWidget(self.dealerwise)
        self.productwise = QtWidgets.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.productwise.setFont(font)
        self.productwise.setObjectName("productwise")
        self.productwise.clicked.connect(self.toggled)

        self.horizontalLayout_10.addWidget(self.productwise)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.comboBox = QtWidgets.QComboBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        shortcut3 = QtWidgets.QShortcut(QtGui.QKeySequence("F1"), self.comboBox)
        shortcut3.activated.connect(self.search_product)

        self.verticalLayout.addWidget(self.comboBox)
        self.line_44 = QtWidgets.QFrame(self.tab)
        self.line_44.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_44.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_44.setObjectName("line_44")
        self.verticalLayout.addWidget(self.line_44)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.shrtdate = QtWidgets.QRadioButton(self.tab)
        self.shrtdate.clicked.connect(self.short_date)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.shrtdate.setFont(font)
        self.shrtdate.setObjectName("shrtdate")
        self.horizontalLayout_12.addWidget(self.shrtdate)

        self.shortlist = QtWidgets.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.shortlist.setFont(font)
        self.shortlist.setObjectName("shortlist")
        self.shortlist.clicked.connect(self.short_list)

        self.horizontalLayout_12.addWidget(self.shortlist)
        self.showall = QtWidgets.QRadioButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.showall.setFont(font)
        self.showall.setObjectName("showall")

        self.showall.clicked.connect(self.show_stock)

        self.horizontalLayout_12.addWidget(self.showall)
        self.radioButton = QtWidgets.QRadioButton(self.tab)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.exp_list)
        self.horizontalLayout_12.addWidget(self.radioButton)

        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.line_43 = QtWidgets.QFrame(self.tab)
        self.line_43.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_43.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_43.setObjectName("line_43")
        self.verticalLayout.addWidget(self.line_43)
        self.summery = QtWidgets.QTextBrowser(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.summery.sizePolicy().hasHeightForWidth())
        self.summery.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.summery.setFont(font)
        self.summery.setObjectName("summery")
        self.show_summery()
        self.verticalLayout.addWidget(self.summery)
        self.line_40 = QtWidgets.QFrame(self.tab)
        self.line_40.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_40.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_40.setObjectName("line_40")
        self.verticalLayout.addWidget(self.line_40)
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.duplicate)

        self.horizontalLayout_55.addWidget(self.pushButton_3)
        self.Search = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.Search.setFont(font)
        self.Search.setObjectName("Search")
        self.Search.clicked.connect(self.search_product)

        self.horizontalLayout_55.addWidget(self.Search)
        # self.horizontalLayout_9.addWidget(self.Search)
        self.edit = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.edit.setFont(font)
        self.edit.setObjectName("edit")
        self.edit.clicked.connect(self.edit_stock)

        self.horizontalLayout_55.addWidget(self.edit)
        self.delete_2 = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.delete_2.setFont(font)
        self.delete_2.setObjectName("delete_2")
        self.delete_2.clicked.connect(self.delete_product)

        self.horizontalLayout_55.addWidget(self.delete_2)
        self.print = QtWidgets.QPushButton(self.tab)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.print.setFont(font)
        self.print.setObjectName("print")
        self.print.clicked.connect(self.stock_xlsx)
        self.horizontalLayout_55.addWidget(self.print)
        self.addproduct = QtWidgets.QPushButton(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.addproduct.setFont(font)
        self.addproduct.setObjectName("addproduct")
        self.addproduct.clicked.connect(self.add_product_to_stock)

        self.horizontalLayout_55.addWidget(self.addproduct)
        self.verticalLayout.addLayout(self.horizontalLayout_55)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        shortcut3 = QtWidgets.QShortcut(QtGui.QKeySequence("Delete"), self.tableWidget)
        shortcut3.activated.connect(self.delete_product)
        """for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            #self.tableWidget.item(i,0).setFlags(QtCore.Qt.S)"""

        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.line_41 = QtWidgets.QFrame(self.tab)
        self.line_41.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_41.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_41.setObjectName("line_41")
        self.gridLayout_2.addWidget(self.line_41, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        ########################################################
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_18.addWidget(self.label_12)
        self.patientname = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.patientname.sizePolicy().hasHeightForWidth())
        self.patientname.setSizePolicy(sizePolicy)
        self.patientname.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.patientname.setFont(font)
        self.patientname.setObjectName("patientname")
        self.patientname.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout_18.addWidget(self.patientname)
        self.verticalLayout_9.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_24 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_24.addWidget(self.label_24)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_11.sizePolicy().hasHeightForWidth())
        self.lineEdit_11.setSizePolicy(sizePolicy)
        self.lineEdit_11.setMinimumSize(QtCore.QSize(450, 0))

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setDragEnabled(False)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_11.setValidator(QtGui.QIntValidator())
        self.horizontalLayout_24.addWidget(self.lineEdit_11)
        self.verticalLayout_9.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_17.addWidget(self.label_13)
        self.doctor = QtWidgets.QComboBox(self.tab_2)
        self.show_doc()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doctor.sizePolicy().hasHeightForWidth())
        self.doctor.setSizePolicy(sizePolicy)
        self.doctor.setMinimumSize(QtCore.QSize(450, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.doctor.setFont(font)
        self.doctor.setObjectName("doctor")
        self.horizontalLayout_17.addWidget(self.doctor)
        self.verticalLayout_9.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_16.addWidget(self.label_14)
        self.adddoctor = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adddoctor.sizePolicy().hasHeightForWidth())
        self.adddoctor.setSizePolicy(sizePolicy)
        self.adddoctor.setMinimumSize(QtCore.QSize(450, 0))
        self.adddoctor.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.adddoctor.setFont(font)
        self.adddoctor.setObjectName("adddoctor")
        self.horizontalLayout_16.addWidget(self.adddoctor)
        self.verticalLayout_9.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        """spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem2)
        self.ok = QtWidgets.QPushButton(self.tab_2)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        #########################################################
        self.ok.setFont(font)
        self.ok.setObjectName("ok")
        self.ok.clicked.connect(self.show_bill)
        self.horizontalLayout_14.addWidget(self.ok)
        self.adddoctor_2 = QtWidgets.QPushButton(self.tab_2)
        self.adddoctor_2.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.adddoctor_2.setFont(font)
        self.adddoctor_2.setObjectName("adddoctor_2")
        self.horizontalLayout_14.addWidget(self.adddoctor_2)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem3)"""
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem)
        """self.comboBox_7 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.horizontalLayout_14.addWidget(self.comboBox_7)
        self.save = QtWidgets.QPushButton(self.tab_2)
        self.save.clicked.connect(self.save_bill)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.save.setFont(font)
        self.save.setObjectName("save")
        self.horizontalLayout_14.addWidget(self.save)
        self.print_2 = QtWidgets.QPushButton(self.tab_2)
        self.print_2.setMinimumSize(QtCore.QSize(0, 0))
        self.print_2.clicked.connect(self.show_pdf)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.print_2.setFont(font)
        self.print_2.setObjectName("print_2")
        self.horizontalLayout_15.addWidget(self.print_2)
        self.verticalLayout_9.addLayout(self.horizontalLayout_15)
        self.gridLayout_4.addLayout(self.verticalLayout_9, 0, 0, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tableWidget_2)
        #**********************************************************
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_2)
        self.horizontalLayout_14.addWidget(self.print_2)
        self.ok = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.ok.setFont(font)
        self.ok.setObjectName("ok")
        self.horizontalLayout_14.addWidget(self.ok)"""
        self.adddoctor_2 = QtWidgets.QPushButton(self.tab_2)
        self.adddoctor_2.setMinimumSize(QtCore.QSize(0, 0))

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.adddoctor_2.setFont(font)
        self.adddoctor_2.setObjectName("adddoctor_2")
        self.adddoctor_2.clicked.connect(self.add_doctor)
        self.horizontalLayout_14.addWidget(self.adddoctor_2)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        self.verticalLayout_3.addLayout(self.verticalLayout_9)
        self.line_32 = QtWidgets.QFrame(self.tab_2)
        self.line_32.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.verticalLayout_3.addWidget(self.line_32)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_22.addWidget(self.label_15)
        self.pname = QtWidgets.QComboBox(self.tab_2)
        self.show_to_search()
        self.pname.activated.connect(self.show_to_select)
        shortcut1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Return"), self.pname)
        shortcut1.activated.connect(self.add_to_bill)

        #self.pname.activated.connect(self.show_batch)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pname.sizePolicy().hasHeightForWidth())
        self.pname.setSizePolicy(sizePolicy)
        self.pname.setMinimumSize(QtCore.QSize(400, 0))
        self.pname.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.pname.setFont(font)
        self.pname.setObjectName("pname")
        self.horizontalLayout_22.addWidget(self.pname)
        self.verticalLayout_3.addLayout(self.horizontalLayout_22)
        self.line_31 = QtWidgets.QFrame(self.tab_2)
        self.line_31.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.verticalLayout_3.addWidget(self.line_31)
        self.tableWidget_11 = QtWidgets.QTableWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_11.sizePolicy().hasHeightForWidth())
        self.tableWidget_11.setSizePolicy(sizePolicy)
        self.tableWidget_11.setObjectName("tableWidget_11")
        self.tableWidget_11.setColumnCount(0)
        self.tableWidget_11.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_11)
        self.line_29 = QtWidgets.QFrame(self.tab_2)
        self.line_29.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.verticalLayout_3.addWidget(self.line_29)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.line_30 = QtWidgets.QFrame(self.tab_2)
        self.line_30.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.verticalLayout_3.addWidget(self.line_30)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.comboBox_7 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.horizontalLayout_23.addWidget(self.comboBox_7)
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_23.addWidget(self.label_21)
        self.Odiscount = QtWidgets.QSpinBox(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.Odiscount.setFont(font)
        self.Odiscount.setObjectName("Odiscount")
        self.horizontalLayout_23.addWidget(self.Odiscount)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem1)
        self.save = QtWidgets.QPushButton(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.save.setFont(font)
        self.save.setObjectName("save")
        self.save.clicked.connect(self.save_bill)

        self.horizontalLayout_23.addWidget(self.save)
        self.print_2 = QtWidgets.QPushButton(self.tab_2)
        self.print_2.setMinimumSize(QtCore.QSize(0, 0))
        self.print_2.clicked.connect(self.show_pdf)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.print_2.setFont(font)
        self.print_2.setObjectName("print_2")
        self.horizontalLayout_23.addWidget(self.print_2)
        self.delete_3 = QtWidgets.QPushButton(self.tab_2)
        self.delete_3.setMinimumSize(QtCore.QSize(75, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.delete_3.setFont(font)
        self.delete_3.setObjectName("delete_3")
        self.horizontalLayout_23.addWidget(self.delete_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_19.addLayout(self.verticalLayout_3)
        self.line_33 = QtWidgets.QFrame(self.tab_2)
        self.line_33.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.horizontalLayout_19.addWidget(self.line_33)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.textBrowser.setFont(font)
        self.textBrowser.setPlaceholderText("")
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_19.addWidget(self.textBrowser)
        self.gridLayout_4.addLayout(self.horizontalLayout_19, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tableWidget_12 = QtWidgets.QTableWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_12.sizePolicy().hasHeightForWidth())
        self.tableWidget_12.setSizePolicy(sizePolicy)
        self.tableWidget_12.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget_12.setObjectName("tableWidget_12")
        self.tableWidget_12.setColumnCount(0)
        self.tableWidget_12.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tableWidget_12)
        self.gridLayout_3.addLayout(self.verticalLayout_5, 2, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_3.sizePolicy().hasHeightForWidth())
        self.tableWidget_3.setSizePolicy(sizePolicy)
        self.tableWidget_3.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)

        self.tableWidget_3.setFont(font)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.horizontalLayout_29.addWidget(self.tableWidget_3)

        shortcut2 = QtWidgets.QShortcut(QtGui.QKeySequence("Insert"), self.tableWidget_12)
        shortcut2.activated.connect(self.add_to_purcahse)

        self.line_34 = QtWidgets.QFrame(self.tab_3)
        self.line_34.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.horizontalLayout_29.addWidget(self.line_34)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.show_batch()
        #self.show_mrp()
        """self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_19.addWidget(self.label_18)
        self.quantity_2 = QtWidgets.QComboBox(self.tab_2)
        # self.quantity_2.activated.connect(self.show_mrp)
        self.show_batch()
        self.show_mrp()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)"""
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_2.sizePolicy().hasHeightForWidth())
        self.textBrowser_2.setSizePolicy(sizePolicy)
        self.textBrowser_2.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_29.addWidget(self.textBrowser_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_29)
        self.line_35 = QtWidgets.QFrame(self.tab_3)
        self.line_35.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_35.setObjectName("line_35")
        self.verticalLayout_2.addWidget(self.line_35)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_28.addItem(spacerItem2)

        self.editinpurchase = QtWidgets.QPushButton(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.editinpurchase.setFont(font)
        self.editinpurchase.setObjectName("editinpurchase")
        self.horizontalLayout_28.addWidget(self.editinpurchase)
        self.showpurchase = QtWidgets.QPushButton(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.showpurchase.setFont(font)
        self.showpurchase.setObjectName("showpurchase")
        self.horizontalLayout_28.addWidget(self.showpurchase)
        self.deletefrompurchase = QtWidgets.QPushButton(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.deletefrompurchase.setFont(font)
        self.deletefrompurchase.setObjectName("deletefrompurchase")
        self.horizontalLayout_28.addWidget(self.deletefrompurchase)
        self.deletefrompurchase.clicked.connect(self.delete_from_purchase)
        self.savepurchase = QtWidgets.QPushButton(self.tab_3)
        self.delete_3.clicked.connect(self.delete_from_bill)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.savepurchase.setFont(font)
        self.savepurchase.setObjectName("savepurchase")
        self.horizontalLayout_28.addWidget(self.savepurchase)
        self.savepurchase.clicked.connect(self.save_purchase)

        self.cancel = QtWidgets.QPushButton(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.cancel.clicked.connect(self.cancel_purchase)

        self.horizontalLayout_28.addWidget(self.cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_28)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 4, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.tab_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_3.addWidget(self.line_2, 1, 0, 1, 1)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_26 = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_30.addWidget(self.label_26)
        self.dealer_2 = QtWidgets.QComboBox(self.tab_3)
        self.show_dealer()
        self.dealer_2.activated.connect(self.show_to_select_dealer)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dealer_2.sizePolicy().hasHeightForWidth())
        self.dealer_2.setSizePolicy(sizePolicy)
        self.dealer_2.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealer_2.setFont(font)
        self.dealer_2.setObjectName("dealer_2")
        self.horizontalLayout_30.addWidget(self.dealer_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_30)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_27 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_25.addWidget(self.label_27)
        self.invoicedate = QtWidgets.QDateEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.invoicedate.sizePolicy().hasHeightForWidth())
        self.invoicedate.setSizePolicy(sizePolicy)
        self.invoicedate.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.invoicedate.setFont(font)
        self.invoicedate.setObjectName("invoicedate")
        self.horizontalLayout_25.addWidget(self.invoicedate)
        self.verticalLayout_4.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_25 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_21.addWidget(self.label_25)
        self.invoiceno = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.invoiceno.sizePolicy().hasHeightForWidth())
        self.invoiceno.setSizePolicy(sizePolicy)
        self.invoiceno.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.invoiceno.setFont(font)
        self.invoiceno.setObjectName("invoiceno")
        #self.invoiceno.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.invoiceno.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9 ]*")))
        self.horizontalLayout_21.addWidget(self.invoiceno)
        self.verticalLayout_4.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_28 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_20.addWidget(self.label_28)
        self.paymentmode = QtWidgets.QComboBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paymentmode.sizePolicy().hasHeightForWidth())
        self.paymentmode.setSizePolicy(sizePolicy)
        self.paymentmode.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.paymentmode.setFont(font)
        self.paymentmode.setObjectName("paymentmode")
        self.paymentmode.addItem("")
        self.paymentmode.addItem("")
        self.horizontalLayout_20.addWidget(self.paymentmode)
        self.verticalLayout_4.addLayout(self.horizontalLayout_20)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem3)
        self.line_37 = QtWidgets.QFrame(self.tab_3)
        self.line_37.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_37.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_37.setObjectName("line_37")
        self.verticalLayout_4.addWidget(self.line_37)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_29 = QtWidgets.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_26.addWidget(self.label_29)
        self.product = QtWidgets.QComboBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product.sizePolicy().hasHeightForWidth())
        self.product.setSizePolicy(sizePolicy)
        self.product.setMinimumSize(QtCore.QSize(400, 0))
        self.product.activated.connect(self.show_to_select_product)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.product.setFont(font)
        self.product.setObjectName("product")
        ######################################################################################################yaaa
        self.horizontalLayout_26.addWidget(self.product)
        self.verticalLayout_4.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27.addLayout(self.verticalLayout_4)
        self.line_36 = QtWidgets.QFrame(self.tab_3)
        self.line_36.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_36.setObjectName("line_36")
        self.horizontalLayout_27.addWidget(self.line_36)
        self.tableWidget_13 = QtWidgets.QTableWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_13.sizePolicy().hasHeightForWidth())
        self.tableWidget_13.setSizePolicy(sizePolicy)
        self.tableWidget_13.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget_13.setObjectName("tableWidget_13")
        self.tableWidget_13.setColumnCount(0)
        self.tableWidget_13.setRowCount(0)
        shortcut0 = QtWidgets.QShortcut(QtGui.QKeySequence("Enter"), self.tableWidget_13)
        shortcut0.activated.connect(self.select_dealer)
        self.horizontalLayout_27.addWidget(self.tableWidget_13)
        self.gridLayout_3.addLayout(self.horizontalLayout_27, 0, 0, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.tab_3)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_3.addWidget(self.line_10, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_4)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.today = QtWidgets.QRadioButton(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.today.setFont(font)
        self.today.setObjectName("today")
        self.today.setChecked(True)
        self.horizontalLayout_38.addWidget(self.today)

        self.line_9 = QtWidgets.QFrame(self.tab_6)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout_38.addWidget(self.line_9)

        self.previous = QtWidgets.QRadioButton(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.previous.setFont(font)
        self.previous.setObjectName("previous")
        self.horizontalLayout_38.addWidget(self.previous)

        self.line_6 = QtWidgets.QFrame(self.tab_6)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_38.addWidget(self.line_6)

        self.label_61 = QtWidgets.QLabel(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_61.setFont(font)
        self.label_61.setObjectName("label_61")
        self.horizontalLayout_38.addWidget(self.label_61)
        self.from_ = QtWidgets.QDateEdit(self.tab_6)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.from_.setFont(font)
        self.from_.setObjectName("from_")
        self.horizontalLayout_38.addWidget(self.from_)
        self.label_62 = QtWidgets.QLabel(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_62.sizePolicy().hasHeightForWidth())
        self.label_62.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_62.setFont(font)
        self.label_62.setObjectName("label_62")
        self.horizontalLayout_38.addWidget(self.label_62)
        self.to = QtWidgets.QDateEdit(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.to.setFont(font)
        self.to.setObjectName("to")
        self.horizontalLayout_38.addWidget(self.to)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_38.addItem(spacerItem4)
        self.verticalLayout_16.addLayout(self.horizontalLayout_38)
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")

        self.showbutton = QtWidgets.QPushButton(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.showbutton.clicked.connect(self.calculate_report)
        self.showbutton.setFont(font)
        self.showbutton.setObjectName("showbutton")
        self.horizontalLayout_44.addWidget(self.showbutton)

        self.printbutton = QtWidgets.QPushButton(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.printbutton.setFont(font)
        self.printbutton.setObjectName("printbutton")
        self.printbutton.clicked.connect(self.day_book_xlsx)
        self.horizontalLayout_44.addWidget(self.printbutton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_44.addItem(spacerItem5)
        self.verticalLayout_16.addLayout(self.horizontalLayout_44)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.line_7 = QtWidgets.QFrame(self.tab_6)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_12.addWidget(self.line_7)
        self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_6)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget_4.setFont(font)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.verticalLayout_12.addWidget(self.tableWidget_4)


        self.line_8 = QtWidgets.QFrame(self.tab_6)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_12.addWidget(self.line_8)
        self.total = QtWidgets.QTextBrowser(self.tab_6)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total.sizePolicy().hasHeightForWidth())
        self.total.setSizePolicy(sizePolicy)
        self.total.setMinimumSize(QtCore.QSize(300, 0))

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.total.setFont(font)
        self.total.setObjectName("total")
        self.verticalLayout_12.addWidget(self.total)
        self.verticalLayout_16.addLayout(self.verticalLayout_12)
        self.gridLayout_7.addLayout(self.verticalLayout_16, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_9)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        self.today_4 = QtWidgets.QRadioButton(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.today_4.setFont(font)
        self.today_4.setObjectName("today_4")
        self.horizontalLayout_52.addWidget(self.today_4)
        self.line_14 = QtWidgets.QFrame(self.tab_9)
        self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.horizontalLayout_52.addWidget(self.line_14)
        self.previous_4 = QtWidgets.QRadioButton(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.previous_4.setFont(font)
        self.previous_4.setObjectName("previous_4")
        self.horizontalLayout_52.addWidget(self.previous_4)
        self.line_13 = QtWidgets.QFrame(self.tab_9)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.horizontalLayout_52.addWidget(self.line_13)
        self.label_73 = QtWidgets.QLabel(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_73.setFont(font)
        self.label_73.setObjectName("label_73")
        self.horizontalLayout_52.addWidget(self.label_73)
        self.from_4 = QtWidgets.QDateEdit(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.from_4.setFont(font)
        self.from_4.setObjectName("from_4")
        self.horizontalLayout_52.addWidget(self.from_4)
        self.label_74 = QtWidgets.QLabel(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_74.setFont(font)
        self.label_74.setObjectName("label_74")
        self.horizontalLayout_52.addWidget(self.label_74)
        self.to_4 = QtWidgets.QDateEdit(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.to_4.setFont(font)
        self.to_4.setObjectName("to_4")
        self.horizontalLayout_52.addWidget(self.to_4)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_52.addItem(spacerItem6)
        self.verticalLayout_19.addLayout(self.horizontalLayout_52)
        self.horizontalLayout_53 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.showbutton_4 = QtWidgets.QPushButton(self.tab_9)
        #self.searchkey_2 = QtWidgets.QLineEdit(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.showbutton_4.setFont(font)
        self.showbutton_4.setObjectName("showbutton_4")
        self.showbutton_4.clicked.connect(self.calculate_report)
        self.horizontalLayout_53.addWidget(self.showbutton_4)
        self.printbutton_4 = QtWidgets.QPushButton(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.printbutton_4.setFont(font)
        self.printbutton_4.setObjectName("printbutton_4")
        self.printbutton_4.clicked.connect(self.sale_book_xlsx)
        self.horizontalLayout_53.addWidget(self.printbutton_4)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_53.addItem(spacerItem7)
        self.verticalLayout_19.addLayout(self.horizontalLayout_53)
        self.line_15 = QtWidgets.QFrame(self.tab_9)
        self.line_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.verticalLayout_19.addWidget(self.line_15)
        self.tableWidget_7 = QtWidgets.QTableWidget(self.tab_9)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget_7.setFont(font)
        self.tableWidget_7.setObjectName("tableWidget_7")
        self.tableWidget_7.setColumnCount(0)
        self.tableWidget_7.setRowCount(0)
        self.verticalLayout_19.addWidget(self.tableWidget_7)
        self.line_16 = QtWidgets.QFrame(self.tab_9)
        self.line_16.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.verticalLayout_19.addWidget(self.line_16)
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        self.total_4 = QtWidgets.QTextBrowser(self.tab_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_4.sizePolicy().hasHeightForWidth())
        self.total_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.total_4.setFont(font)
        self.total_4.setObjectName("total_4")
        self.horizontalLayout_54.addWidget(self.total_4)
        self.verticalLayout_19.addLayout(self.horizontalLayout_54)
        self.gridLayout_10.addLayout(self.verticalLayout_19, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_9, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_8)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.today_3 = QtWidgets.QRadioButton(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.today_3.setFont(font)
        self.today_3.setObjectName("today_3")
        self.today_3.setChecked(True)
        self.horizontalLayout_49.addWidget(self.today_3)

        self.line_19 = QtWidgets.QFrame(self.tab_8)
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.horizontalLayout_49.addWidget(self.line_19)

        self.previous_3 = QtWidgets.QRadioButton(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.previous_3.setFont(font)
        self.previous_3.setObjectName("previous_3")
        self.horizontalLayout_49.addWidget(self.previous_3)
        self.line_11 = QtWidgets.QFrame(self.tab_8)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.horizontalLayout_49.addWidget(self.line_11)
        self.label_69 = QtWidgets.QLabel(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_69.setFont(font)
        self.label_69.setObjectName("label_69")
        self.horizontalLayout_49.addWidget(self.label_69)
        self.from_3 = QtWidgets.QDateEdit(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.from_3.setFont(font)
        self.from_3.setObjectName("from_3")
        self.horizontalLayout_49.addWidget(self.from_3)
        self.label_70 = QtWidgets.QLabel(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_70.setFont(font)
        self.label_70.setObjectName("label_70")
        self.horizontalLayout_49.addWidget(self.label_70)
        self.to_3 = QtWidgets.QDateEdit(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.to_3.setFont(font)
        self.to_3.setObjectName("to_3")
        self.horizontalLayout_49.addWidget(self.to_3)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_49.addItem(spacerItem8)
        self.verticalLayout_18.addLayout(self.horizontalLayout_49)
        self.horizontalLayout_50 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_50.setObjectName("horizontalLayout_50")
        self.showbutton_3 = QtWidgets.QPushButton(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.showbutton_3.setFont(font)
        self.showbutton_3.setObjectName("showbutton_3")
        self.showbutton_3.clicked.connect(self.calculate_report)

        self.horizontalLayout_50.addWidget(self.showbutton_3)

        self.printbutton_3 = QtWidgets.QPushButton(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.printbutton_3.setFont(font)
        self.printbutton_3.setObjectName("printbutton_3")
        self.printbutton_3.clicked.connect(self.purchase_book_xlsx)
        self.horizontalLayout_50.addWidget(self.printbutton_3)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_50.addItem(spacerItem9)
        self.verticalLayout_18.addLayout(self.horizontalLayout_50)
        self.line_18 = QtWidgets.QFrame(self.tab_8)
        self.line_18.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.verticalLayout_18.addWidget(self.line_18)
        self.tableWidget_6 = QtWidgets.QTableWidget(self.tab_8)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget_6.setFont(font)
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(0)
        self.tableWidget_6.setRowCount(0)
        self.verticalLayout_18.addWidget(self.tableWidget_6)
        self.line_17 = QtWidgets.QFrame(self.tab_8)
        self.line_17.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.verticalLayout_18.addWidget(self.line_17)
        self.horizontalLayout_51 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_51.setObjectName("horizontalLayout_51")

        self.total_3 = QtWidgets.QTextBrowser(self.tab_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_3.sizePolicy().hasHeightForWidth())
        self.total_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.total_3.setFont(font)
        self.total_3.setObjectName("total_3")
        self.horizontalLayout_51.addWidget(self.total_3)
        self.verticalLayout_18.addLayout(self.horizontalLayout_51)
        self.gridLayout_9.addLayout(self.verticalLayout_18, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.today_2 = QtWidgets.QRadioButton(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.today_2.setFont(font)
        self.today_2.setObjectName("today_2")
        self.horizontalLayout_46.addWidget(self.today_2)
        self.line_20 = QtWidgets.QFrame(self.tab_7)
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.horizontalLayout_46.addWidget(self.line_20)
        self.previous_2 = QtWidgets.QRadioButton(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.previous_2.setFont(font)
        self.previous_2.setObjectName("previous_2")
        self.horizontalLayout_46.addWidget(self.previous_2)
        self.line_12 = QtWidgets.QFrame(self.tab_7)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.horizontalLayout_46.addWidget(self.line_12)
        self.label_65 = QtWidgets.QLabel(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_65.setFont(font)
        self.label_65.setObjectName("label_65")
        self.horizontalLayout_46.addWidget(self.label_65)
        self.from_2 = QtWidgets.QDateEdit(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.from_2.setFont(font)
        self.from_2.setObjectName("from_2")
        self.horizontalLayout_46.addWidget(self.from_2)
        self.label_66 = QtWidgets.QLabel(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_66.setFont(font)
        self.label_66.setObjectName("label_66")
        self.horizontalLayout_46.addWidget(self.label_66)
        self.to_2 = QtWidgets.QDateEdit(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.to_2.setFont(font)
        self.to_2.setObjectName("to_2")
        self.horizontalLayout_46.addWidget(self.to_2)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_46.addItem(spacerItem10)
        self.verticalLayout_17.addLayout(self.horizontalLayout_46)
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.showbutton_2 = QtWidgets.QPushButton(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)

        self.showbutton_2.setFont(font)
        self.showbutton_2.setObjectName("showbutton_2")
        self.horizontalLayout_47.addWidget(self.showbutton_2)
        self.showbutton_2.clicked.connect(self.calculate_report)
        self.printbutton_2 = QtWidgets.QPushButton(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)

        self.printbutton_2.setFont(font)
        self.printbutton_2.setObjectName("printbutton_2")
        self.printbutton_2.clicked.connect(self.tax_book_xlsx)
        self.horizontalLayout_47.addWidget(self.printbutton_2)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_47.addItem(spacerItem11)
        self.verticalLayout_17.addLayout(self.horizontalLayout_47)
        self.line_22 = QtWidgets.QFrame(self.tab_7)
        self.line_22.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.verticalLayout_17.addWidget(self.line_22)
        self.tableWidget_5 = QtWidgets.QTableWidget(self.tab_7)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.tableWidget_5.setFont(font)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(0)
        self.tableWidget_5.setRowCount(0)
        self.verticalLayout_17.addWidget(self.tableWidget_5)
        self.line_21 = QtWidgets.QFrame(self.tab_7)
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.verticalLayout_17.addWidget(self.line_21)
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.total_2 = QtWidgets.QTextBrowser(self.tab_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy.setHeightForWidth(self.total_2.sizePolicy().hasHeightForWidth())
        self.total_2.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.total_2.setFont(font)
        self.total_2.setObjectName("total_2")
        self.horizontalLayout_48.addWidget(self.total_2)
        self.printgstreport = QtWidgets.QPushButton(self.tab_7)
        self.printgstreport.setObjectName("printgstreport")
        self.printgstreport.clicked.connect(self.txtgst)
        self.horizontalLayout_48.addWidget(self.printgstreport)
        self.verticalLayout_17.addLayout(self.horizontalLayout_48)
        self.gridLayout_8.addLayout(self.verticalLayout_17, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_7, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tab_11)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.tab_11)

        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_12 = QtWidgets.QWidget()
        self.tab_12.setObjectName("tab_12")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_12)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout()
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.horizontalLayout_56 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_56.setObjectName("horizontalLayout_56")
        self.label_47 = QtWidgets.QLabel(self.tab_12)
        self.label_47.setObjectName("label_47")
        self.horizontalLayout_56.addWidget(self.label_47)
        self.party = QtWidgets.QComboBox(self.tab_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.party.sizePolicy().hasHeightForWidth())
        self.party.setSizePolicy(sizePolicy)
        self.party.setObjectName("party")
        self.horizontalLayout_56.addWidget(self.party)
        self.label_17 = QtWidgets.QLabel(self.tab_12)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_56.addWidget(self.label_17)
        self.line_26 = QtWidgets.QFrame(self.tab_12)
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.horizontalLayout_56.addWidget(self.line_26)
        self.contact = QtWidgets.QComboBox(self.tab_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contact.sizePolicy().hasHeightForWidth())
        self.contact.setSizePolicy(sizePolicy)
        self.contact.setObjectName("contact")
        self.horizontalLayout_56.addWidget(self.contact)
        self.today_6 = QtWidgets.QRadioButton(self.tab_12)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.today_6.setFont(font)
        self.today_6.setObjectName("today_6")
        self.horizontalLayout_56.addWidget(self.today_6)
        self.line_27 = QtWidgets.QFrame(self.tab_12)
        self.line_27.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.horizontalLayout_56.addWidget(self.line_27)
        self.previous_6 = QtWidgets.QRadioButton(self.tab_12)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.previous_6.setFont(font)
        self.previous_6.setObjectName("previous_6")
        self.horizontalLayout_56.addWidget(self.previous_6)
        self.line_28 = QtWidgets.QFrame(self.tab_12)
        self.line_28.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.horizontalLayout_56.addWidget(self.line_28)
        self.label_71 = QtWidgets.QLabel(self.tab_12)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_71.setFont(font)
        self.label_71.setObjectName("label_71")
        self.horizontalLayout_56.addWidget(self.label_71)
        self.from_6 = QtWidgets.QDateEdit(self.tab_12)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.from_6.setFont(font)
        self.from_6.setObjectName("from_6")
        self.horizontalLayout_56.addWidget(self.from_6)
        self.label_75 = QtWidgets.QLabel(self.tab_12)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_75.setFont(font)
        self.label_75.setObjectName("label_75")
        self.horizontalLayout_56.addWidget(self.label_75)
        self.to_6 = QtWidgets.QDateEdit(self.tab_12)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.to_6.setFont(font)
        self.to_6.setObjectName("to_6")
        self.horizontalLayout_56.addWidget(self.to_6)
        self.verticalLayout_23.addLayout(self.horizontalLayout_56)
        self.horizontalLayout_57 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")
        self.showledger_2 = QtWidgets.QPushButton(self.tab_12)
        self.showledger_2.setObjectName("showledger_2")
        self.showledger_2.clicked.connect(self.show_sale_ledger)
        self.horizontalLayout_57.addWidget(self.showledger_2)
        self.updateledger_2 = QtWidgets.QPushButton(self.tab_12)
        self.updateledger_2.setObjectName("updateledger_2")
        self.updateledger_2.clicked.connect(self.update_sale_ledger)
        self.horizontalLayout_57.addWidget(self.updateledger_2)
        self.allledger_2 = QtWidgets.QPushButton(self.tab_12)
        self.allledger_2.setObjectName("allledger_2")
        self.allledger_2.clicked.connect(self.show_all_sale_ledger)
        self.horizontalLayout_57.addWidget(self.allledger_2)
        self.printledger_2 = QtWidgets.QPushButton(self.tab_12)
        self.printledger_2.setObjectName("printledger_2")
        self.printledger_2.clicked.connect(self.sale_ledger_xlsx)
        self.horizontalLayout_57.addWidget(self.printledger_2)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_57.addItem(spacerItem12)
        self.verticalLayout_23.addLayout(self.horizontalLayout_57)
        self.verticalLayout_22.addLayout(self.verticalLayout_23)
        self.line_63 = QtWidgets.QFrame(self.tab_12)
        self.line_63.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_63.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_63.setObjectName("line_63")
        self.verticalLayout_22.addWidget(self.line_63)
        self.tableWidget_10 = QtWidgets.QTableWidget(self.tab_12)
        self.tableWidget_10.setObjectName("tableWidget_10")
        self.tableWidget_10.setColumnCount(0)
        self.tableWidget_10.setRowCount(0)
        self.verticalLayout_22.addWidget(self.tableWidget_10)
        self.horizontalLayout_45.addLayout(self.verticalLayout_22)
        self.line_62 = QtWidgets.QFrame(self.tab_12)
        self.line_62.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_62.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_62.setObjectName("line_62")
        self.horizontalLayout_45.addWidget(self.line_62)
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_4.sizePolicy().hasHeightForWidth())
        self.textBrowser_4.setSizePolicy(sizePolicy)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.horizontalLayout_45.addWidget(self.textBrowser_4)
        self.gridLayout_13.addLayout(self.horizontalLayout_45, 0, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_12, "")
        self.tab_13 = QtWidgets.QWidget()
        self.tab_13.setObjectName("tab_13")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tab_13)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.horizontalLayout_41 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_41.setObjectName("horizontalLayout_41")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")

        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")

        self.horizontalLayout_40 = QtWidgets.QHBoxLayout()

        self.horizontalLayout_40.setObjectName("horizontalLayout_40")
        self.label_39 = QtWidgets.QLabel(self.tab_13)
        self.label_39.setObjectName("label_39")
        self.horizontalLayout_40.addWidget(self.label_39)
        self.deaer = QtWidgets.QComboBox(self.tab_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deaer.sizePolicy().hasHeightForWidth())
        self.deaer.setSizePolicy(sizePolicy)
        self.deaer.setObjectName("deaer")
        self.horizontalLayout_40.addWidget(self.deaer)
        self.label_16 = QtWidgets.QLabel(self.tab_13)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_40.addWidget(self.label_16)
        self.address = QtWidgets.QComboBox(self.tab_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.address.sizePolicy().hasHeightForWidth())
        self.address.setSizePolicy(sizePolicy)
        self.address.setObjectName("address")
        self.horizontalLayout_40.addWidget(self.address)
        self.line_25 = QtWidgets.QFrame(self.tab_13)
        self.line_25.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.horizontalLayout_40.addWidget(self.line_25)
        self.today_5 = QtWidgets.QRadioButton(self.tab_13)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.today_5.setFont(font)
        self.today_5.setObjectName("today_5")
        self.horizontalLayout_40.addWidget(self.today_5)
        self.line_23 = QtWidgets.QFrame(self.tab_13)
        self.line_23.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.horizontalLayout_40.addWidget(self.line_23)
        self.previous_5 = QtWidgets.QRadioButton(self.tab_13)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.previous_5.setFont(font)
        self.previous_5.setObjectName("previous_5")
        self.horizontalLayout_40.addWidget(self.previous_5)
        self.line_24 = QtWidgets.QFrame(self.tab_13)
        self.line_24.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.horizontalLayout_40.addWidget(self.line_24)
        self.label_67 = QtWidgets.QLabel(self.tab_13)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_67.setFont(font)
        self.label_67.setObjectName("label_67")
        self.horizontalLayout_40.addWidget(self.label_67)
        self.from_5 = QtWidgets.QDateEdit(self.tab_13)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.from_5.setFont(font)
        self.from_5.setObjectName("from_5")
        self.horizontalLayout_40.addWidget(self.from_5)
        self.label_68 = QtWidgets.QLabel(self.tab_13)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_68.setFont(font)
        self.label_68.setObjectName("label_68")
        self.horizontalLayout_40.addWidget(self.label_68)
        self.to_5 = QtWidgets.QDateEdit(self.tab_13)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.to_5.setFont(font)
        self.to_5.setObjectName("to_5")
        self.horizontalLayout_40.addWidget(self.to_5)
        self.verticalLayout_20.addLayout(self.horizontalLayout_40)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.showledger = QtWidgets.QPushButton(self.tab_13)
        self.showledger.setObjectName("showledger")
        self.showledger.clicked.connect(self.show_purchase_ledger)
        self.horizontalLayout_15.addWidget(self.showledger)
        self.updateledger = QtWidgets.QPushButton(self.tab_13)
        self.updateledger.setObjectName("updateledger")
        self.updateledger.clicked.connect(self.update_purchase_ledger)
        self.horizontalLayout_15.addWidget(self.updateledger)
        self.allledger = QtWidgets.QPushButton(self.tab_13)
        self.allledger.setObjectName("allledger")
        self.allledger.clicked.connect(self.show_all_purchase_ledger)
        self.horizontalLayout_15.addWidget(self.allledger)
        self.printledger = QtWidgets.QPushButton(self.tab_13)

        self.printledger.setAutoDefault(True)
        self.allledger.setAutoDefault(True)
        self.updateledger.setAutoDefault(True)
        self.showledger.setAutoDefault(True)
        self.printledger_2.setAutoDefault(True)
        self.allledger_2.setAutoDefault(True)
        self.updateledger_2.setAutoDefault(True)
        self.showledger_2.setAutoDefault(True)
        self.printbutton_2.setAutoDefault(True)
        self.showbutton_2.setAutoDefault(True)
        self.printbutton_3.setAutoDefault(True)
        self.showbutton_3.setAutoDefault(True)
        self.printbutton_4.setAutoDefault(True)
        self.showbutton_4.setAutoDefault(True)
        self.printbutton.setAutoDefault(True)
        self.showbutton.setAutoDefault(True)
        self.cancel.setAutoDefault(True)
        self.savepurchase.setAutoDefault(True)
        self.deletefrompurchase.setAutoDefault(True)
        self.showpurchase.setAutoDefault(True)
        self.editinpurchase.setAutoDefault(True)
        self.delete_3.setAutoDefault(True)
        self.print_2.setAutoDefault(True)
        self.save.setAutoDefault(True)
        self.adddoctor_2.setAutoDefault(True)
        self.addproduct.setAutoDefault(True)
        self.print.setAutoDefault(True)
        self.delete_2.setAutoDefault(True)
        self.edit.setAutoDefault(True)
        self.Search.setAutoDefault(True)
        self.pushButton_3.setAutoDefault(True)


        self.printledger.setObjectName("printledger")
        self.printledger.clicked.connect(self.purchase_ledger_xlsx)
        self.horizontalLayout_15.addWidget(self.printledger)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem13)
        self.verticalLayout_20.addLayout(self.horizontalLayout_15)
        self.verticalLayout_21.addLayout(self.verticalLayout_20)
        self.line_39 = QtWidgets.QFrame(self.tab_13)
        self.line_39.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_39.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_39.setObjectName("line_39")
        self.verticalLayout_21.addWidget(self.line_39)
        self.tableWidget_8 = QtWidgets.QTableWidget(self.tab_13)
        self.tableWidget_8.setObjectName("tableWidget_8")
        self.tableWidget_8.setColumnCount(0)
        self.tableWidget_8.setRowCount(0)
        self.verticalLayout_21.addWidget(self.tableWidget_8)
        self.horizontalLayout_41.addLayout(self.verticalLayout_21)
        self.line_38 = QtWidgets.QFrame(self.tab_13)
        self.line_38.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_38.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_38.setObjectName("line_38")
        self.horizontalLayout_41.addWidget(self.line_38)
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_3.sizePolicy().hasHeightForWidth())
        self.textBrowser_3.setSizePolicy(sizePolicy)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.horizontalLayout_41.addWidget(self.textBrowser_3)
        self.gridLayout_12.addLayout(self.horizontalLayout_41, 0, 0, 1, 1)
        self.tabWidget_3.addTab(self.tab_13, "")
        self.gridLayout_11.addWidget(self.tabWidget_3, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_11, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.tabWidget_2.addTab(self.tab_10, "")
        self.gridLayout_6.addWidget(self.tabWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        ####################################################
        self.tab_14 = QtWidgets.QWidget()
        self.tab_14.setObjectName("tab_14")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.tab_14)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.tabWidget_4 = QtWidgets.QTabWidget(self.tab_14)
        self.tabWidget_4.setObjectName("tabWidget_4")
        self.tab_15 = QtWidgets.QWidget()
        self.tab_15.setObjectName("tab_15")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tab_15)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_19 = QtWidgets.QLabel(self.tab_15)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_31.addWidget(self.label_19)
        self.Invoiceno = QtWidgets.QComboBox(self.tab_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Invoiceno.sizePolicy().hasHeightForWidth())
        self.Invoiceno.setSizePolicy(sizePolicy)
        self.Invoiceno.setObjectName("Invoiceno")
        self.horizontalLayout_31.addWidget(self.Invoiceno)
        self.line_52 = QtWidgets.QFrame(self.tab_15)
        self.line_52.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_52.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_52.setObjectName("line_52")
        self.horizontalLayout_31.addWidget(self.line_52)
        self.party_2 = QtWidgets.QLabel(self.tab_15)
        self.party_2.setObjectName("party_2")
        self.horizontalLayout_31.addWidget(self.party_2)
        self.line_58 = QtWidgets.QFrame(self.tab_15)
        self.line_58.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_58.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_58.setObjectName("line_58")
        self.horizontalLayout_31.addWidget(self.line_58)
        self.label_20 = QtWidgets.QLabel(self.tab_15)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_31.addWidget(self.label_20)
        self.invoicedate_2 = QtWidgets.QDateEdit(self.tab_15)
        self.invoicedate_2.setObjectName("invoicedate_2")
        self.horizontalLayout_31.addWidget(self.invoicedate_2)
        self.line_65 = QtWidgets.QFrame(self.tab_15)
        self.line_65.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_65.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_65.setObjectName("line_65")
        self.horizontalLayout_31.addWidget(self.line_65)
        self.modify = QtWidgets.QPushButton(self.tab_15)
        self.modify.setAutoDefault(True)
        self.modify.setFlat(False)
        self.modify.setObjectName("modify")
        self.modify.clicked.connect(self.show_to_modify_sale)

        self.horizontalLayout_31.addWidget(self.modify)
        self.line_53 = QtWidgets.QFrame(self.tab_15)
        self.line_53.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_53.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_53.setObjectName("line_53")
        self.horizontalLayout_31.addWidget(self.line_53)
        self.label_18 = QtWidgets.QLabel(self.tab_15)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_31.addWidget(self.label_18)
        self.product_2 = QtWidgets.QComboBox(self.tab_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_2.sizePolicy().hasHeightForWidth())
        self.product_2.setSizePolicy(sizePolicy)
        self.product_2.setObjectName("product_2")
        self.product_2.currentTextChanged.connect(self.show_to_select_product_modify_sale)

        self.horizontalLayout_31.addWidget(self.product_2)
        self.line_54 = QtWidgets.QFrame(self.tab_15)
        self.line_54.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_54.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_54.setObjectName("line_54")
        self.horizontalLayout_31.addWidget(self.line_54)
        self.add = QtWidgets.QPushButton(self.tab_15)
        self.add.setObjectName("add")
        self.add.clicked.connect(self.add_to_modify_sale)
        self.horizontalLayout_31.addWidget(self.add)
        self.edit_2 = QtWidgets.QPushButton(self.tab_15)
        self.edit_2.setObjectName("edit_2")
        self.horizontalLayout_31.addWidget(self.edit_2)
        self.delete_5 = QtWidgets.QPushButton(self.tab_15)
        self.delete_5.setObjectName("delete_5")
        self.horizontalLayout_31.addWidget(self.delete_5)
        self.delete_5.clicked.connect(self.delete_modify_sale)

        self.gridLayout_15.addLayout(self.horizontalLayout_31, 0, 0, 1, 1)
        self.line_57 = QtWidgets.QFrame(self.tab_15)
        self.line_57.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_57.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_57.setObjectName("line_57")
        self.gridLayout_15.addWidget(self.line_57, 7, 0, 1, 1)
        self.line_55 = QtWidgets.QFrame(self.tab_15)
        self.line_55.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_55.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_55.setObjectName("line_55")
        self.gridLayout_15.addWidget(self.line_55, 1, 0, 1, 1)
        self.tableWidget_14 = QtWidgets.QTableWidget(self.tab_15)
        self.tableWidget_14.setObjectName("tableWidget_14")
        self.tableWidget_14.setColumnCount(0)
        self.tableWidget_14.setRowCount(0)
        self.gridLayout_15.addWidget(self.tableWidget_14, 4, 0, 1, 1)
        self.horizontalLayout_58 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_58.setObjectName("horizontalLayout_58")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_58.addItem(spacerItem14)
        self.label_31 = QtWidgets.QLabel(self.tab_15)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_58.addWidget(self.label_31)
        self.discount = QtWidgets.QSpinBox(self.tab_15)
        self.discount.setObjectName("discount")
        self.horizontalLayout_58.addWidget(self.discount)
        self.save_2 = QtWidgets.QPushButton(self.tab_15)
        self.save_2.setObjectName("save_2")
        self.save_2.clicked.connect(self.save_print_modify_sale)

        self.horizontalLayout_58.addWidget(self.save_2)
        self.print_3 = QtWidgets.QPushButton(self.tab_15)
        self.print_3.setObjectName("print_3")
        self.horizontalLayout_58.addWidget(self.print_3)
        self.cancel_2 = QtWidgets.QPushButton(self.tab_15)
        self.cancel_2.setObjectName("cancel_2")
        self.horizontalLayout_58.addWidget(self.cancel_2)
        self.gridLayout_15.addLayout(self.horizontalLayout_58, 8, 0, 1, 1)
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.tab_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_5.sizePolicy().hasHeightForWidth())
        self.textBrowser_5.setSizePolicy(sizePolicy)
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.gridLayout_15.addWidget(self.textBrowser_5, 6, 0, 1, 1)
        self.line_56 = QtWidgets.QFrame(self.tab_15)
        self.line_56.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_56.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_56.setObjectName("line_56")
        self.gridLayout_15.addWidget(self.line_56, 3, 0, 1, 1)
        self.tableWidget_15 = QtWidgets.QTableWidget(self.tab_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_15.sizePolicy().hasHeightForWidth())
        self.tableWidget_15.setSizePolicy(sizePolicy)
        self.tableWidget_15.setObjectName("tableWidget_15")
        self.tableWidget_15.setColumnCount(0)
        self.tableWidget_15.setRowCount(0)
        self.gridLayout_15.addWidget(self.tableWidget_15, 2, 0, 1, 1)
        self.line_61 = QtWidgets.QFrame(self.tab_15)
        self.line_61.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_61.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_61.setObjectName("line_61")
        self.gridLayout_15.addWidget(self.line_61, 5, 0, 1, 1)
        self.tabWidget_4.addTab(self.tab_15, "")
        self.tab_16 = QtWidgets.QWidget()
        self.tab_16.setObjectName("tab_16")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.tab_16)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.tab_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_6.sizePolicy().hasHeightForWidth())
        self.textBrowser_6.setSizePolicy(sizePolicy)
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.gridLayout_16.addWidget(self.textBrowser_6, 6, 0, 1, 1)
        self.tableWidget_17 = QtWidgets.QTableWidget(self.tab_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_17.sizePolicy().hasHeightForWidth())
        self.tableWidget_17.setSizePolicy(sizePolicy)
        self.tableWidget_17.setObjectName("tableWidget_17")
        self.tableWidget_17.setColumnCount(0)
        self.tableWidget_17.setRowCount(0)
        self.gridLayout_16.addWidget(self.tableWidget_17, 2, 0, 1, 1)
        self.line_47 = QtWidgets.QFrame(self.tab_16)
        self.line_47.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_47.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_47.setObjectName("line_47")
        self.gridLayout_16.addWidget(self.line_47, 7, 0, 1, 1)
        self.horizontalLayout_60 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_60.setObjectName("horizontalLayout_60")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_60.addItem(spacerItem15)
        self.save_3 = QtWidgets.QPushButton(self.tab_16)
        self.save_3.setAutoDefault(True)
        self.save_3.setObjectName("save_3")
        self.horizontalLayout_60.addWidget(self.save_3)
        self.save_3.clicked.connect(self.save_print_modify_pur)


        self.cancel_3 = QtWidgets.QPushButton(self.tab_16)
        self.cancel_3.setAutoDefault(True)
        self.cancel_3.setObjectName("cancel_3")
        self.horizontalLayout_60.addWidget(self.cancel_3)
        self.gridLayout_16.addLayout(self.horizontalLayout_60, 8, 0, 1, 1)
        self.horizontalLayout_59 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_59.setObjectName("horizontalLayout_59")
        self.label_22 = QtWidgets.QLabel(self.tab_16)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_59.addWidget(self.label_22)
        self.invoiceno_2 = QtWidgets.QComboBox(self.tab_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.invoiceno_2.sizePolicy().hasHeightForWidth())
        self.invoiceno_2.setSizePolicy(sizePolicy)
        self.invoiceno_2.setObjectName("invoiceno_2")
        self.horizontalLayout_59.addWidget(self.invoiceno_2)
        self.line_59 = QtWidgets.QFrame(self.tab_16)
        self.line_59.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_59.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_59.setObjectName("line_59")
        self.horizontalLayout_59.addWidget(self.line_59)
        self.Party = QtWidgets.QLabel(self.tab_16)
        self.Party.setObjectName("Party")
        self.horizontalLayout_59.addWidget(self.Party)
        self.line_51 = QtWidgets.QFrame(self.tab_16)
        self.line_51.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_51.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_51.setObjectName("line_51")
        self.horizontalLayout_59.addWidget(self.line_51)
        self.label_23 = QtWidgets.QLabel(self.tab_16)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_59.addWidget(self.label_23)
        self.invoicedate_3 = QtWidgets.QDateEdit(self.tab_16)
        self.invoicedate_3.setObjectName("invoicedate_3")
        self.horizontalLayout_59.addWidget(self.invoicedate_3)
        self.line_64 = QtWidgets.QFrame(self.tab_16)
        self.line_64.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_64.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_64.setObjectName("line_64")
        self.horizontalLayout_59.addWidget(self.line_64)
        self.Modify = QtWidgets.QPushButton(self.tab_16)
        self.Modify.setObjectName("Modify")
        self.Modify.clicked.connect(self.show_to_modify_pur)
        self.horizontalLayout_59.addWidget(self.Modify)
        self.line_46 = QtWidgets.QFrame(self.tab_16)
        self.line_46.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_46.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_46.setObjectName("line_46")
        self.horizontalLayout_59.addWidget(self.line_46)
        self.label_30 = QtWidgets.QLabel(self.tab_16)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_59.addWidget(self.label_30)
        self.product_3 = QtWidgets.QComboBox(self.tab_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_3.sizePolicy().hasHeightForWidth())
        self.product_3.setSizePolicy(sizePolicy)
        self.product_3.setObjectName("product_3")
        self.product_3.activated.connect(self.show_to_select_product_modify_pur)
        self.horizontalLayout_59.addWidget(self.product_3)
        self.line_50 = QtWidgets.QFrame(self.tab_16)
        self.line_50.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_50.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_50.setObjectName("line_50")
        self.horizontalLayout_59.addWidget(self.line_50)
        self.add_2 = QtWidgets.QPushButton(self.tab_16)
        self.add_2.setObjectName("add_2")
        self.horizontalLayout_59.addWidget(self.add_2)
        self.add_2.clicked.connect(self.add_to_modify_pur)

        self.edit_3 = QtWidgets.QPushButton(self.tab_16)
        self.edit_3.setObjectName("edit_3")
        self.horizontalLayout_59.addWidget(self.edit_3)
        self.delete_6 = QtWidgets.QPushButton(self.tab_16)
        self.delete_6.setObjectName("delete_6")
        self.delete_6.clicked.connect(self.delete_modify_pur)

        self.horizontalLayout_59.addWidget(self.delete_6)
        self.gridLayout_16.addLayout(self.horizontalLayout_59, 0, 0, 1, 1)
        self.line_49 = QtWidgets.QFrame(self.tab_16)
        self.line_49.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_49.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_49.setObjectName("line_49")
        self.gridLayout_16.addWidget(self.line_49, 1, 0, 1, 1)
        self.line_48 = QtWidgets.QFrame(self.tab_16)
        self.line_48.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_48.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_48.setObjectName("line_48")
        self.gridLayout_16.addWidget(self.line_48, 3, 0, 1, 1)
        self.tableWidget_16 = QtWidgets.QTableWidget(self.tab_16)
        self.tableWidget_16.setObjectName("tableWidget_16")
        self.tableWidget_16.setColumnCount(0)
        self.tableWidget_16.setRowCount(0)
        self.gridLayout_16.addWidget(self.tableWidget_16, 4, 0, 1, 1)
        self.line_60 = QtWidgets.QFrame(self.tab_16)
        self.line_60.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_60.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_60.setObjectName("line_60")
        self.gridLayout_16.addWidget(self.line_60, 5, 0, 1, 1)
        self.tabWidget_4.addTab(self.tab_16, "")
        self.gridLayout_14.addWidget(self.tabWidget_4, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_14, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()

        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.line_4 = QtWidgets.QFrame(self.tab_5)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_13.addWidget(self.line_4)
        self.label_57 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_57.setFont(font)
        self.label_57.setAlignment(QtCore.Qt.AlignCenter)
        self.label_57.setObjectName("label_57")
        self.verticalLayout_13.addWidget(self.label_57)
        self.horizontalLayout_42 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_42.setObjectName("horizontalLayout_42")
        self.label_59 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_59.setFont(font)
        self.label_59.setObjectName("label_59")
        self.horizontalLayout_42.addWidget(self.label_59)
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setObjectName("comboBox_3")
        self.horizontalLayout_42.addWidget(self.comboBox_3)
        self.search = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.search.setFont(font)
        self.search.setObjectName("search")
        self.search.clicked.connect(self.search_bill)
        self.horizontalLayout_42.addWidget(self.search)
        self.verticalLayout_13.addLayout(self.horizontalLayout_42)
        self.verticalLayout_15.addLayout(self.verticalLayout_13)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.line_45 = QtWidgets.QFrame(self.tab_5)
        self.line_45.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_45.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_45.setObjectName("line_45")
        self.verticalLayout_14.addWidget(self.line_45)
        self.label_58 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_58.setFont(font)
        self.label_58.setAlignment(QtCore.Qt.AlignCenter)
        self.label_58.setObjectName("label_58")
        self.verticalLayout_14.addWidget(self.label_58)
        self.textEdit = QtWidgets.QTextEdit(self.tab_5)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_14.addWidget(self.textEdit)
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_43.addItem(spacerItem16)
        self.delete_4 = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.delete_4.setFont(font)
        self.delete_4.setObjectName("delete_4")
        self.delete_4.clicked.connect(self.send)

        self.horizontalLayout_43.addWidget(self.delete_4)
        self.verticalLayout_14.addLayout(self.horizontalLayout_43)
        """self.tableWidget_9 = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_9.setObjectName("tableWidget_9")
        self.tableWidget_9.setColumnCount(0)
        self.tableWidget_9.setRowCount(0)
        self.verticalLayout_14.addWidget(self.tableWidget_9)"""
        self.verticalLayout_15.addLayout(self.verticalLayout_14)
        self.gridLayout_5.addLayout(self.verticalLayout_15, 1, 3, 1, 1)

        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.line = QtWidgets.QFrame(self.tab_5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_8.addWidget(self.line)
        self.label_52 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_52.setFont(font)
        self.label_52.setAlignment(QtCore.Qt.AlignCenter)
        self.label_52.setObjectName("label_52")
        self.verticalLayout_8.addWidget(self.label_52)
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.label_40 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.horizontalLayout_33.addWidget(self.label_40)
        self.dealer_3 = QtWidgets.QLineEdit(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealer_3.setFont(font)
        self.dealer_3.setObjectName("dealer_3")
        self.dealer_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout_33.addWidget(self.dealer_3)
        self.label_43 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_43.setFont(font)
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_33.addWidget(self.label_43)
        self.dealercontact = QtWidgets.QLineEdit(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealercontact.setFont(font)
        self.dealercontact.setObjectName("dealercontact")
        self.dealercontact.setValidator(QtGui.QIntValidator())
        self.horizontalLayout_33.addWidget(self.dealercontact)
        self.label_42 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_42.setFont(font)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_33.addWidget(self.label_42)
        self.dealergst = QtWidgets.QLineEdit(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealergst.setFont(font)
        self.dealergst.setObjectName("dealergst")
        self.dealergst.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout_33.addWidget(self.dealergst)
        self.verticalLayout_8.addLayout(self.horizontalLayout_33)
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_41 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_41.setFont(font)
        self.label_41.setObjectName("label_41")
        self.horizontalLayout_32.addWidget(self.label_41)
        self.dealeraddress = QtWidgets.QLineEdit(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealeraddress.setFont(font)
        self.dealeraddress.setObjectName("dealeraddress")
        self.dealeraddress.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout_32.addWidget(self.dealeraddress)
        self.savedealer = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.savedealer.setFont(font)
        self.savedealer.setObjectName("savedealer")
        self.savedealer.clicked.connect(self.add_dealer)

        self.horizontalLayout_32.addWidget(self.savedealer)
        self.editdealer = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.editdealer.setFont(font)
        self.editdealer.setObjectName("editdealer")
        self.editdealer.clicked.connect(self.edit_dealer)
        self.horizontalLayout_32.addWidget(self.editdealer)
        self.dealerdelete = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.dealerdelete.setFont(font)
        self.dealerdelete.setObjectName("dealerdelete")
        self.dealerdelete.clicked.connect(self.delete_dealer)
        self.horizontalLayout_32.addWidget(self.dealerdelete)
        self.verticalLayout_8.addLayout(self.horizontalLayout_32)
        self.dealertable = QtWidgets.QTableWidget(self.tab_5)
        font = QtGui.QFont()

        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)

        self.dealertable.setFont(font)
        self.dealertable.setObjectName("dealertable")
        self.dealertable.setColumnCount(0)
        self.dealertable.setRowCount(0)
        self.verticalLayout_8.addWidget(self.dealertable)
        self.gridLayout_5.addLayout(self.verticalLayout_8, 1, 0, 1, 2)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()

        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_55 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_55.setFont(font)
        self.label_55.setAlignment(QtCore.Qt.AlignCenter)
        self.label_55.setObjectName("label_55")
        self.verticalLayout_11.addWidget(self.label_55)
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.label_45 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_45.setFont(font)
        self.label_45.setObjectName("label_45")
        self.horizontalLayout_36.addWidget(self.label_45)
        self.comboBox_5 = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_5.sizePolicy().hasHeightForWidth())
        self.comboBox_5.setSizePolicy(sizePolicy)
        self.comboBox_5.setObjectName("comboBox_5")
        self.horizontalLayout_36.addWidget(self.comboBox_5)
        self.verticalLayout_11.addLayout(self.horizontalLayout_36)
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.verticalLayout_11.addLayout(self.horizontalLayout_39)
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_37.addWidget(self.pushButton_2)
        self.deletecontact = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.deletecontact.setFont(font)
        self.deletecontact.setObjectName("deletecontact")
        self.deletecontact.clicked.connect(self.search_customer)
        self.horizontalLayout_37.addWidget(self.deletecontact)
        self.verticalLayout_11.addLayout(self.horizontalLayout_37)
        self.customertable = QtWidgets.QTableWidget(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.customertable.setFont(font)
        self.customertable.setObjectName("customertable")
        self.customertable.setColumnCount(0)
        self.customertable.setRowCount(0)
        self.verticalLayout_11.addWidget(self.customertable)
        self.gridLayout_5.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_54 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_54.setFont(font)
        self.label_54.setAlignment(QtCore.Qt.AlignCenter)
        self.label_54.setObjectName("label_54")
        self.verticalLayout_10.addWidget(self.label_54)
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.label_44 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.label_44.setFont(font)
        self.label_44.setObjectName("label_44")
        self.horizontalLayout_34.addWidget(self.label_44)
        self.companyentry = QtWidgets.QLineEdit(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.companyentry.setFont(font)
        self.companyentry.setObjectName("companyentry")
        self.companyentry.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9 ]*")))
        self.horizontalLayout_34.addWidget(self.companyentry)
        self.verticalLayout_10.addLayout(self.horizontalLayout_34)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.savecomany = QtWidgets.QPushButton(self.tab_5)
        self.savecomany.clicked.connect(self.add_company)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.savecomany.setFont(font)
        self.savecomany.setObjectName("savecomany")
        self.horizontalLayout_35.addWidget(self.savecomany)
        self.editcompany = QtWidgets.QPushButton(self.tab_5)
        self.editcompany.clicked.connect(self.edit_company)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.editcompany.setFont(font)
        self.editcompany.setObjectName("editcompany")
        self.horizontalLayout_35.addWidget(self.editcompany)
        self.deletecompany = QtWidgets.QPushButton(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.deletecompany.setFont(font)
        self.deletecompany.clicked.connect(self.delete_company)
        self.deletecompany.setObjectName("deletecompany")
        self.horizontalLayout_35.addWidget(self.deletecompany)
        self.verticalLayout_10.addLayout(self.horizontalLayout_35)
        self.companytable = QtWidgets.QTableWidget(self.tab_5)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(62)
        self.companytable.setFont(font)
        self.companytable.setObjectName("companytable")
        self.companytable.setColumnCount(0)
        self.companytable.setRowCount(0)
        self.verticalLayout_10.addWidget(self.companytable)
        self.gridLayout_5.addLayout(self.verticalLayout_10, 0, 3, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.tab_5)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_5.addWidget(self.line_5, 1, 2, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.tab_5)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_5.addWidget(self.line_3, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.show_other()
        self.today_2.setChecked(True)
        self.today_3.setChecked(True)
        self.today_4.setChecked(True)
        self.today_5.setChecked(True)
        self.today_6.setChecked(True)
        self.to.setDate(QDate.currentDate())
        self.to_2.setDate(QDate.currentDate())
        self.to_3.setDate(QDate.currentDate())
        self.to_4.setDate(QDate.currentDate())
        self.to_5.setDate(QDate.currentDate())
        self.to_6.setDate(QDate.currentDate())
        self.invoicedate_2.setDate(QDate.currentDate())
        self.invoicedate_3.setDate(QDate.currentDate())
        self.invoicedate.setDate(QDate.currentDate())
        self.show_to_select()
        self.show_stock()
        self.show_to_select_dealer()
        self.show_to_search_purchase()
        self.show_to_select_product_modify_sale()
        self.show_to_select_product_modify_pur()



        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.name, self.batch)
        MainWindow.setTabOrder(self.batch, self.mrp)
        MainWindow.setTabOrder(self.mrp, self.exp)
        MainWindow.setTabOrder(self.exp, self.quantity)
        MainWindow.setTabOrder(self.quantity, self.hsn)
        MainWindow.setTabOrder(self.hsn, self.rate)
        MainWindow.setTabOrder(self.rate, self.gst)
        MainWindow.setTabOrder(self.gst, self.dealer)
        MainWindow.setTabOrder(self.dealer, self.company)
        MainWindow.setTabOrder(self.company, self.addproduct)
        MainWindow.setTabOrder(self.addproduct, self.print)
        MainWindow.setTabOrder(self.print, self.delete_2)
        MainWindow.setTabOrder(self.delete_2, self.edit)
        MainWindow.setTabOrder(self.edit, self.Search)
        MainWindow.setTabOrder(self.Search, self.summery)
        MainWindow.setTabOrder(self.summery, self.shrtdate)
        MainWindow.setTabOrder(self.shrtdate, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.companywise)
        MainWindow.setTabOrder(self.companywise, self.dealerwise)
        MainWindow.setTabOrder(self.dealerwise, self.productwise)
        MainWindow.setTabOrder(self.productwise, self.shortlist)
        MainWindow.setTabOrder(self.shortlist, self.showall)
        MainWindow.setTabOrder(self.showall, self.tableWidget)
        MainWindow.setTabOrder(self.tableWidget, self.patientname)
        MainWindow.setTabOrder(self.patientname, self.lineEdit_11)
        MainWindow.setTabOrder(self.lineEdit_11, self.doctor)
        MainWindow.setTabOrder(self.doctor, self.pname)
        MainWindow.setTabOrder(self.pname, self.tableWidget_11)
        MainWindow.setTabOrder(self.tableWidget_11, self.adddoctor)

        MainWindow.setTabOrder(self.adddoctor, self.Odiscount)
        MainWindow.setTabOrder(self.Odiscount, self.delete_3)
        MainWindow.setTabOrder(self.delete_3, self.dealer_2)
        MainWindow.setTabOrder(self.dealer_2, self.tableWidget_13)
        MainWindow.setTabOrder(self.tableWidget_13, self.invoicedate)
        MainWindow.setTabOrder(self.invoicedate, self.invoiceno)
        MainWindow.setTabOrder(self.invoiceno, self.paymentmode)
        MainWindow.setTabOrder(self.paymentmode, self.product)
        MainWindow.setTabOrder(self.product, self.tableWidget_12)
        MainWindow.setTabOrder(self.tableWidget_12, self.savepurchase)
        MainWindow.setTabOrder(self.savepurchase, self.cancel)
        MainWindow.setTabOrder(self.cancel, self.tabWidget_2)
        MainWindow.setTabOrder(self.tabWidget_2, self.today)
        MainWindow.setTabOrder(self.today, self.previous)
        MainWindow.setTabOrder(self.previous, self.from_)
        MainWindow.setTabOrder(self.from_, self.to)
        MainWindow.setTabOrder(self.to, self.showbutton)
        MainWindow.setTabOrder(self.showbutton, self.printbutton)
        MainWindow.setTabOrder(self.printbutton, self.tableWidget_4)
        MainWindow.setTabOrder(self.tableWidget_4, self.total)
        MainWindow.setTabOrder(self.total, self.today_2)
        MainWindow.setTabOrder(self.today_2, self.previous_2)
        MainWindow.setTabOrder(self.previous_2, self.from_2)
        MainWindow.setTabOrder(self.from_2, self.to_2)
        MainWindow.setTabOrder(self.to_2, self.showbutton_2)
        MainWindow.setTabOrder(self.showbutton_2, self.printbutton_2)
        MainWindow.setTabOrder(self.printbutton_2, self.tableWidget_5)
        MainWindow.setTabOrder(self.tableWidget_5, self.total_2)
        MainWindow.setTabOrder(self.total_2, self.today_3)
        MainWindow.setTabOrder(self.today_3, self.previous_3)
        MainWindow.setTabOrder(self.previous_3, self.from_3)
        MainWindow.setTabOrder(self.from_3, self.to_3)
        MainWindow.setTabOrder(self.to_3, self.showbutton_3)
        MainWindow.setTabOrder(self.showbutton_3, self.printbutton_3)
        MainWindow.setTabOrder(self.printbutton_3, self.tableWidget_6)
        MainWindow.setTabOrder(self.tableWidget_6, self.total_3)
        MainWindow.setTabOrder(self.total_3, self.today_4)
        MainWindow.setTabOrder(self.today_4, self.previous_4)
        MainWindow.setTabOrder(self.previous_4, self.from_4)
        MainWindow.setTabOrder(self.from_4, self.to_4)
        MainWindow.setTabOrder(self.to_4, self.showbutton_4)
        MainWindow.setTabOrder(self.showbutton_4, self.printbutton_4)
        MainWindow.setTabOrder(self.printbutton_4, self.tableWidget_7)
        MainWindow.setTabOrder(self.tableWidget_7, self.total_4)
        MainWindow.setTabOrder(self.total_4, self.companyentry)
        MainWindow.setTabOrder(self.companyentry, self.savecomany)
        MainWindow.setTabOrder(self.savecomany, self.editcompany)
        MainWindow.setTabOrder(self.editcompany, self.deletecompany)
        MainWindow.setTabOrder(self.deletecompany, self.companytable)
        MainWindow.setTabOrder(self.companytable, self.deletecontact)
        MainWindow.setTabOrder(self.deletecontact, self.customertable)
        MainWindow.setTabOrder(self.customertable, self.dealer_3)
        MainWindow.setTabOrder(self.dealer_3, self.dealercontact)
        MainWindow.setTabOrder(self.dealercontact, self.dealergst)
        MainWindow.setTabOrder(self.dealergst, self.dealeraddress)
        MainWindow.setTabOrder(self.dealeraddress, self.savedealer)
        MainWindow.setTabOrder(self.savedealer, self.editdealer)
        MainWindow.setTabOrder(self.editdealer, self.dealerdelete)
        MainWindow.setTabOrder(self.dealerdelete, self.dealertable)
        MainWindow.setTabOrder(self.dealertable, self.search)
        MainWindow.setTabOrder(self.search, self.delete_4)
        MainWindow.setTabOrder(self.delete_4, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.radioButton)
        MainWindow.setTabOrder(self.radioButton, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.adddoctor_2)
        MainWindow.setTabOrder(self.adddoctor_2, self.tableWidget_2)
        MainWindow.setTabOrder(self.tableWidget_2, self.comboBox_7)
        MainWindow.setTabOrder(self.comboBox_7, self.save)
        MainWindow.setTabOrder(self.save, self.print_2)
        MainWindow.setTabOrder(self.print_2, self.textBrowser)
        MainWindow.setTabOrder(self.textBrowser, self.textBrowser_2)
        MainWindow.setTabOrder(self.textBrowser_2, self.editinpurchase)
        MainWindow.setTabOrder(self.editinpurchase, self.showpurchase)
        MainWindow.setTabOrder(self.showpurchase, self.deletefrompurchase)
        MainWindow.setTabOrder(self.deletefrompurchase, self.tableWidget_3)
        MainWindow.setTabOrder(self.tableWidget_3, self.printgstreport)
        MainWindow.setTabOrder(self.printgstreport, self.tabWidget_3)
        MainWindow.setTabOrder(self.tabWidget_3, self.party)
        MainWindow.setTabOrder(self.party, self.contact)
        MainWindow.setTabOrder(self.contact, self.today_6)
        MainWindow.setTabOrder(self.today_6, self.previous_6)
        MainWindow.setTabOrder(self.previous_6, self.from_6)
        MainWindow.setTabOrder(self.from_6, self.to_6)
        MainWindow.setTabOrder(self.to_6, self.showledger_2)
        MainWindow.setTabOrder(self.showledger_2, self.updateledger_2)
        MainWindow.setTabOrder(self.updateledger_2, self.allledger_2)
        MainWindow.setTabOrder(self.allledger_2, self.printledger_2)
        MainWindow.setTabOrder(self.printledger_2, self.tableWidget_10)
        MainWindow.setTabOrder(self.tableWidget_10, self.textBrowser_4)
        MainWindow.setTabOrder(self.textBrowser_4, self.deaer)
        MainWindow.setTabOrder(self.deaer, self.address)
        MainWindow.setTabOrder(self.address, self.today_5)
        MainWindow.setTabOrder(self.today_5, self.previous_5)
        MainWindow.setTabOrder(self.previous_5, self.from_5)
        MainWindow.setTabOrder(self.from_5, self.to_5)
        MainWindow.setTabOrder(self.to_5, self.showledger)
        MainWindow.setTabOrder(self.showledger, self.updateledger)
        MainWindow.setTabOrder(self.updateledger, self.allledger)
        MainWindow.setTabOrder(self.allledger, self.printledger)
        MainWindow.setTabOrder(self.printledger, self.tableWidget_8)
        MainWindow.setTabOrder(self.tableWidget_8, self.textBrowser_3)
        MainWindow.setTabOrder(self.textBrowser_3, self.tabWidget_4)
        MainWindow.setTabOrder(self.tabWidget_4, self.Invoiceno)
        MainWindow.setTabOrder(self.Invoiceno, self.invoicedate_2)
        MainWindow.setTabOrder(self.invoicedate_2, self.modify)
        MainWindow.setTabOrder(self.modify, self.product_2)
        MainWindow.setTabOrder(self.product_2, self.tableWidget_15)
        MainWindow.setTabOrder(self.tableWidget_15, self.edit_2)
        MainWindow.setTabOrder(self.edit_2, self.delete_5)
        MainWindow.setTabOrder(self.delete_5, self.tableWidget_14)
        MainWindow.setTabOrder(self.tableWidget_14, self.discount)
        MainWindow.setTabOrder(self.discount, self.save_2)
        MainWindow.setTabOrder(self.save_2, self.print_3)
        MainWindow.setTabOrder(self.print_3, self.cancel_2)
        MainWindow.setTabOrder(self.cancel_2, self.textBrowser_5)
        MainWindow.setTabOrder(self.textBrowser_5, self.add)
        MainWindow.setTabOrder(self.add, self.textBrowser_6)
        MainWindow.setTabOrder(self.textBrowser_6, self.add_2)
        MainWindow.setTabOrder(self.add_2, self.save_3)
        MainWindow.setTabOrder(self.save_3, self.cancel_3)
        MainWindow.setTabOrder(self.cancel_3, self.invoiceno_2)
        MainWindow.setTabOrder(self.invoiceno_2, self.invoicedate_3)
        MainWindow.setTabOrder(self.invoicedate_3, self.Modify)
        MainWindow.setTabOrder(self.Modify, self.product_3)
        MainWindow.setTabOrder(self.product_3, self.tableWidget_17)
        MainWindow.setTabOrder(self.tableWidget_17, self.edit_3)
        MainWindow.setTabOrder(self.edit_3, self.delete_6)
        MainWindow.setTabOrder(self.delete_6, self.tableWidget_16)
        MainWindow.setTabOrder(self.tableWidget_16, self.comboBox_3)
        MainWindow.setTabOrder(self.comboBox_3, self.comboBox_5)
        MainWindow.setTabOrder(self.comboBox_5, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.textEdit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smooothware Solutions - Maa Tara Ayurved"))
        self.label.setText(_translate("MainWindow", "Name"))
        self.name.setPlaceholderText(_translate("MainWindow", "Enter name of the product"))
        self.label_2.setText(_translate("MainWindow", "Batch No."))
        self.batch.setPlaceholderText(_translate("MainWindow", "Enter Batch of the product"))
        self.label_3.setText(_translate("MainWindow", "MRP"))
        self.label_4.setText(_translate("MainWindow", "Expiry Date"))
        self.exp.setDisplayFormat(_translate("MainWindow", "yyyy--MM"))
        self.from_.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.to.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.from_2.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.to_2.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.from_3.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.to_3.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.from_4.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.to_4.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.from_5.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.to_5.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.from_6.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.to_6.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))

        self.label_5.setText(_translate("MainWindow", "Quantity"))
        self.label_6.setText(_translate("MainWindow", "HSN Code"))
        self.hsn.setPlaceholderText(_translate("MainWindow", "Enter HSN Code"))
        self.label_7.setText(_translate("MainWindow", "Rate"))
        self.label_8.setText(_translate("MainWindow", "GST"))
        self.label_10.setText(_translate("MainWindow", "Dealer"))

        self.label_11.setText(_translate("MainWindow", "Company"))
        self.label_77.setText(_translate("MainWindow", "Rack No."))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter Rack No."))
        self.label_9.setText(_translate("MainWindow", "Search"))
        self.companywise.setText(_translate("MainWindow", "Comany Wise"))
        self.dealerwise.setText(_translate("MainWindow", "Dealer Wise"))
        self.productwise.setText(_translate("MainWindow", "Product Wise"))
        self.shrtdate.setText(_translate("MainWindow", "Short Date"))
        self.shortlist.setText(_translate("MainWindow", "Short List"))
        self.showall.setText(_translate("MainWindow", "Show All"))
        self.radioButton.setText(_translate("MainWindow", "Expired"))
        self.pushButton_3.setText(_translate("MainWindow", "Duplicate"))
        self.Search.setText(_translate("MainWindow", "Search"))
        self.edit.setText(_translate("MainWindow", "Edit"))
        self.delete_2.setText(_translate("MainWindow", "Delete"))
        self.print.setText(_translate("MainWindow", "Print"))
        self.addproduct.setText(_translate("MainWindow", "Add Product"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Stock"))
        self.label_12.setText(_translate("MainWindow", "Patient\'s Name : "))
        self.patientname.setPlaceholderText(_translate("MainWindow", "Enter Patient name "))
        self.label_24.setText(_translate("MainWindow", "Customer Contact No : "))
        self.lineEdit_11.setPlaceholderText(_translate("MainWindow", "Enter Customer contact no."))
        self.label_13.setText(_translate("MainWindow", "Doctor : Dr."))
        self.label_14.setText(_translate("MainWindow", "Add Doctor : "))
        self.adddoctor.setPlaceholderText(_translate("MainWindow", "Enter Doctor name to add"))
        self.adddoctor_2.setText(_translate("MainWindow", "Add Doctor"))
        self.label_15.setText(_translate("MainWindow", "Search"))
        self.comboBox_7.setItemText(0, _translate("MainWindow", "Cash"))
        self.comboBox_7.setItemText(1, _translate("MainWindow", "Credit"))
        self.label_21.setText(_translate("MainWindow", "Overall Discount"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.print_2.setText(_translate("MainWindow", "Print"))

        self.delete_3.setText(_translate("MainWindow", "Delete"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Sale"))

        self.editinpurchase.setText(_translate("MainWindow", "Edit"))
        self.showpurchase.setText(_translate("MainWindow", "Show"))
        self.deletefrompurchase.setText(_translate("MainWindow", "Delete"))
        self.savepurchase.setText(_translate("MainWindow", "Save"))
        self.cancel.setText(_translate("MainWindow", "Cancel"))
        self.label_26.setText(_translate("MainWindow", "Dealer"))
        self.label_27.setText(_translate("MainWindow", "Invoice Date"))
        self.label_25.setText(_translate("MainWindow", "Invoice No."))
        self.invoiceno.setPlaceholderText(_translate("MainWindow", "Enter Invoice no."))
        self.label_28.setText(_translate("MainWindow", "Mode of Payment"))
        self.paymentmode.setItemText(0, _translate("MainWindow", "Cash"))
        self.paymentmode.setItemText(1, _translate("MainWindow", "Credit"))
        self.label_29.setText(_translate("MainWindow", "Product"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Purchase"))
        self.today.setText(_translate("MainWindow", "Today"))
        self.previous.setText(_translate("MainWindow", "Previous"))
        self.label_61.setText(_translate("MainWindow", "From"))
        self.label_62.setText(_translate("MainWindow", "To"))
        self.showbutton.setText(_translate("MainWindow", "Show"))

        self.printbutton.setText(_translate("MainWindow", "Print"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "DayBook"))
        self.today_4.setText(_translate("MainWindow", "Today"))
        self.previous_4.setText(_translate("MainWindow", "Previous"))
        self.label_73.setText(_translate("MainWindow", "From"))
        self.label_74.setText(_translate("MainWindow", "To"))
        self.showbutton_4.setText(_translate("MainWindow", "Show"))
        self.printbutton_4.setText(_translate("MainWindow", "Print"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), _translate("MainWindow", "Sales Reaport "))

        self.today_3.setText(_translate("MainWindow", "Today"))
        self.previous_3.setText(_translate("MainWindow", "Previous"))
        self.label_69.setText(_translate("MainWindow", "From"))
        self.label_70.setText(_translate("MainWindow", "To"))


        self.showbutton_3.setText(_translate("MainWindow", "Show"))

        self.printbutton_3.setText(_translate("MainWindow", "Print"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), _translate("MainWindow", "Purchase Report"))
        self.today_2.setText(_translate("MainWindow", "Today"))
        self.previous_2.setText(_translate("MainWindow", "Previous"))
        self.label_65.setText(_translate("MainWindow", "From"))
        self.label_66.setText(_translate("MainWindow", "To"))
        self.showbutton_2.setText(_translate("MainWindow", "Show"))
        self.printbutton_2.setText(_translate("MainWindow", "Print"))
        self.printgstreport.setText(_translate("MainWindow", "Print Report"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("MainWindow", "Tax Summery"))
        self.label_47.setText(_translate("MainWindow", "Party"))
        self.label_17.setText(_translate("MainWindow", "Contact"))
        self.today_6.setText(_translate("MainWindow", "Today"))
        self.previous_6.setText(_translate("MainWindow", "Previous"))
        self.label_71.setText(_translate("MainWindow", "From"))
        self.label_75.setText(_translate("MainWindow", "To"))
        self.showledger_2.setText(_translate("MainWindow", "Show"))
        self.updateledger_2.setText(_translate("MainWindow", "Update"))
        self.allledger_2.setText(_translate("MainWindow", "Show All"))
        self.printledger_2.setText(_translate("MainWindow", "Print"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_12), _translate("MainWindow", "Sales Ledger"))
        self.label_39.setText(_translate("MainWindow", "Dealer"))
        self.label_16.setText(_translate("MainWindow", "Address"))
        self.today_5.setText(_translate("MainWindow", "Today"))
        self.previous_5.setText(_translate("MainWindow", "Previous"))
        self.label_67.setText(_translate("MainWindow", "From"))
        self.label_68.setText(_translate("MainWindow", "To"))
        self.showledger.setText(_translate("MainWindow", "Show"))
        self.updateledger.setText(_translate("MainWindow", "Update"))
        self.allledger.setText(_translate("MainWindow", "Show All"))
        self.printledger.setText(_translate("MainWindow", "Print"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_13), _translate("MainWindow", "Purchase Ledger"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_11), _translate("MainWindow", "Ledger"))


        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_10), _translate("MainWindow", "GST"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Reports"))
        self.label_19.setText(_translate("MainWindow", "Invoice ID"))
        self.party_2.setText(_translate("MainWindow", "Party"))
        self.label_20.setText(_translate("MainWindow", "Invoice Date"))
        self.invoicedate_2.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.modify.setText(_translate("MainWindow", "Modify"))
        self.label_18.setText(_translate("MainWindow", "Product"))
        self.add.setText(_translate("MainWindow", "Add"))
        self.edit_2.setText(_translate("MainWindow", "Edit"))
        self.delete_5.setText(_translate("MainWindow", "Delete"))
        self.label_31.setText(_translate("MainWindow", "Discount"))
        self.save_2.setText(_translate("MainWindow", "Save"))
        self.print_3.setText(_translate("MainWindow", "Print"))
        self.cancel_2.setText(_translate("MainWindow", "Cancel"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_15),
                                    _translate("MainWindow", "Modify Sales Bill"))
        self.save_3.setText(_translate("MainWindow", "Save"))
        self.cancel_3.setText(_translate("MainWindow", "Cancel"))
        self.label_22.setText(_translate("MainWindow", "Invoice No"))
        self.Party.setText(_translate("MainWindow", "Party"))
        self.label_23.setText(_translate("MainWindow", "Invoice Date"))
        self.invoicedate_3.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.Modify.setText(_translate("MainWindow", "Modify"))
        self.label_30.setText(_translate("MainWindow", "Product"))
        self.add_2.setText(_translate("MainWindow", "Add"))
        self.edit_3.setText(_translate("MainWindow", "Edit"))
        self.delete_6.setText(_translate("MainWindow", "Delete"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_16),
                                    _translate("MainWindow", "Modify Purchase Bill"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_14), _translate("MainWindow", "Modify"))
        self.label_57.setText(_translate("MainWindow", ":::::::::::::::Print Bill:::::::::::::::"))
        self.label_59.setText(_translate("MainWindow", "Invoice ID"))
        self.search.setText(_translate("MainWindow", "Print"))
        self.label_58.setText(_translate("MainWindow", ":::::::::::::::Modify Bill:::::::::::::::"))
        self.label_58.setText(_translate("MainWindow", ":::::::::::::::Send SMS:::::::::::::::"))
        self.delete_4.setText(_translate("MainWindow", "Send"))


        self.label_52.setText(_translate("MainWindow", ":::::::::::::::Dealer Entry:::::::::::::::"))
        self.label_40.setText(_translate("MainWindow", "Dealer"))
        self.dealer_3.setPlaceholderText(_translate("MainWindow", "Enter dealer name to save"))
        self.label_43.setText(_translate("MainWindow", "Contact"))
        self.dealercontact.setPlaceholderText(_translate("MainWindow", "Enter customer contact to save"))
        self.label_42.setText(_translate("MainWindow", "GSTIN"))
        self.dealergst.setPlaceholderText(_translate("MainWindow", "Enter dealer GSTIN to save"))
        self.label_41.setText(_translate("MainWindow", "Address"))
        self.dealeraddress.setPlaceholderText(_translate("MainWindow", "Enter customer address to save"))
        self.savedealer.setText(_translate("MainWindow", "Save"))
        self.editdealer.setText(_translate("MainWindow", "Edit"))
        self.dealerdelete.setText(_translate("MainWindow", "Delete"))
        self.label_55.setText(_translate("MainWindow", ":::::::::::::::Customer Entry:::::::::::::::"))
        self.label_45.setText(_translate("MainWindow", "Customer"))
        self.pushButton_2.setText(_translate("MainWindow", "Show All"))
        self.deletecontact.setText(_translate("MainWindow", "Search"))
        self.label_54.setText(_translate("MainWindow", ":::::::::::::::Company Entry:::::::::::::::"))
        self.label_44.setText(_translate("MainWindow", "Company"))
        self.companyentry.setPlaceholderText(_translate("MainWindow", "Enter Company name"))
        self.savecomany.setText(_translate("MainWindow", "Save"))
        self.editcompany.setText(_translate("MainWindow", "Edit"))
        self.deletecompany.setText(_translate("MainWindow", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Other"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
