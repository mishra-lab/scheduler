# pylint: disable=undefined-variable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.mainwindow import MainWindow

app = None

def main():
    app = QApplication([])
    app.setApplicationName("Clinician Scheduler")

    window = MainWindow()
    app.exec_()

if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        QMessageBox.critical(app, "", "Unknown error occurred!\nDetails: {}".format(str(ex)))