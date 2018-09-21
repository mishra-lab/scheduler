# pylint: disable=undefined-variable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ValidationDelegate(QItemDelegate):
    """
    Custom delegate to prevent editing of item
    """

    def __init__(self, parent=None, validator=None):
        QItemDelegate.__init__(self, parent)
        self.validator = validator

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(self.validator())
        return editor

class TreeEditDelegate(QItemDelegate):
    """
    Custom delegate that copies data into editor during initialization
    """

    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        if index.isValid():
            editor.setText(index.data())
        else:
            QItemDelegate.setEditorData(editor, index)