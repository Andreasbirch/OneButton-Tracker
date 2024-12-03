import board
import time
import busio
from boardLogger import BoardLogger
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_STABILITY_CLASSIFIER
from adafruit_ds3231 import DS3231
from digitalio import DigitalInOut, Direction, Pull
i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
rtc = DS3231(i2c)

stability_enum = {
    'Unknown': 0,
    'On Table': 1,
    'Stationary': 2,
    'Stable': 3,
    'In motion': 4
}

logger = BoardLogger(headers=['timestamp', 'acc_x', 'acc_y', 'acc_z', 'stability', 'tilt_up', 'tilt_forward'])

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

switch_UP = DigitalInOut(board.D6)
switch_UP.direction = Direction.INPUT
switch_UP.pull = Pull.UP

switch_FORWARD = DigitalInOut(board.D5)
switch_FORWARD.direction = Direction.INPUT
switch_FORWARD.pull = Pull.UP

#NB - ikke indstillet til vintertid, dvs. tiden svarer til GMT
while(True):
    rows = []
    for i in range(10):
        acc_x, acc_y, acc_z = bno.acceleration
        stability = stability_enum[bno.stability_classification]
        rows.append(
        [
            time.mktime(rtc.datetime),
            round(acc_x,3),
            round(acc_y,3),
            round(acc_z,3),
            stability,
            int(switch_UP.value),
            int(switch_FORWARD.value)
        ])
        time.sleep(1)
    logger.log_multirow(rows)