# pylint: disable=undefined-variable
import json
import ast

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui import delegates, models
from ui.dialog import DialogWindow
from ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.model = models.TreeModel(None)

        self.treeEditorDelegate = delegates.TreeEditDelegate()
        self.treeView.setItemDelegate(self.treeEditorDelegate)
        self.treeView.setModel(self.model)

        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionNew.triggered.connect(self.new)
        self.actionNew_Clinician.triggered.connect(self.createNewClinician)
        self.actionEdit_Clinician.triggered.connect(self.editClinician)
        self.actionDelete_Clinician.triggered.connect(self.deleteClinician)

        # self.path = ''
        self.data = {}

        self.show()

    def open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "JSON files (*.json)"
        )

        if path != '':
            try:
                with open(path, 'r') as f:
                    self.data = json.load(f)
                    self.syncTreeView()

            except Exception as ex:
                QMessageBox.information(self, "Unable to open file", str(ex))

    def save(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", ""
        )

        if fileName != '':
            try:
                with open(fileName, 'w') as f:
                    data = {}
                    self.convertTreeToDict(self.model.rootItem, data)
                    json.dump(data, f)

            except Exception as ex:
                QMessageBox.information(self, "Unable to save file", str(ex))

    def new(self):
        # clear data
        self.data = {}
        
        # build treeview
        self.syncTreeView()

    def createNewClinician(self):
        dialog = DialogWindow()
        dialog.setClinicianDictionary(self.data)
        dialog.exec_()

        # reset treeview
        self.syncTreeView()

    def editClinician(self):
        selectedItem = self.getSelectedClinician()
        if selectedItem:
            clinData = {}
            self.convertTreeToDict(selectedItem, clinData)
            clinData["name"] = selectedItem.itemData[0]

            # transfer clinData to edit dialog
            dialog = DialogWindow()
            dialog.setClinicianDictionary(self.data)
            dialog.setClinician(clinData)
            dialog.exec_()

            self.syncTreeView()

    def deleteClinician(self):
        selectedItem = self.getSelectedClinician()
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
            self.syncTreeView()

    def syncTreeView(self):
        self.model.clear()
        self.convertDictToTree(self.model.rootItem, self.data)
        self.treeView.reset()

    def getSelectedClinician(self):
        idxes = self.treeView.selectedIndexes()
        if len(idxes) > 0:
            # find clinician associated with selected index
            selectedItem = idxes[0].internalPointer()
            parent = selectedItem.parentItem

            while parent.parentItem is not None:
                selectedItem = parent
                parent = selectedItem.parentItem

            return selectedItem
        return None

    def convertDictToTree(self, root, data):
        for key in data:
            if type(data[key]) is dict:
                # recurse on child properties
                child = models.TreeItem(data=[key, None], parent=root)
                self.convertDictToTree(child, data[key])
                root.appendChild(child)
            else:
                # display property value
                child = models.TreeItem(
                    data=[key, str(data[key])], parent=root)
                root.appendChild(child)

    def convertTreeToDict(self, root, data):
        for child in root.childItems:
            key, childData = child.getData(0), child.getData(1)
            if childData == None:
                # recurse on child
                subData = {}
                self.convertTreeToDict(child, subData)
                data[key] = subData
            else:
                # add child data to our JSON object
                value = None
                if childData == '' or childData == None:
                    value = ''
                else:
                    try:
                        # try to parse value as a list/int if possible
                        value = ast.literal_eval(childData)
                    except (ValueError, SyntaxError):
                        # when we can't parse, just store it as a string
                        value = childData
                        
                data[key] = value


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Configuration Manager")

    window = MainWindow()
    app.exec_()
