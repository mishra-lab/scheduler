# pylint: disable=undefined-variable
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.mainwindow import MainWindow

app = None

def main():
    app = QApplication([])
    app.setApplicationName("Clinician Scheduler")

    # increase global font size
    global_font = app.font()
    global_font.setPointSize(11)
    app.setFont(global_font)

    window = MainWindow()
    app.exec_()

if __name__ == '__main__':
    main()