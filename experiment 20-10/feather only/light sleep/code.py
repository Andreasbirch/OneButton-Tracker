import board
from time import sleep
from analogio import AnalogIn
from logger import FileLogger, ConsoleLogger

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
usb_voltage = AnalogIn(board.A1)

print("Going to sleep.")
sleep(1000)
print("Woke up.")