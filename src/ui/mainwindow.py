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
        dialog.setData(self.data)
        dialog.exec_()

        # reset treeview
        self.syncTreeView()

    def syncTreeView(self):
        self.model.clear()
        self.convertDictToTree(self.model.rootItem, self.data)
        self.treeView.reset()

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
