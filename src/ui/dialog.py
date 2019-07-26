# pylint: disable=undefined-variable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui import delegates
from ui.ui_dialog import Ui_Dialog


class DialogWindow(QDialog, Ui_Dialog):
    def __init__(self, isEdit=False, *args, **kwargs):
        super(DialogWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.isEdit = isEdit

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
        # store current clinician name in case it changes
        if self.isEdit: self.oldName = data['name']
    
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
        """
        Accept changes and update configuration.
        """

        # validate data
        if not self.checkInput():
            return

        ret = False

        if self.isEdit: 
            ret = self.acceptEdit()
        else: 
            ret = self.acceptNew()

        if ret: QDialog.accept(self)

    def acceptEdit(self):
        """
        Updates configuration based on edits made to existing clinician.

        Returns True iff changes were accepted.
        """

        clinician = self.extractFormData()

        # check if the newly chosen name already exists in the config
        if self.oldName != clinician['name'] and clinician['name'] in self.clinDict:
            QMessageBox.critical(
                self,
                "Name Error",
                "A clinician with this name already exists in the configuration file. Please choose a different name.",
                QMessageBox.Ok
            )

            return False

        # remove old data and update config
        del self.clinDict[self.oldName]
        self.clinDict[clinician['name']] = clinician

        return True

    def acceptNew(self):
        """
        Updates configuration for newly added clinician.
        
        Returns True iff changes were accepted.
        """

        clinician = self.extractFormData()

        # check if such a name is already stored in config
        if clinician['name'] in self.clinDict:
            QMessageBox.critical(
                self,
                "Name Error",
                "A clinician with this name already exists in the configuration file. Please choose a different name.",
                QMessageBox.Ok
            )

            return False

        # set new clinician
        self.clinDict[clinician['name']] = clinician

        return True

    def extractFormData(self):
        # extract name, email
        clinician = dict()
        clinName = self.nameLineEdit.text()
        clinician['name'] = clinName

        clinEmail = self.emailLineEdit.text()
        clinician['email'] = clinEmail
        clinician['divisions'] = dict()
        
        # extract clinician's division list
        for i in range(self.divisionTable.rowCount()):
            division = dict()

            try:
                divName = self.divisionTable.item(i, 0).text()
                divMin = self.divisionTable.item(i, 1).text()
                divMax = self.divisionTable.item(i, 2).text()
            except AttributeError:
                break

            division['min'] = int(divMin)
            division['max'] = int(divMax)
            clinician['divisions'][divName] = division

        return clinician
