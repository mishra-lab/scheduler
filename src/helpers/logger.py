# pylint: disable=undefined-variable
from datetime import datetime
from PyQt5.QtGui import *

LEVELCOLOURS = {
    'INFO': 'black',
    'WARNING': 'orange',
    'ERROR': 'red'
}

class Logger:
    def __init__(self, output):
        self.output = output

    def write_line(self, line, level='INFO'):
        timestamp = datetime.now().time().strftime('%H:%M:%S')
        colour = LEVELCOLOURS[level]

        self.output.moveCursor(QTextCursor.End)
        self.output.insertHtml('<span style="color:{2}">[{0}] {1}</span><br>'.format(timestamp, line, colour))