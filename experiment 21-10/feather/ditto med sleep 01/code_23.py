import board
import time
import alarm
import busio
from adafruit_ds3231 import DS3231
i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1000) ## Deep sleep 1000 seconds

alarm.exit_and_deep_sleep_until_alarms(time_alarm)