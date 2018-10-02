# pylint: disable=undefined-variable
import json
import ast

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui import delegates, models
from ui.helpers import UiHelper
from ui.dialog import DialogWindow
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setupConfigurationTab()
        self.setupSchedulerTab()

        self.show()

    def setupConfigurationTab(self):
        self.data = {}

        # treeview setup
        self.model = models.TreeModel(None)
        self.treeEditorDelegate = delegates.TreeEditDelegate()
        self.treeView.setItemDelegate(self.treeEditorDelegate)
        self.treeView.setModel(self.model)

        # action setup
        self.actionOpen.triggered.connect(self.openConfig)
        self.actionSave.triggered.connect(self.saveConfig)
        self.actionNew.triggered.connect(self.newConfig)
        self.actionNew_Clinician.triggered.connect(self.createNewClinician)
        self.actionEdit_Clinician.triggered.connect(self.editClinician)
        self.actionDelete_Clinician.triggered.connect(self.deleteClinician)

    def setupSchedulerTab(self):
        # action setup
        self.actionGenerate_Schedule.triggered.connect(self.generateSchedule)
        self.actionExport_Schedule.triggered.connect(self.exportSchedule)
        self.actionPublish.triggered.connect(self.publishSchedule)
        self.actionClear_Calendar.triggered.connect(self.clearCalendar)

    def openConfig(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "JSON files (*.json)"
        )

        if path != '':
            try:
                with open(path, 'r') as f:
                    self.data = json.load(f)
                    UiHelper.syncTreeView(self.treeView, self.model, self.data)

            except Exception as ex:
                QMessageBox.information(self, "Unable to open file", str(ex))

    def saveConfig(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", ""
        )

        if fileName != '':
            try:
                with open(fileName, 'w') as f:
                    data = {}
                    UiHelper.convertTreeToDict(self.model.rootItem, data)
                    json.dump(data, f)

            except Exception as ex:
                QMessageBox.information(self, "Unable to save file", str(ex))

    def newConfig(self):
        # clear data
        self.data = {}
        
        # build treeview
        UiHelper.syncTreeView(self.treeView, self.model, self.data)

    def createNewClinician(self):
        dialog = DialogWindow()
        dialog.setClinicianDictionary(self.data)
        dialog.exec_()

        # reset treeview
        UiHelper.syncTreeView(self.treeView, self.model, self.data)

    def editClinician(self):
        selectedItem = UiHelper.getSelectedRoot(self.treeView)
        if selectedItem:
            clinData = {}
            UiHelper.convertTreeToDict(selectedItem, clinData)
            clinData["name"] = selectedItem.itemData[0]

            # transfer clinData to edit dialog
            dialog = DialogWindow()
            dialog.setClinicianDictionary(self.data)
            dialog.setClinician(clinData)
            dialog.exec_()

            UiHelper.syncTreeView(self.treeView, self.model, self.data)

    def deleteClinician(self):
        selectedItem = UiHelper.getSelectedRoot(self.treeView)
        if selectedItem:
            clinName = selectedItem.itemData[0]
            reply = QMessageBox.question(
                self, 
                "Delete Warning", 
                "This action will delete the current data stored for {}. Are you sure you want to continue?".format(
                    clinName)
                , QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No: return

            del self.data[clinName]
            UiHelper.syncTreeView(self.treeView, self.model, self.data)

    def generateSchedule(self):
        # TODO:
        pass
    
    def exportSchedule(self):
        # TODO:
        pass

    def publishSchedule(self):
        # TODO:
        pass

    def clearCalendar(self):
        # TODO:
        pass


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Configuration Manager")

    window = MainWindow()
    app.exec_()
