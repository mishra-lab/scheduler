# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.configurationTab = QtWidgets.QWidget()
        self.configurationTab.setObjectName("configurationTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.configurationTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.configActions = QtWidgets.QGroupBox(self.configurationTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configActions.sizePolicy().hasHeightForWidth())
        self.configActions.setSizePolicy(sizePolicy)
        self.configActions.setObjectName("configActions")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.configActions)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newButton = QtWidgets.QPushButton(self.configActions)
        self.newButton.setObjectName("newButton")
        self.horizontalLayout.addWidget(self.newButton)
        self.openButton = QtWidgets.QPushButton(self.configActions)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.saveButton = QtWidgets.QPushButton(self.configActions)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.newClinicianButton = QtWidgets.QPushButton(self.configActions)
        self.newClinicianButton.setObjectName("newClinicianButton")
        self.horizontalLayout.addWidget(self.newClinicianButton)
        self.editClinicianButton = QtWidgets.QPushButton(self.configActions)
        self.editClinicianButton.setObjectName("editClinicianButton")
        self.horizontalLayout.addWidget(self.editClinicianButton)
        self.deleteClinicianButton = QtWidgets.QPushButton(self.configActions)
        self.deleteClinicianButton.setObjectName("deleteClinicianButton")
        self.horizontalLayout.addWidget(self.deleteClinicianButton)
        self.verticalLayout.addWidget(self.configActions)
        self.treeView = QtWidgets.QTreeView(self.configurationTab)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.treeView.setExpandsOnDoubleClick(True)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.tabWidget.addTab(self.configurationTab, "")
        self.schedulerTab = QtWidgets.QWidget()
        self.schedulerTab.setObjectName("schedulerTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.schedulerTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.settingsGroupBox = QtWidgets.QGroupBox(self.schedulerTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsGroupBox.sizePolicy().hasHeightForWidth())
        self.settingsGroupBox.setSizePolicy(sizePolicy)
        self.settingsGroupBox.setObjectName("settingsGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.settingsGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.settingsForm = QtWidgets.QFormLayout()
        self.settingsForm.setObjectName("settingsForm")
        self.configFileLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.configFileLabel.setObjectName("configFileLabel")
        self.settingsForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.configFileLabel)
        self.loadButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.loadButton.setObjectName("loadButton")
        self.settingsForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.loadButton)
        self.calendarYearLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.calendarYearLabel.setObjectName("calendarYearLabel")
        self.settingsForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.calendarYearLabel)
        self.calendarYearSpinBox = QtWidgets.QSpinBox(self.settingsGroupBox)
        self.calendarYearSpinBox.setMinimum(2000)
        self.calendarYearSpinBox.setMaximum(3000)
        self.calendarYearSpinBox.setObjectName("calendarYearSpinBox")
        self.settingsForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.calendarYearSpinBox)
        self.gCalLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.gCalLabel.setObjectName("gCalLabel")
        self.settingsForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.gCalLabel)
        self.gCalLineEdit = QtWidgets.QLineEdit(self.settingsGroupBox)
        self.gCalLineEdit.setObjectName("gCalLineEdit")
        self.settingsForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gCalLineEdit)
        self.retrieveTimeOffRequestsLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.retrieveTimeOffRequestsLabel.setObjectName("retrieveTimeOffRequestsLabel")
        self.settingsForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.retrieveTimeOffRequestsLabel)
        self.retrieveTimeOffRequestsCheckBox = QtWidgets.QCheckBox(self.settingsGroupBox)
        self.retrieveTimeOffRequestsCheckBox.setChecked(True)
        self.retrieveTimeOffRequestsCheckBox.setObjectName("retrieveTimeOffRequestsCheckBox")
        self.settingsForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.retrieveTimeOffRequestsCheckBox)
        self.numberOfBlocksLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.numberOfBlocksLabel.setObjectName("numberOfBlocksLabel")
        self.settingsForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.numberOfBlocksLabel)
        self.numberOfBlocksSpinBox = QtWidgets.QSpinBox(self.settingsGroupBox)
        self.numberOfBlocksSpinBox.setMaximum(26)
        self.numberOfBlocksSpinBox.setProperty("value", 26)
        self.numberOfBlocksSpinBox.setObjectName("numberOfBlocksSpinBox")
        self.settingsForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.numberOfBlocksSpinBox)
        self.horizontalLayout_2.addLayout(self.settingsForm)
        self.verticalLayout_2.addWidget(self.settingsGroupBox)
        self.schedulerButtonLayout = QtWidgets.QHBoxLayout()
        self.schedulerButtonLayout.setObjectName("schedulerButtonLayout")
        self.scheduleActions = QtWidgets.QGroupBox(self.schedulerTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scheduleActions.sizePolicy().hasHeightForWidth())
        self.scheduleActions.setSizePolicy(sizePolicy)
        self.scheduleActions.setObjectName("scheduleActions")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scheduleActions)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.generateScheduleButton = QtWidgets.QPushButton(self.scheduleActions)
        self.generateScheduleButton.setObjectName("generateScheduleButton")
        self.horizontalLayout_3.addWidget(self.generateScheduleButton)
        self.exportScheduleButton = QtWidgets.QPushButton(self.scheduleActions)
        self.exportScheduleButton.setObjectName("exportScheduleButton")
        self.horizontalLayout_3.addWidget(self.exportScheduleButton)
        self.schedulerButtonLayout.addWidget(self.scheduleActions)
        self.calendarActions = QtWidgets.QGroupBox(self.schedulerTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarActions.sizePolicy().hasHeightForWidth())
        self.calendarActions.setSizePolicy(sizePolicy)
        self.calendarActions.setObjectName("calendarActions")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.calendarActions)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.publishCalendarButton = QtWidgets.QPushButton(self.calendarActions)
        self.publishCalendarButton.setObjectName("publishCalendarButton")
        self.horizontalLayout_4.addWidget(self.publishCalendarButton)
        self.clearCalendarButton = QtWidgets.QPushButton(self.calendarActions)
        self.clearCalendarButton.setObjectName("clearCalendarButton")
        self.horizontalLayout_4.addWidget(self.clearCalendarButton)
        self.schedulerButtonLayout.addWidget(self.calendarActions)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.schedulerButtonLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.schedulerButtonLayout)
        self.scheduleTable = QtWidgets.QTableWidget(self.schedulerTab)
        self.scheduleTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.scheduleTable.setObjectName("scheduleTable")
        self.scheduleTable.setColumnCount(1)
        self.scheduleTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.scheduleTable.setHorizontalHeaderItem(0, item)
        self.scheduleTable.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.scheduleTable)
        self.tabWidget.addTab(self.schedulerTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew_Clinician = QtWidgets.QAction(MainWindow)
        self.actionNew_Clinician.setObjectName("actionNew_Clinician")
        self.actionEdit_Clinician = QtWidgets.QAction(MainWindow)
        self.actionEdit_Clinician.setObjectName("actionEdit_Clinician")
        self.actionDelete_Clinician = QtWidgets.QAction(MainWindow)
        self.actionDelete_Clinician.setObjectName("actionDelete_Clinician")
        self.actionGenerate_Schedule = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Schedule.setObjectName("actionGenerate_Schedule")
        self.actionExport_Schedule = QtWidgets.QAction(MainWindow)
        self.actionExport_Schedule.setObjectName("actionExport_Schedule")
        self.actionPublish = QtWidgets.QAction(MainWindow)
        self.actionPublish.setObjectName("actionPublish")
        self.actionClear_Calendar = QtWidgets.QAction(MainWindow)
        self.actionClear_Calendar.setObjectName("actionClear_Calendar")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.newButton.clicked['bool'].connect(self.actionNew.trigger)
        self.openButton.clicked['bool'].connect(self.actionOpen.trigger)
        self.saveButton.clicked['bool'].connect(self.actionSave.trigger)
        self.newClinicianButton.clicked['bool'].connect(self.actionNew_Clinician.trigger)
        self.editClinicianButton.clicked['bool'].connect(self.actionEdit_Clinician.trigger)
        self.deleteClinicianButton.clicked['bool'].connect(self.actionDelete_Clinician.trigger)
        self.loadButton.clicked['bool'].connect(self.actionOpen.trigger)
        self.generateScheduleButton.clicked['bool'].connect(self.actionGenerate_Schedule.trigger)
        self.exportScheduleButton.clicked['bool'].connect(self.actionExport_Schedule.trigger)
        self.publishCalendarButton.clicked['bool'].connect(self.actionPublish.trigger)
        self.clearCalendarButton.clicked['bool'].connect(self.actionClear_Calendar.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.configActions.setTitle(_translate("MainWindow", "Actions"))
        self.newButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Create new configuration file</p></body></html>"))
        self.newButton.setText(_translate("MainWindow", "New"))
        self.openButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open configuration file</p></body></html>"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.saveButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save changes to configuration file</p></body></html>"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.newClinicianButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Add a new clinician</p></body></html>"))
        self.newClinicianButton.setText(_translate("MainWindow", "New Clinician"))
        self.editClinicianButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Edit the selected clinician</p></body></html>"))
        self.editClinicianButton.setText(_translate("MainWindow", "Edit Clinician"))
        self.deleteClinicianButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Delete the selected clinician</p></body></html>"))
        self.deleteClinicianButton.setText(_translate("MainWindow", "Delete Clinician"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configurationTab), _translate("MainWindow", "Configuration"))
        self.settingsGroupBox.setTitle(_translate("MainWindow", "Settings"))
        self.configFileLabel.setText(_translate("MainWindow", "Configuration File Status: Not Loaded"))
        self.loadButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open configuration file</p></body></html>"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.calendarYearLabel.setText(_translate("MainWindow", "Calendar Year"))
        self.calendarYearSpinBox.setToolTip(_translate("MainWindow", "<html><head/><body><p>Set the calendar year to be used by the scheduler</p></body></html>"))
        self.gCalLabel.setText(_translate("MainWindow", "Google Calendar ID"))
        self.gCalLineEdit.setToolTip(_translate("MainWindow", "<html><head/><body><p>Set the calendar ID to retrieve calendar events from and publish generated schedule to</p></body></html>"))
        self.retrieveTimeOffRequestsLabel.setText(_translate("MainWindow", "Retrieve Time-off Requests"))
        self.numberOfBlocksLabel.setText(_translate("MainWindow", "Number of Blocks"))
        self.scheduleActions.setTitle(_translate("MainWindow", "Schedule"))
        self.generateScheduleButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Generate a new schedule using the given configuration file and calendar information</p></body></html>"))
        self.generateScheduleButton.setText(_translate("MainWindow", "Generate"))
        self.exportScheduleButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export generated schedule as an Excel spreadsheet</p></body></html>"))
        self.exportScheduleButton.setText(_translate("MainWindow", "Export"))
        self.calendarActions.setTitle(_translate("MainWindow", "Calendar"))
        self.publishCalendarButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Publish the generated schedule to the calendar</p></body></html>"))
        self.publishCalendarButton.setText(_translate("MainWindow", "Publish"))
        self.clearCalendarButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Clear published schedule from calendar for the given calendar year</p></body></html>"))
        self.clearCalendarButton.setText(_translate("MainWindow", "Clear"))
        item = self.scheduleTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Week Number"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.schedulerTab), _translate("MainWindow", "Scheduler"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open configuration file"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setToolTip(_translate("MainWindow", "Create new configuration file"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save changes to configuration file"))
        self.actionNew_Clinician.setText(_translate("MainWindow", "New Clinician"))
        self.actionNew_Clinician.setToolTip(_translate("MainWindow", "Add a new clinician"))
        self.actionEdit_Clinician.setText(_translate("MainWindow", "Edit Clinician"))
        self.actionEdit_Clinician.setToolTip(_translate("MainWindow", "Edit the selected clinician"))
        self.actionDelete_Clinician.setText(_translate("MainWindow", "Delete Clinician"))
        self.actionDelete_Clinician.setToolTip(_translate("MainWindow", "Delete the selected clinician"))
        self.actionGenerate_Schedule.setText(_translate("MainWindow", "Generate Schedule"))
        self.actionExport_Schedule.setText(_translate("MainWindow", "Export Schedule"))
        self.actionPublish.setText(_translate("MainWindow", "Publish"))
        self.actionClear_Calendar.setText(_translate("MainWindow", "Clear Calendar"))

