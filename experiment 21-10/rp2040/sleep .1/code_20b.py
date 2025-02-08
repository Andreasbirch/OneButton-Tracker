import board
import busio
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_STABILITY_CLASSIFIER, BNO_REPORT_ACCELEROMETER
from analogio import AnalogIn
from digitalio import DigitalInOut, Pull, Direction
import alarm, alarm.time

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)

tilt = AnalogIn(board.A1)
btn = DigitalInOut(board.D6)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

while True:
    stability = bno.stability_classification
    x, y, z = bno.acceleration
    try:
        tilt_val = tilt.value
    except:
        pass
    
    try:
        btn_val = btn.value
    except:
        pass
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1000)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)