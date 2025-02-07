import alarm.time
import board
import busio
import time
import alarm, alarm.pin
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_ACTIVITY_CLASSIFIER, BNO_REPORT_STEP_COUNTER

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
bno.enable_feature(BNO_REPORT_STEP_COUNTER)


time_alarm = alarm.pin.PinAlarm(board.D6, value=True, pull=True)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)