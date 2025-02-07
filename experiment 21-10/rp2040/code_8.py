import board
import busio
import time
import alarm.time
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)

alarm.light_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1000))