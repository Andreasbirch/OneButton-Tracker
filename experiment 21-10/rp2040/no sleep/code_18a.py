import board
import busio
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_STABILITY_CLASSIFIER
import alarm, alarm.time

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

alarm.light_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1000))