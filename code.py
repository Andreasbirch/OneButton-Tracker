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

tilt_switch = DigitalInOut(board.D5)
tilt_switch.direction = Direction.INPUT
tilt_switch.pull = Pull.UP

tilt_switch_state = tilt_switch.value

sleep_time = 0.1

def get_datetime():
    timestamp = rtc.datetime
    return datetime(year=timestamp.tm_year, month=timestamp.tm_mon, day=timestamp.tm_mday, hour=timestamp.tm_hour, minute=timestamp.tm_min, second=timestamp.tm_sec)

if board_control:
    with open("/data_horizontal_fast.csv", "a+") as fp:
        fp.write("timestamp,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,mag_x,mag_y,mag_z,quat_i,quat_j,quat_k,quat_real,switch_state,state_change\n")
        while True:
            time.sleep(sleep_time)
            timestamp = get_datetime()
            accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
            fp.write("%d,%0.6f,%0.6f,%0.6f," % (timestamp, accel_x, accel_y, accel_z))
            
            gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
            fp.write("%0.6f,%0.6f,%0.6f," % (gyro_x, gyro_y, gyro_z))

            mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
            fp.write("%0.6f,%0.6f,%0.6f," % (mag_x, mag_y, mag_z))

            quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
            fp.write("%0.6f,%0.6f,%0.6f,%0.6f," % (quat_i, quat_j, quat_k, quat_real))
            
            new_tilt_switch_state = tilt_switch.value
            state_change = new_tilt_switch_state != tilt_switch_state
            if(state_change):
                tilt_switch_state = new_tilt_switch_state
            fp.write("{0},{1}\n".format(tilt_switch_state, state_change))

            fp.flush()
else:
    while True:
        time.sleep(sleep_time)
        print("Time")
        print(get_datetime())
        print("Acceleration:")
        accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
        print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
        print("")

        print("Gyro:")
        gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
        print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
        print("")

        print("Magnetometer:")
        mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
        print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
        print("")

        print("Rotation Vector Quaternion:")
        quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
        print(
            "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
        )
        print("")

        print("Tilt-switch:")
        new_tilt_switch_state = tilt_switch.value
        state_change = new_tilt_switch_state != tilt_switch_state
        if(state_change):
            tilt_switch_state = new_tilt_switch_state
        print("State: {0} Change?: {1}".format(tilt_switch_state, state_change))