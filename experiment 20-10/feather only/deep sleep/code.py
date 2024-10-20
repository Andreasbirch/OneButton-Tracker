import alarm.time
import board
import alarm
import time
from analogio import AnalogIn
from logger import FileLogger, ConsoleLogger

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
usb_voltage = AnalogIn(board.A1)

print("Going to sleep.")
deep_sleep_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic()+1000)
alarm.exit_and_deep_sleep_until_alarms(deep_sleep_alarm)