# pylint: disable=undefined-variable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui import delegates
from ui.ui_dialog import Ui_Dialog


class DialogWindow(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(DialogWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # make sure min/max columns only accept integer values
        # note: need class to "own" delegates, otherwise they will be GC'd and cause a segfault
        self.minDelegate = delegates.ValidationDelegate(
            validator=QIntValidator)
        self.maxDelegate = delegates.ValidationDelegate(
            validator=QIntValidator)
        self.divisionTable.setItemDelegateForColumn(
            1,
            self.minDelegate)
        self.divisionTable.setItemDelegateForColumn(
            2,
            self.maxDelegate)

        # setup connects
        self.actionAddDivision.triggered.connect(self.addDivision)
        self.actionRemoveDivision.triggered.connect(self.removeDivision)

        # associate buttons with actions
        self.addButton.setDefaultAction(self.actionAddDivision)
        self.removeButton.setDefaultAction(self.actionRemoveDivision)

    def setClinicianDictionary(self, clinDict):
        self.clinDict = clinDict

    def setClinician(self, data):
        self.nameLineEdit.setText(data['name'])
        self.emailLineEdit.setText(data['email'])
        
        for divName in data['divisions']:
            rowCount = self.divisionTable.rowCount()
            self.divisionTable.insertRow(rowCount)

            divObject = data['divisions'][divName]
            self.divisionTable.setItem(rowCount, 0, QTableWidgetItem(divName))
            self.divisionTable.setItem(rowCount, 1, QTableWidgetItem(str(divObject['min'])))
            self.divisionTable.setItem(rowCount, 2, QTableWidgetItem(str(divObject['max'])))

    def addDivision(self):
        try:
            rowIdx = self.divisionTable.rowCount()
            self.divisionTable.insertRow(rowIdx)
        except Exception as ex:
            print(ex)

    def removeDivision(self):
        rowIdx = self.divisionTable.currentRow()
        if rowIdx >= 0:
            self.divisionTable.removeRow(rowIdx)

    def checkInput(self):
        if not self.nameLineEdit.text():
            QMessageBox.critical(self, "Input Error", "Missing clinician name!")
            return False

        return True

    def accept(self):
        # validate data
        if not self.checkInput():
            return

        # create new clinician in self.data
        clinName = self.nameLineEdit.text()
        clinician = dict()

        if clinName in self.clinDict:
            # warn user that data will be overwritten for that clinician
            reply = QMessageBox.question(
                self, 
                "Overwrite Warning", 
                "This action will overwrite the current data stored for {}. Are you sure you want to continue?".format(
                    clinName)
                , QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.No: return

        # assume no data exists about current clinician
        clinEmail = self.emailLineEdit.text()
        clinician['email'] = clinEmail
        clinician['divisions'] = dict()
        
        for i in range(self.divisionTable.rowCount()):
            division = dict()

            # extract data
            divName = self.divisionTable.item(i, 0).text()
            divMin = self.divisionTable.item(i, 1).text()
            divMax = self.divisionTable.item(i, 2).text()

            division['min'] = divMin
            division['max'] = divMax
            clinician['divisions'][divName] = division

        self.clinDict[clinName] = clinician
        QDialog.accept(self)

