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