## Code med to tilt switches
import alarm.time
import board
from digitalio import DigitalInOut, Direction, Pull
import alarm, alarm.pin
import time
from boardLogger import BoardLogger
from adafruit_ds3231 import DS3231
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_STABILITY_CLASSIFIER

import busio
import math
from analogio import AnalogIn

TILT_X_1 = DigitalInOut(board.D6)
TILT_X_1.direction = Direction.INPUT
TILT_X_1.pull = Pull.UP

TILT_X_2 = DigitalInOut(board.D13)
TILT_X_2.direction = Direction.INPUT
TILT_X_2.pull = Pull.UP

TILT_Y_1 = DigitalInOut(board.D5)
TILT_Y_1.direction = Direction.INPUT
TILT_Y_1.pull = Pull.UP

TILT_Y_2 = DigitalInOut(board.D9)
TILT_Y_2.direction = Direction.INPUT
TILT_Y_2.pull = Pull.UP

i2c = busio.I2C(board.SCL, board.SDA, frequency=40000)
rtc = DS3231(i2c)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

stability_enum = {
    'Unknown': 0,
    'On Table': 1,
    'Stationary': 2,
    'Stable': 3,
    'In motion': 4
}

logger = BoardLogger(headers=['timestamp', 'acc_magnitude', 'stability', 'tilt_x', 'tilt_y'])

data = []
x, y, z = bno.acceleration
acc_magnitude = round(math.sqrt(x**2 + y**2 + z**2), 3)
stability = stability_enum[bno.stability_classification]

timestamp = rtc.datetime
timestamp_unix = time.mktime(rtc.datetime)

data.append([
    timestamp_unix,
    acc_magnitude,
    stability,
    int(TILT_X_1.value),
    int(TILT_Y_1.value),
])

# Once an hour, log battery voltage
if alarm.sleep_memory[0]:
    if alarm.sleep_memory[0] != timestamp.tm_hour:
        alarm.sleep_memory[0] = timestamp.tm_hour  
        data.append([timestamp_unix, logger.get_voltage(AnalogIn(board.A1))])

logger.log_multirow(data)

x_alarm = None
y_alarm = None
wakealarm = alarm.wake_alarm
if isinstance(wakealarm, alarm.time.TimeAlarm):
    print("Woke from sleep")
    if TILT_X_1.value: # LEFT
        TILT_X_2.deinit()
        x_alarm = alarm.pin.PinAlarm(board.D13, value=False, pull=True, edge=True)
    else: # RIGHT
        TILT_X_1.deinit()
        x_alarm = alarm.pin.PinAlarm(board.D6, value=False, pull=True, edge=True)

    if TILT_Y_1.value: # FORWARD
        TILT_Y_2.deinit()
        y_alarm = alarm.pin.PinAlarm(board.D9, value=False, pull=True, edge=True)
    else: # BACKWARD
        TILT_Y_1.deinit()
        y_alarm = alarm.pin.PinAlarm(board.D5, value=False, pull=True, edge=True)
    time.sleep(.2)
    alarm.exit_and_deep_sleep_until_alarms(x_alarm, y_alarm)
else:
    print("Woke from movement")
    time.sleep(.2)
    alarm.exit_and_deep_sleep_until_alarms(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 5))