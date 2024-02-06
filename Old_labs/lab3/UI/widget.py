import sys
from typing import Optional
import PySide6.QtCore
sys.path.append('../library/')

from PySide6.QtWidgets import QWidget,QMessageBox,QTableWidgetItem
from library.calc import *
from UI.ui_function_calc import Ui_MainWindow

class Widget(QWidget,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Function calculus")

        self.Calculate.clicked.connect(self.calculate)
    
    def calculate(self):
        parameters = [self.SpinBoxA.value(),
                      self.SpinBoxB.value(),
                      self.SpinBoxH.value(),
                      self.SpinBoxK.value(),
                      self.SpinBoxM.value(),]
        self.HandleOutputWidget(parameters,Function(parameters))    
        
    def HandleOutputWidget(self,inputParameters,functionResult):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem(str("№")))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem(str("x")))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem(str("f(x)")))
        a = inputParameters[0]
        b = inputParameters[1]
        h = inputParameters[2]
        self.tableWidget.setColumnCount(3)
        counter = 1
        while a <= b:
            i=a
            self.add_row(counter,i,functionResult[counter-1])
            a+=h
            counter += 1
            
    
    def add_row(self,counter,xValue,functionResult):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setRowCount(rowPosition+1)        
        self.tableWidget.setItem(rowPosition,0,QTableWidgetItem(str(counter)))        
        self.tableWidget.setItem(rowPosition,1,QTableWidgetItem(str(xValue)))
        self.tableWidget.setItem(rowPosition,2,QTableWidgetItem(str(functionResult)))
        