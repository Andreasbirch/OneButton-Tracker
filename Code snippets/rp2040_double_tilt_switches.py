## Code with two tilt switches in each direction
import alarm.time
import board
from digitalio import DigitalInOut, Direction, Pull
import alarm, alarm.pin
import time

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
time.sleep(.5)
alarm.exit_and_deep_sleep_until_alarms(x_alarm, y_alarm)