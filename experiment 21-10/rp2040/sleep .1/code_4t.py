import board
import time
import digitalio
import os
from analogio import AnalogIn

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
usb_voltage = AnalogIn(board.A1)



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

    def log(self, *rows):
        with open(self.filePath, 'w') as file:
            for row in rows:
                file.write(','.join(row) + "\n")

class ConsoleLogger():
    def log(self, *rows):
        for row in rows:
            if isinstance(row, str):
                print(row)
            else:
                print(', '.join(row))



def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

logger = None

if get_voltage(usb_voltage) > 2:
    logger = ConsoleLogger()
else:
    logger = FileLogger("test.csv")

repeat_times = 100

time_before = time.monotonic_ns()
for i in range(repeat_times):
    logger.log([
        "1.23456, 1.23456, 1.23456, 123, still"
    ])
time_after = time.monotonic_ns()
average_ms = (time_after - time_before) / 1_000_000 ## Difference from ns to ms
average_ms /= repeat_times ## Average

logger.log(str(average_ms))

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
while True:
    led.value = True