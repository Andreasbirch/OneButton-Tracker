# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
from adafruit_datetime import datetime
import adafruit_ds3231
from digitalio import DigitalInOut, Direction, Pull
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
    BNO_REPORT_STEP_COUNTER
)
from adafruit_bno08x.i2c import BNO08X_I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)
rtc = adafruit_ds3231.DS3231(i2c)

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

switch = DigitalInOut(board.A1)
board_control = not switch.value
print("Control of board is given to {}".format("board" if board_control else "computer"))

tilt_switch_upward = DigitalInOut(board.D5)
tilt_switch_upward.direction = Direction.INPUT
tilt_switch_upward.pull = Pull.UP

tilt_switch_forward = DigitalInOut(board.D6)
tilt_switch_forward.direction = Direction.INPUT
tilt_switch_forward.pull = Pull.UP

tilt_switch_upward_state = tilt_switch_upward.value
tilt_switch_forward_state = tilt_switch_forward.value

sleep_time = 0.1

def get_datetime():
    timestamp = rtc.datetime
    return datetime(year=timestamp.tm_year, month=timestamp.tm_mon, day=timestamp.tm_mday, hour=timestamp.tm_hour, minute=timestamp.tm_min, second=timestamp.tm_sec)
bno.enable_feature(BNO_REPORT_STEP_COUNTER)
if board_control:
    with open("/data.csv", "a+") as fp:
        fp.write("timestamp,bno_steps,forward_state_change,upward_state_change\n")
        while True:
            time.sleep(sleep_time)
            timestamp = get_datetime()

            #Check for state changes and update accordingly
            upward_state_change = tilt_switch_upward.value != tilt_switch_upward_state
            if upward_state_change:
                tilt_switch_upward_state = tilt_switch_upward.value

            forward_state_change = tilt_switch_forward.value != tilt_switch_forward_state
            if forward_state_change:
                tilt_switch_forward_state = tilt_switch_forward.value

            fp.write("%s,%d,%s,%s\n" % (timestamp, bno.steps, upward_state_change, forward_state_change))
            fp.flush()
else:
    while True:
        time.sleep(sleep_time)
        timestamp = get_datetime()

        #Check for state changes and update accordingly
        upward_state_change = tilt_switch_upward.value != tilt_switch_upward_state
        if upward_state_change:
            tilt_switch_upward_state = tilt_switch_upward.value

        forward_state_change = tilt_switch_forward.value != tilt_switch_forward_state
        if forward_state_change:
            tilt_switch_forward_state = tilt_switch_forward.value

        print("%s,%d,%s,%s" % (timestamp, bno.steps, upward_state_change, forward_state_change))