# pylint: disable=undefined-variable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.mainwindow import MainWindow

app = None

def main():
    app = QApplication([])
    app.setApplicationName("Configuration Manager")

    window = MainWindow()
    app.exec_()

if __name__ == '__main__':
    main()