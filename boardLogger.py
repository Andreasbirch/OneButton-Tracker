import os
import board
from analogio import AnalogIn

class FileLogger():
    folderPath = "data"
    filePath = None
    
    def __init__(self, filename, headers=None):
        if self.folderPath not in os.listdir():
            os.mkdir(self.folderPath)
        
        self.filePath = self.folderPath + os.sep + filename

        if filename not in os.listdir(self.folderPath):
            with open(self.filePath, 'w') as file:
                if headers is not None:
                    file.write(','.join(headers)+"\n")

    def log(self, row):
        with open(self.filePath, 'a+') as file:
            _row = []
            for item in row:
                _row.append(str(item))
            file.write(','.join(_row)+"\n")

    def log_multirows(self, rows):
        _rows = []
        for row in rows:
            _row = []
            for item in row:
                _row.append(str(item))
            _rows.append(','.join(_row) + '\n')
        with open(self.filePath, 'a+') as file:
            file.write(''.join(_rows))

class ConsoleLogger():
    def log(self, row):
        print(row)
    
    def log_multirows(self, rows):
        for row in rows:
            self.log(row)

class BoardLogger():
    logger = None
    def __init__(self, headers=None):
        usb_voltage = AnalogIn(board.A1)

        def get_voltage(pin):
            return (pin.value * 3.3) / 65536 * 2
        
        if get_voltage(usb_voltage) > 2:
            self.logger = ConsoleLogger()
        else:
            self.logger = FileLogger("test.csv", headers)
    
    def log(self, row):
        self.logger.log(row)
    
    def log_multirow(self, rows):
        self.logger.log_multirows(rows)