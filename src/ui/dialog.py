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

        # setup triggers
        self.actionAddDivision.triggered.connect(self.addDivision)
        self.actionRemoveDivision.triggered.connect(self.removeDivision)

        # associate buttons with actions
        self.addButton.setDefaultAction(self.actionAddDivision)
        self.removeButton.setDefaultAction(self.actionRemoveDivision)

    def setData(self, data):
        self.data = data

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
