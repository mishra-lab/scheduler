# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 602)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
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
        self.newConfigButton = QtWidgets.QPushButton(self.configActions)
        self.newConfigButton.setObjectName("newConfigButton")
        self.horizontalLayout.addWidget(self.newConfigButton)
        self.openConfigButton = QtWidgets.QPushButton(self.configActions)
        self.openConfigButton.setObjectName("openConfigButton")
        self.horizontalLayout.addWidget(self.openConfigButton)
        self.saveConfigButton = QtWidgets.QPushButton(self.configActions)
        self.saveConfigButton.setObjectName("saveConfigButton")
        self.horizontalLayout.addWidget(self.saveConfigButton)
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
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
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
        self.controlsLayout = QtWidgets.QHBoxLayout()
        self.controlsLayout.setObjectName("controlsLayout")
        self.setupScheduleGroupBox = QtWidgets.QVBoxLayout()
        self.setupScheduleGroupBox.setObjectName("setupScheduleGroupBox")
        self.setupGroupBox = QtWidgets.QGroupBox(self.schedulerTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setupGroupBox.sizePolicy().hasHeightForWidth())
        self.setupGroupBox.setSizePolicy(sizePolicy)
        self.setupGroupBox.setObjectName("setupGroupBox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.setupGroupBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.setupForm = QtWidgets.QFormLayout()
        self.setupForm.setObjectName("setupForm")
        self.configFileLabel = QtWidgets.QLabel(self.setupGroupBox)
        self.configFileLabel.setObjectName("configFileLabel")
        self.setupForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.configFileLabel)
        self.loadConfigButton = QtWidgets.QPushButton(self.setupGroupBox)
        self.loadConfigButton.setObjectName("loadConfigButton")
        self.setupForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.loadConfigButton)
        self.requestsLabel = QtWidgets.QLabel(self.setupGroupBox)
        self.requestsLabel.setObjectName("requestsLabel")
        self.setupForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.requestsLabel)
        self.loadRequestsButton = QtWidgets.QPushButton(self.setupGroupBox)
        self.loadRequestsButton.setObjectName("loadRequestsButton")
        self.setupForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.loadRequestsButton)
        self.holidaysLabel = QtWidgets.QLabel(self.setupGroupBox)
        self.holidaysLabel.setObjectName("holidaysLabel")
        self.setupForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.holidaysLabel)
        self.loadHolidaysButton = QtWidgets.QPushButton(self.setupGroupBox)
        self.loadHolidaysButton.setObjectName("loadHolidaysButton")
        self.setupForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.loadHolidaysButton)
        self.calendarYearLabel = QtWidgets.QLabel(self.setupGroupBox)
        self.calendarYearLabel.setObjectName("calendarYearLabel")
        self.setupForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.calendarYearLabel)
        self.calendarYearSpinBox = QtWidgets.QSpinBox(self.setupGroupBox)
        self.calendarYearSpinBox.setMinimum(2000)
        self.calendarYearSpinBox.setMaximum(3000)
        self.calendarYearSpinBox.setObjectName("calendarYearSpinBox")
        self.setupForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.calendarYearSpinBox)
        self.numberOfBlocksLabel = QtWidgets.QLabel(self.setupGroupBox)
        self.numberOfBlocksLabel.setObjectName("numberOfBlocksLabel")
        self.setupForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.numberOfBlocksLabel)
        self.numberOfBlocksSpinBox = QtWidgets.QSpinBox(self.setupGroupBox)
        self.numberOfBlocksSpinBox.setMinimum(1)
        self.numberOfBlocksSpinBox.setMaximum(9999)
        self.numberOfBlocksSpinBox.setProperty("value", 26)
        self.numberOfBlocksSpinBox.setObjectName("numberOfBlocksSpinBox")
        self.setupForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.numberOfBlocksSpinBox)
        self.exportLpButton = QtWidgets.QPushButton(self.setupGroupBox)
        self.exportLpButton.setObjectName("exportLpButton")
        self.setupForm.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.exportLpButton)
        self.exportMpsButton = QtWidgets.QPushButton(self.setupGroupBox)
        self.exportMpsButton.setObjectName("exportMpsButton")
        self.setupForm.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.exportMpsButton)
        self.horizontalLayout_6.addLayout(self.setupForm)
        self.setupScheduleGroupBox.addWidget(self.setupGroupBox)
        self.scheduleActions = QtWidgets.QGroupBox(self.schedulerTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scheduleActions.sizePolicy().hasHeightForWidth())
        self.scheduleActions.setSizePolicy(sizePolicy)
        self.scheduleActions.setObjectName("scheduleActions")
        self.formLayout = QtWidgets.QFormLayout(self.scheduleActions)
        self.formLayout.setObjectName("formLayout")
        self.shuffleCheckBox = QtWidgets.QCheckBox(self.scheduleActions)
        self.shuffleCheckBox.setObjectName("shuffleCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.shuffleCheckBox)
        self.generateScheduleButton = QtWidgets.QPushButton(self.scheduleActions)
        self.generateScheduleButton.setObjectName("generateScheduleButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.generateScheduleButton)
        self.exportScheduleButton = QtWidgets.QPushButton(self.scheduleActions)
        self.exportScheduleButton.setObjectName("exportScheduleButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.exportScheduleButton)
        self.exportMonthlyButton = QtWidgets.QPushButton(self.scheduleActions)
        self.exportMonthlyButton.setObjectName("exportMonthlyButton")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.exportMonthlyButton)
        self.verboseCheckBox = QtWidgets.QCheckBox(self.scheduleActions)
        self.verboseCheckBox.setObjectName("verboseCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.verboseCheckBox)
        self.setupScheduleGroupBox.addWidget(self.scheduleActions)
        self.controlsLayout.addLayout(self.setupScheduleGroupBox)
        self.outputGroupBox = QtWidgets.QGroupBox(self.schedulerTab)
        self.outputGroupBox.setObjectName("outputGroupBox")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.outputGroupBox)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.outputTextEdit = QtWidgets.QTextEdit(self.outputGroupBox)
        self.outputTextEdit.setReadOnly(True)
        self.outputTextEdit.setObjectName("outputTextEdit")
        self.horizontalLayout_9.addWidget(self.outputTextEdit)
        self.controlsLayout.addWidget(self.outputGroupBox)
        self.verticalLayout_2.addLayout(self.controlsLayout)
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
        self.settingsTab = QtWidgets.QWidget()
        self.settingsTab.setObjectName("settingsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settingsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.constraintsGroupBox = QtWidgets.QGroupBox(self.settingsTab)
        self.constraintsGroupBox.setObjectName("constraintsGroupBox")
        self.formLayout1 = QtWidgets.QFormLayout(self.constraintsGroupBox)
        self.formLayout1.setObjectName("formLayout1")
        self.constraintsForm = QtWidgets.QFormLayout()
        self.constraintsForm.setObjectName("constraintsForm")
        self.coverageLabel = QtWidgets.QLabel(self.constraintsGroupBox)
        self.coverageLabel.setObjectName("coverageLabel")
        self.constraintsForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.coverageLabel)
        self.coverageCheckBox = QtWidgets.QCheckBox(self.constraintsGroupBox)
        self.coverageCheckBox.setChecked(True)
        self.coverageCheckBox.setObjectName("coverageCheckBox")
        self.constraintsForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.coverageCheckBox)
        self.minMaxBlocksLabel = QtWidgets.QLabel(self.constraintsGroupBox)
        self.minMaxBlocksLabel.setObjectName("minMaxBlocksLabel")
        self.constraintsForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.minMaxBlocksLabel)
        self.minMaxBlocksCheckBox = QtWidgets.QCheckBox(self.constraintsGroupBox)
        self.minMaxBlocksCheckBox.setChecked(True)
        self.minMaxBlocksCheckBox.setObjectName("minMaxBlocksCheckBox")
        self.constraintsForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.minMaxBlocksCheckBox)
        self.balancedWeekendsLabel = QtWidgets.QLabel(self.constraintsGroupBox)
        self.balancedWeekendsLabel.setObjectName("balancedWeekendsLabel")
        self.constraintsForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.balancedWeekendsLabel)
        self.balancedWeekendsCheckBox = QtWidgets.QCheckBox(self.constraintsGroupBox)
        self.balancedWeekendsCheckBox.setChecked(True)
        self.balancedWeekendsCheckBox.setObjectName("balancedWeekendsCheckBox")
        self.constraintsForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.balancedWeekendsCheckBox)
        self.balancedLongWeekendsLabel = QtWidgets.QLabel(self.constraintsGroupBox)
        self.balancedLongWeekendsLabel.setObjectName("balancedLongWeekendsLabel")
        self.constraintsForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.balancedLongWeekendsLabel)
        self.balancedLongWeekendsCheckBox = QtWidgets.QCheckBox(self.constraintsGroupBox)
        self.balancedLongWeekendsCheckBox.setChecked(True)
        self.balancedLongWeekendsCheckBox.setObjectName("balancedLongWeekendsCheckBox")
        self.constraintsForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.balancedLongWeekendsCheckBox)
        self.preventConsecutiveBlocksLabel = QtWidgets.QLabel(self.constraintsGroupBox)
        self.preventConsecutiveBlocksLabel.setObjectName("preventConsecutiveBlocksLabel")
        self.constraintsForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.preventConsecutiveBlocksLabel)
        self.preventConsecutiveBlocksCheckBox = QtWidgets.QCheckBox(self.constraintsGroupBox)
        self.preventConsecutiveBlocksCheckBox.setChecked(True)
        self.preventConsecutiveBlocksCheckBox.setObjectName("preventConsecutiveBlocksCheckBox")
        self.constraintsForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.preventConsecutiveBlocksCheckBox)
        self.preventConsecutiveWeekendsLabel = QtWidgets.QLabel(self.constraintsGroupBox)
        self.preventConsecutiveWeekendsLabel.setObjectName("preventConsecutiveWeekendsLabel")
        self.constraintsForm.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.preventConsecutiveWeekendsLabel)
        self.preventConsecutiveWeekendsCheckBox = QtWidgets.QCheckBox(self.constraintsGroupBox)
        self.preventConsecutiveWeekendsCheckBox.setChecked(True)
        self.preventConsecutiveWeekendsCheckBox.setObjectName("preventConsecutiveWeekendsCheckBox")
        self.constraintsForm.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.preventConsecutiveWeekendsCheckBox)
        self.formLayout1.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.constraintsForm)
        self.verticalLayout_3.addWidget(self.constraintsGroupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.tabWidget.addTab(self.settingsTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.configFileLabel.setBuddy(self.loadConfigButton)
        self.requestsLabel.setBuddy(self.loadRequestsButton)
        self.holidaysLabel.setBuddy(self.loadHolidaysButton)
        self.calendarYearLabel.setBuddy(self.calendarYearSpinBox)
        self.numberOfBlocksLabel.setBuddy(self.numberOfBlocksSpinBox)
        self.coverageLabel.setBuddy(self.coverageCheckBox)
        self.minMaxBlocksLabel.setBuddy(self.minMaxBlocksCheckBox)
        self.balancedWeekendsLabel.setBuddy(self.balancedWeekendsCheckBox)
        self.balancedLongWeekendsLabel.setBuddy(self.balancedLongWeekendsCheckBox)
        self.preventConsecutiveBlocksLabel.setBuddy(self.preventConsecutiveBlocksCheckBox)
        self.preventConsecutiveWeekendsLabel.setBuddy(self.preventConsecutiveWeekendsCheckBox)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clinician Scheduler"))
        self.configActions.setTitle(_translate("MainWindow", "Actions"))
        self.newConfigButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Create new configuration file</p></body></html>"))
        self.newConfigButton.setText(_translate("MainWindow", "New Config"))
        self.openConfigButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open configuration file</p></body></html>"))
        self.openConfigButton.setText(_translate("MainWindow", "Open Config"))
        self.saveConfigButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save changes to configuration file</p></body></html>"))
        self.saveConfigButton.setText(_translate("MainWindow", "Save Config"))
        self.newClinicianButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Add a new clinician</p></body></html>"))
        self.newClinicianButton.setText(_translate("MainWindow", "New Clinician"))
        self.editClinicianButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Edit the selected clinician</p></body></html>"))
        self.editClinicianButton.setText(_translate("MainWindow", "Edit Clinician"))
        self.deleteClinicianButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Delete the selected clinician</p></body></html>"))
        self.deleteClinicianButton.setText(_translate("MainWindow", "Delete Clinician"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configurationTab), _translate("MainWindow", "Configuration"))
        self.setupGroupBox.setTitle(_translate("MainWindow", "Setup"))
        self.configFileLabel.setText(_translate("MainWindow", "Configuration"))
        self.loadConfigButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open configuration file</p></body></html>"))
        self.loadConfigButton.setText(_translate("MainWindow", "Load"))
        self.requestsLabel.setText(_translate("MainWindow", "Requests"))
        self.loadRequestsButton.setText(_translate("MainWindow", "Load"))
        self.holidaysLabel.setText(_translate("MainWindow", "Holidays"))
        self.loadHolidaysButton.setText(_translate("MainWindow", "Load"))
        self.calendarYearLabel.setText(_translate("MainWindow", "Calendar Year"))
        self.calendarYearSpinBox.setToolTip(_translate("MainWindow", "<html><head/><body><p>Set the calendar year to be used by the scheduler</p></body></html>"))
        self.numberOfBlocksLabel.setText(_translate("MainWindow", "Number of Blocks"))
        self.exportLpButton.setText(_translate("MainWindow", "Export as LP"))
        self.exportMpsButton.setText(_translate("MainWindow", "Export as MPS"))
        self.scheduleActions.setTitle(_translate("MainWindow", "Schedule"))
        self.shuffleCheckBox.setText(_translate("MainWindow", "Shuffle?"))
        self.generateScheduleButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Generate a new schedule using the given configuration file and calendar information</p></body></html>"))
        self.generateScheduleButton.setText(_translate("MainWindow", "Generate"))
        self.exportScheduleButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Export generated schedule as an Excel spreadsheet</p></body></html>"))
        self.exportScheduleButton.setText(_translate("MainWindow", "Export Yearly"))
        self.exportMonthlyButton.setText(_translate("MainWindow", "Export Monthly"))
        self.verboseCheckBox.setText(_translate("MainWindow", "Verbose Output"))
        self.outputGroupBox.setTitle(_translate("MainWindow", "Output"))
        item = self.scheduleTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Week Number"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.schedulerTab), _translate("MainWindow", "Scheduler"))
        self.constraintsGroupBox.setTitle(_translate("MainWindow", "Constraints"))
        self.coverageLabel.setText(_translate("MainWindow", "Cover All Blocks && Weekends"))
        self.minMaxBlocksLabel.setText(_translate("MainWindow", "Restrict Min/Max Blocks"))
        self.balancedWeekendsLabel.setText(_translate("MainWindow", "Balance Weekends"))
        self.balancedLongWeekendsLabel.setText(_translate("MainWindow", "Balance Long Weekends"))
        self.preventConsecutiveBlocksLabel.setText(_translate("MainWindow", "Prevent Consecutive Blocks"))
        self.preventConsecutiveWeekendsLabel.setText(_translate("MainWindow", "Prevent Consecutive Weekends"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), _translate("MainWindow", "Settings"))

