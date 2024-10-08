# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
# import alarm.time
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
    BNO_REPORT_STEP_COUNTER,
    BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR
)
from adafruit_bno08x.i2c import BNO08X_I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)
rtc = adafruit_ds3231.DS3231(i2c)

## Setup voltage reader
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

## Setup board write access
usb_voltage = AnalogIn(board.A1)
board_control = get_voltage(usb_voltage) < 2
print("Control of board is given to {}".format("board" if board_control else "computer"))

bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
bno.enable_feature(BNO_REPORT_STEP_COUNTER)
bno.enable_feature(BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)

## Setup tilt switches
tilt_switch_upward = DigitalInOut(board.D5)
tilt_switch_upward.direction = Direction.INPUT
tilt_switch_upward.pull = Pull.UP

tilt_switch_forward = DigitalInOut(board.D6)
tilt_switch_forward.direction = Direction.INPUT
tilt_switch_forward.pull = Pull.UP

sleep_time = 1 ## Sleep time in seconds

# ## Alarms
# time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)

def get_datetime():
    timestamp = rtc.datetime
    return datetime(year=timestamp.tm_year, month=timestamp.tm_mon, day=timestamp.tm_mday, hour=timestamp.tm_hour, minute=timestamp.tm_min, second=timestamp.tm_sec)

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

if board_control:
    with open("/data.csv", "a+") as fp:
        while True:
            q_x, q_y, q_z, q_w = bno.geomagnetic_quaternion
            fp.write("%s,%s,%s,%f,%f,%f,%f,%s,%s,%.5f,%.5f\n" % (get_datetime(), 
                                              bno.activity_classification['most_likely'], 
                                              bno.steps,
                                              q_x,
                                              q_y,
                                              q_z,
                                              q_w,
                                              tilt_switch_forward.value, 
                                              tilt_switch_upward.value, 
                                              get_voltage(vbat_voltage), 
                                              get_voltage(usb_voltage)))
            fp.flush()
            time.sleep(sleep_time)
else:
    while True:
        q_x, q_y, q_z, q_w = bno.geomagnetic_quaternion
        print("%s,%s,%s,%f,%f,%f,%f,%s,%s,%.5f,%.5f\n" % (get_datetime(), 
                                              bno.activity_classification['most_likely'], 
                                              bno.steps,
                                              q_x,
                                              q_y,
                                              q_z,
                                              q_w,
                                              tilt_switch_forward.value, 
                                              tilt_switch_upward.value, 
                                              get_voltage(vbat_voltage), 
                                              get_voltage(usb_voltage)))
        time.sleep(sleep_time)