import time
import board
import busio
from adafruit_datetime import datetime
import adafruit_ds3231
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from adafruit_bno08x import (
    BNO_REPORT_ACTIVITY_CLASSIFIER,
    BNO_REPORT_STEP_COUNTER,
    BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
    BNO_REPORT_STABILITY_CLASSIFIER,
    BNO_REPORT_SHAKE_DETECTOR,
    BNO_REPORT_ACCELEROMETER
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
bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)
bno.enable_feature(BNO_REPORT_SHAKE_DETECTOR)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)

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

def format_line(*args):
    line = []
    for arg in args:
        if isinstance(arg, datetime):
            line.append("%s" % arg)
        elif isinstance(arg, float):
            line.append("%.5f" % arg)
        elif isinstance(arg, int):
            line.append("%d" % arg)
        else:
            line.append(str(arg))

    return ','.join(line)

if board_control:
    with open("/data.csv", "a+") as fp:
        while True:
            q_x, q_y, q_z, q_w = bno.geomagnetic_quaternion
            a_x, a_y, a_z = bno.acceleration
            fp.write(format_line(get_datetime(), 
                            bno.activity_classification, 
                            bno.stability_classification,
                            bno.shake,
                            bno.steps,
                            q_x,
                            q_y,
                            q_z,
                            q_w,
                            a_x,
                            a_y,
                            a_z,
                            tilt_switch_forward.value, 
                            tilt_switch_upward.value, 
                            get_voltage(vbat_voltage), 
                            get_voltage(usb_voltage)) + "\n")
            fp.flush()
            time.sleep(sleep_time)
else:
    while True:
        q_x, q_y, q_z, q_w = bno.geomagnetic_quaternion
        a_x, a_y, a_z = bno.acceleration
        print(format_line(get_datetime(), 
                            bno.activity_classification, 
                            bno.stability_classification,
                            bno.shake,
                            bno.steps,
                            q_x,
                            q_y,
                            q_z,
                            q_w,
                            a_x,
                            a_y,
                            a_z,
                            tilt_switch_forward.value, 
                            tilt_switch_upward.value, 
                            get_voltage(vbat_voltage), 
                            get_voltage(usb_voltage)))
        time.sleep(sleep_time)