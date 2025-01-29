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
from analogio import AnalogIn
from os import stat

# Terminate the program if we're too close to full storage space
try:
    if stat("/data")[6] > 7_000_000:
        exit()
except OSError:
    pass

rtc_alarm = alarm.pin.PinAlarm(board.D10, value=False, pull=True, edge=True)

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

BUTTON = DigitalInOut(board.D12)
BUTTON.direction = Direction.INPUT
BUTTON.pull = Pull.UP

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

logger = BoardLogger(headers=['timestamp', 'acc_x', 'acc_y', 'acc_z', 'stability', 'tilt_x', 'tilt_y', 'button'])

data = []
timestamp = None
for take in range(2):
    for i in range(5): # Take 5 samples
        x, y, z = bno.acceleration
        stability = stability_enum[bno.stability_classification]

        timestamp = rtc.datetime
        timestamp_unix = time.mktime(rtc.datetime)

        data.append([
            timestamp_unix,
            round(x, 2),
            round(y, 2),
            round(z, 2),
            stability,
            int(TILT_X_1.value),
            int(TILT_Y_1.value),
            int(not BUTTON.value)
        ])
        time.sleep(.1)
    time.sleep(60) # Now sleep for a minute, then sample again


## DS3231 section
battery_alarm = rtc.alarm2_status

# If alarm 2 is alarming, we log battery
if battery_alarm:
    rtc.alarm2 = (time.struct_time(2017, 1, 1, 12, timestamp.tm_min + 30, 0, 0, -1, -1), "hourly")
    rtc.alarm2_interrupt = True
    rtc.alarm2_status = False
    data.append([(AnalogIn(board.A2).value * 3.3) / 65536 * 2])
## End DS3231 section


logger.log_multirow(data)


## Set next alarms and go to sleep
x_alarm = None
y_alarm = None
wakealarm = alarm.wake_alarm
BUTTON.deinit()
button_alarm = alarm.pin.PinAlarm(board.D12, value=False, pull=True, edge=False)
if rtc.alarm1_status:
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

    # Set alarm
    rtc.alarm1_interrupt = False
    rtc.alarm1_status = False

    alarm.exit_and_deep_sleep_until_alarms(rtc_alarm, x_alarm, y_alarm, button_alarm)
else:
    # Set timer 1 minute ahead
    rtc.alarm1 = (time.struct_time((2017, 1, 1, 12, timestamp.tm_hour, timestamp.tm_min + 1, timestamp.tm_sec, -1, -1)), "minutely")
    rtc.alarm1_interrupt = True
    rtc.alarm1_status = True
    alarm.exit_and_deep_sleep_until_alarms(rtc_alarm, button_alarm)