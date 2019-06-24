from datetime import datetime

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
        self.output.insertHtml('<p style="color:{2}">[{0}] {1}</p><br>'.format(timestamp, line, colour))