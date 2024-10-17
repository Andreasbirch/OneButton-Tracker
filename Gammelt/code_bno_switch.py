# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import alarm.time
import board
import busio
import alarm
from adafruit_datetime import datetime
import adafruit_ds3231
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from adafruit_bno08x import (
    BNO_REPORT_ACTIVITY_CLASSIFIER,
    _FEATURE_ENABLE_TIMEOUT
)
from adafruit_bno08x.i2c import BNO08X_I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)
rtc = adafruit_ds3231.DS3231(i2c)

## Setup board write access
switch = DigitalInOut(board.A1)
board_control = not switch.value
print("Control of board is given to {}".format("board" if board_control else "computer"))

bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)

## Setup tilt switches
tilt_switch_upward = DigitalInOut(board.D5)
tilt_switch_upward.direction = Direction.INPUT
tilt_switch_upward.pull = Pull.UP

tilt_switch_forward = DigitalInOut(board.D6)
tilt_switch_forward.direction = Direction.INPUT
tilt_switch_forward.pull = Pull.UP

sleep_time = 10 ## Sleep time in seconds

## Alarms
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)
def get_datetime():
    timestamp = rtc.datetime
    return datetime(year=timestamp.tm_year, month=timestamp.tm_mon, day=timestamp.tm_mday, hour=timestamp.tm_hour, minute=timestamp.tm_min, second=timestamp.tm_sec)

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
def get_voltage():
    return (vbat_voltage.value * 3.3) / 65536 * 2

if board_control:
    with open("/data.csv", "a+") as fp:
        while True:
            fp.write("%s,%d,%s,%s,%.10f\n" % (get_datetime(), bno.activity_classification, tilt_switch_forward.value, tilt_switch_upward.value, get_voltage()))
            fp.flush()
            alarm.exit_and_deep_sleep_until_alarms(time_alarm)
else:
    while True:
        bno_on_off_switch.value = True # Turn on BNO For reading data
        time.sleep(0.5)
        print("%s,%d,%s,%s,%.10f\n" % (get_datetime(), bno.activity_classification, tilt_switch_forward.value, tilt_switch_upward.value, get_voltage()))
        alarm.exit_and_deep_sleep_until_alarms(time_alarm)