# pylint: disable=undefined-variable
from PyQt5.QtCore import *

class TreeItem(object):
    def __init__(self, data=[], parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def getData(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def setData(self, column, newData):
        try:
            self.itemData[column] = newData
        except IndexError:
            pass

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(("Property Name", "Property Value"))

    def columnCount(self, parent):
        # if parent.isValid():
        #     return parent.internalPointer().columnCount()
        # else:
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.getData(index.column())

    def setData(self, index, value, role):
        data = self.data(index, Qt.DisplayRole)
        # make sure user can only edit property values that are not None
        # this will prevent the user from editing parent properties
        if role == Qt.EditRole and data != None and value != data:
            # update value in tree model
            item = index.internalPointer()
            item.setData(index.column(), value)
        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flag = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        # prevent user from editing property names (i.e. first column)
        if index.column() == 0: return flag

        return flag | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.getData(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def clear(self):
        QAbstractItemModel.beginResetModel(self)
        self.rootItem.childItems = []
        QAbstractItemModel.endResetModel(self)