import ast

from ui import models


class UiHelper:
    @staticmethod
    def syncTreeView(treeView, model, data):
        model.clear()
        UiHelper.convertDictToTree(model.rootItem, data)
        treeView.reset()

    @staticmethod
    def getSelectedRoot(treeView):
        idxes = treeView.selectedIndexes()
        if len(idxes) > 0:
            # find clinician associated with selected index
            selectedItem = idxes[0].internalPointer()
            parent = selectedItem.parentItem

            while parent.parentItem is not None:
                selectedItem = parent
                parent = selectedItem.parentItem

            return selectedItem
        return None

    @staticmethod
    def convertDictToTree(root, data):
        for key in data:
            if type(data[key]) is dict:
                # recurse on child properties
                child = models.TreeItem(data=[key, None], parent=root)
                UiHelper.convertDictToTree(child, data[key])
                root.appendChild(child)
            else:
                # display property value
                child = models.TreeItem(
                    data=[key, str(data[key])], parent=root)
                root.appendChild(child)

    @staticmethod
    def convertTreeToDict(root, data):
        for child in root.childItems:
            key, childData = child.getData(0), child.getData(1)
            if childData == None:
                # recurse on child
                subData = {}
                UiHelper.convertTreeToDict(child, subData)
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
