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
                if headers:
                    file.write(','.join(headers)+"\n")

    def log(self, row):
        with open(self.filePath, 'w') as file:
            file.write(row+"\n")

class ConsoleLogger():
    def log(self, row):
        print(row)

class BoardLogger():
    logger = None
    def __init__(self):
        usb_voltage = AnalogIn(board.A1)

        def get_voltage(pin):
            return (pin.value * 3.3) / 65536 * 2
        
        if get_voltage(usb_voltage) > 2:
            self.logger = ConsoleLogger()
        else:
            self.logger = FileLogger("test.csv")
    
    def log(self, row):
        self.logger.log(row)