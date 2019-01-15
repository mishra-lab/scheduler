# pylint: disable=undefined-variable
import ast
import json
from datetime import datetime, timedelta

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from constants import WEEK_HOURS, WEEKEND_HOURS
from helpers.apihelper import ApiHelper
from helpers.excelhelper import ExcelHelper
from helpers.uihelper import UiHelper
from services import scheduler

from .delegates import TreeEditDelegate
from .dialog import DialogWindow
from .models import TreeModel
from .ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self._configuration = {}
        self._configPath = ''

        self.setupUi(self)
        self.setupConfigurationTab()
        self.setupSchedulerTab()

        self.tabWidget.setCurrentIndex(0)

        self.show()

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, value):
        if type(value) is dict:
            self._configuration = value
        else:
            raise TypeError(value)

    @property
    def configPath(self):
        return self._configPath

    @configPath.setter
    def configPath(self, value):
        if value:
            self._configPath = value
            self.tabWidget.setTabText(0, 'Configuration ({})'.format(self._configPath))
            self.tabWidget.setTabText(1, 'Scheduler ({})'.format(self._configPath))

    def setupConfigurationTab(self):
        # treeview setup
        self.model = TreeModel(None)
        self.treeEditorDelegate = TreeEditDelegate()
        self.treeView.setItemDelegate(self.treeEditorDelegate)
        self.treeView.setModel(self.model)

        # action setup
        self.actionOpen.triggered.connect(self.openConfig)
        self.actionSave.triggered.connect(self.saveConfig)
        self.actionNew.triggered.connect(self.newConfig)
        self.actionNew_Clinician.triggered.connect(self.createNewClinician)
        self.actionEdit_Clinician.triggered.connect(self.editClinician)
        self.actionDelete_Clinician.triggered.connect(self.deleteClinician)

        self.newConfig()

    def setupSchedulerTab(self):
        # action setup
        self.actionGenerate_Schedule.triggered.connect(self.generateSchedule)
        self.actionExport_Schedule.triggered.connect(self.exportSchedule)
        self.actionExport_Monthly.triggered.connect(self.exportMonthlySchedule)
        self.actionPublish.triggered.connect(self.publishSchedule)
        self.actionClear_Calendar.triggered.connect(self.clearCalendar)

        # misc vars
        self.holidayMap = {}

    def openConfig(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "JSON files (*.json)"
        )

        if path != '':
            try:
                with open(path, 'r') as f:
                    self.configPath = path
                    self.configuration = json.load(f)
                    UiHelper.syncTreeView(self.treeView, self.model, self.configuration)

            except Exception as ex:
                QMessageBox.critical(self, "Unable to open file", str(ex))

    def saveConfig(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON files (*.json)"
        )

        if fileName != '':
            try:
                with open(fileName, 'w') as f:
                    data = {}
                    UiHelper.convertTreeToDict(self.model.rootItem, data)
                    json.dump(data, f)
                    self.configPath = fileName

            except Exception as ex:
                QMessageBox.critical(self, "Unable to save file", str(ex))

    def newConfig(self):
        # clear data
        self.configuration = {}
        self.configPath = 'new config'
        
        # build treeview
        UiHelper.syncTreeView(self.treeView, self.model, self.configuration)

    def createNewClinician(self):
        dialog = DialogWindow()
        dialog.setClinicianDictionary(self.configuration)
        dialog.exec_()

        # reset treeview
        UiHelper.syncTreeView(self.treeView, self.model, self.configuration)

    def editClinician(self):
        selectedItem = UiHelper.getSelectedRoot(self.treeView)
        if selectedItem:
            clinData = {}
            UiHelper.convertTreeToDict(selectedItem, clinData)
            clinData["name"] = selectedItem.itemData[0]

            # transfer clinData to edit dialog
            dialog = DialogWindow()
            dialog.setClinicianDictionary(self.configuration)
            dialog.setClinician(clinData)
            dialog.exec_()

            UiHelper.syncTreeView(self.treeView, self.model, self.configuration)

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

            del self.configuration[clinName]
            UiHelper.syncTreeView(self.treeView, self.model, self.configuration)

    def generateSchedule(self):
        self.clearScheduleTable()

        numClinicians = len(self.configuration.keys())
        if numClinicians <= 0:
            QMessageBox.critical(self, "No Clinicians Configured", "Please load a configuration file with at least one clinician!")
            return

        numBlocks = self.numberOfBlocksSpinBox.value()
        retrieveTimeOff = self.retrieveTimeOffRequestsCheckBox.isChecked()
        retrieveLongWeekends = self.retrieveLongWeekendsCheckBox.isChecked()
        calendarYear = self.calendarYearSpinBox.value()
        calendarId = self.gCalLineEdit.text()

        requests = []
        holidays = []

        if retrieveTimeOff:    
            if not calendarId:
                QMessageBox.critical(self, "Missing Calendar ID", "Please supply a calendar ID!")
                return

            # read timeoff requests from gcal
            startDate = datetime(calendarYear, 1, 1)
            endDate = startDate + timedelta(weeks=52)
            requests = ApiHelper(calendarId).get_events(
                start=startDate.isoformat() + 'Z',
                end=endDate.isoformat() + 'Z',
                search_str='[request]'
            )

        if retrieveLongWeekends:
            if not calendarId:
                QMessageBox.critical(self, "Missing Calendar ID", "Please supply a calendar ID!")
                return

            # read longweekend events from gcal
            startDate = datetime(calendarYear, 1, 1)
            endDate = startDate + timedelta(weeks=52)
            holidays = ApiHelper(calendarId).get_events(
                start=startDate.isoformat() + 'Z',
                end=endDate.isoformat() + 'Z',
                search_str='[holiday]'
            )

        # init scheduler with all the given data
        schedule = scheduler.Scheduler(
            num_blocks=numBlocks, clin_data=self.configuration, timeoff_data=requests, long_weekends=holidays).generate(debug=True)
        if schedule is None:
            QMessageBox.critical(self, "Could not generate schedule!",
                "Could not generate a schedule based on the given constraints and configuration. Try adjusting min/max values in the configuration tab.")
        
        else:
            divAssignments = schedule[0]
            weekendAssignments = schedule[1]
            self.holidayMap = schedule[2]
            longWeekends = list(self.holidayMap.values())
            
            # create rows for each week num
            for weekNum in range(1, len(weekendAssignments) + 1):
                rowCount = self.scheduleTable.rowCount()
                self.scheduleTable.insertRow(rowCount)
                value = str(weekNum) + '*' if weekNum in longWeekends else str(weekNum)
                self.scheduleTable.setItem(rowCount, 0, QTableWidgetItem(value))

            for divName in divAssignments:
                # create division columns
                assignments = divAssignments[divName]
                columnCount = self.scheduleTable.columnCount()
                self.scheduleTable.insertColumn(columnCount)
                self.scheduleTable.setHorizontalHeaderItem(columnCount, QTableWidgetItem(divName))

                for i in range(len(assignments)):
                    clinName = assignments[i]
                    self.scheduleTable.setItem(i, columnCount, QTableWidgetItem(clinName))

            weekendCol = self.scheduleTable.columnCount()
            self.scheduleTable.insertColumn(weekendCol)
            self.scheduleTable.setHorizontalHeaderItem(weekendCol, QTableWidgetItem("Weekend"))

            for i in range(len(weekendAssignments)):
                clinName = weekendAssignments[i]
                self.scheduleTable.setItem(i, weekendCol, QTableWidgetItem(clinName))
                    
    
    def exportSchedule(self):
        # open save dialog to let user choose folder + filename
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Excel file", "", "Excel file (*.xlsx)"
        )

        if not fileName:
            return

        ExcelHelper.saveYearlySchedule(fileName, self.scheduleTable)

    def exportMonthlySchedule(self):
        # open save dialog to let user choose folder + filename
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Excel file", "", "Excel file (*.xlsx)"
        )

        if not fileName:
            return

        calendarYear = self.calendarYearSpinBox.value()
        ExcelHelper.saveMonthlySchedule(fileName, self.scheduleTable, calendarYear, self.holidayMap)

    def publishSchedule(self):
        calendarYear = self.calendarYearSpinBox.value()
        calendarId = self.gCalLineEdit.text()

        if not calendarId:
            QMessageBox.critical(self, "Missing Calendar ID", "Please supply a calendar ID!")
            return

        # confirm user action
        reply = QMessageBox.question(
                self, 
                "Publish Calendar Warning", 
                "This action will publish the generated schedule to the specified calendar. Are you sure you want to continue?",
                QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No: return


        rows = self.scheduleTable.rowCount()
        cols = self.scheduleTable.columnCount()

        # display progress so user knows app is working
        progress = QProgressDialog(
            "Publishing schedule...",
            "",
            1,
            # max progress = total # of events to be created
            (cols - 1) * rows
        )
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setMinimumDuration(0)
        
        # go through table, creating an event per each row, per each column
        for i in range(rows):
            for j in range(1, cols):
                progress.setValue(j + (cols - 1) * i)
                colHeader = self.scheduleTable.horizontalHeaderItem(j).text()

                weekText = self.scheduleTable.item(i, 0).text() 
                weekNum = int(weekText[:-1]) if weekText[-1] == '*' else int(weekText)
                name = self.scheduleTable.item(i, j).text()
                email = self.configuration[name]['email']

                # figure out correct event time range
                if colHeader == 'Weekend':
                    summary = '[scheduler] {} - on call'.format(name)
                    start = datetime.strptime(
                        # year / weekNum / Friday / 5PM
                        '{0}/{1:02d}/5/17:00'.format(calendarYear, weekNum),
                        '%G/%V/%u/%H:%M'
                    )
                    end = start + timedelta(hours=WEEKEND_HOURS)
                else:
                    summary = '[scheduler] {} - on call ({} division)'.format(name, colHeader)
                    start = datetime.strptime(
                        # year / weekNum / Monday / 8AM
                        '{0}/{1:02d}/1/08:00'.format(calendarYear, weekNum),
                        '%G/%V/%u/%H:%M'
                    )
                    end = start + timedelta(hours=WEEK_HOURS)

                # call api to publish event
                ApiHelper(calendarId).create_event(
                    start.isoformat(),
                    end.isoformat(),
                    [email] if email else [],
                    summary
                )

    def clearCalendar(self, args):
        calendarYear = self.calendarYearSpinBox.value()
        calendarId = self.gCalLineEdit.text()

        if not calendarId:
            QMessageBox.critical(self, "Missing Calendar ID", "Please supply a calendar ID!")
            return

        # confirm user action
        reply = QMessageBox.question(
                self, 
                "Clear Calendar Warning", 
                "This action will clear all events generated by the scheduler for the year {}. Are you sure you want to continue?".format(
                    calendarYear),
                QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No: return

        # call API
        api = ApiHelper(calendarId)
        startDate = datetime(calendarYear, 1, 1)
        endDate = startDate + timedelta(weeks=52)

        events = api.get_events(
            startDate.isoformat() + 'Z',
            endDate.isoformat() + 'Z',
            search_str='[scheduler]'
        )

        # display progress so user knows app is working
        progress = QProgressDialog(
            "Clearing schedule...",
            "",
            0,
            # max progress = total # of events to be created
            len(events) - 1
        )
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setMinimumDuration(0)

        for i in range(len(events)):
            progress.setValue(i)
            id_ = events[i]['id']
            api.delete_event(id_)

    def clearScheduleTable(self):
        while self.scheduleTable.rowCount() > 0:
            lastRow = self.scheduleTable.rowCount()
            self.scheduleTable.removeRow(lastRow - 1)

        while self.scheduleTable.columnCount() > 1:
            lastColumn = self.scheduleTable.columnCount()
            self.scheduleTable.removeColumn(lastColumn - 1)


if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationName("Configuration Manager")

    window = MainWindow()
    app.exec_()
