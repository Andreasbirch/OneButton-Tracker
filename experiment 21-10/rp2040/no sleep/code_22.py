import board
import busio
import time
import alarm, alarm.time
from adafruit_ds3231 import DS3231

i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

alarm.light_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1000))