import alarm
import board
import alarm.pin
import time
from digitalio import DigitalInOut, Direction, Pull

TILT_X = DigitalInOut(board.D13)
TILT_X.direction = Direction.INPUT
TILT_X.pull = Pull.UP

TILT_Y = DigitalInOut(board.D12)
TILT_Y.direction = Direction.INPUT
TILT_Y.pull = Pull.UP

PIN_X = board.A2
PIN_Y = board.A3

class Orientation:
    FORWARD = 0 #"FORWARD"
    RIGHT = 1 #"RIGHT"
    BACKWARDS = 2 #"BACKWARDS"
    LEFT = 3 #"LEFT"
    
    def toString(orientation):
        if orientation == Orientation.FORWARD:
            return "FORWARD"
        if orientation == Orientation.RIGHT:
            return "RIGHT"
        if orientation == Orientation.BACKWARDS:
            return "BACKWARDS"
        if orientation == Orientation.LEFT:
            return "LEFT"

def GetOrientation():
    orientation_x = Orientation.RIGHT if TILT_X.value else Orientation.LEFT
    orientation_y = Orientation.BACKWARDS if TILT_Y.value else Orientation.FORWARD
    return orientation_x, orientation_y

def GetAlarmFromOrientation(orientation):
    ## Gets the alarm that wakes the orientation up
    if orientation == Orientation.FORWARD:
        return alarm.pin.PinAlarm(PIN_Y, value=True, pull=True), Orientation.BACKWARDS
    if orientation == Orientation.RIGHT:
        return alarm.pin.PinAlarm(PIN_X, value=False, pull=True), Orientation.LEFT
    if orientation == Orientation.BACKWARDS:
        return alarm.pin.PinAlarm(PIN_Y, value=False, pull=True), Orientation.FORWARD
    if orientation == Orientation.LEFT:
        # TILT_X.pull = Pull.DOWN
        print(TILT_X.value)
        return alarm.pin.PinAlarm(PIN_X, value=True, pull=True), Orientation.RIGHT

def GetNextAlarms(prev_orientation_x, prev_orientation_y):
    print("Last device orientation: {} and {}".format(Orientation.toString(prev_orientation_x), Orientation.toString(prev_orientation_y)))
    
    orientation_x, orientation_y = GetOrientation()
    print("Current device orientation: {} and {}".format(Orientation.toString(orientation_x), Orientation.toString(orientation_y)))

    alarm_x = None
    alarm_y = None
    
    next_orientation_x = None
    next_orientation_y = None

    # Only update alarm if orientation has changed
    if orientation_x != prev_orientation_x:
        alarm_x, next_orientation_x = GetAlarmFromOrientation(orientation_x)
    else:
        alarm_x, next_orientation_x = GetAlarmFromOrientation(prev_orientation_x)

    if orientation_y != prev_orientation_y:
        alarm_y, next_orientation_y = GetAlarmFromOrientation(orientation_y)
    else:
        alarm_y, next_orientation_y = GetAlarmFromOrientation(prev_orientation_y)

    if alarm_x or alarm_y:
        print("Waking if tilted {} or {}".format(Orientation.toString(next_orientation_x), Orientation.toString(next_orientation_y)))
        return alarm_x, alarm_y, orientation_x, orientation_y
    
    # No change in orientation, so return None for alarms
    return None, None, prev_orientation_x, prev_orientation_y


prev_orientation_x = alarm.sleep_memory[0]
prev_orientation_y = alarm.sleep_memory[1]

while True:
    time.sleep(0.5)

    # Get the alarms and check if any orientation change occurred
    alarm_x, alarm_y, prev_orientation_x, prev_orientation_y = GetNextAlarms(prev_orientation_x, prev_orientation_y)
    alarm.sleep_memory[0] = prev_orientation_x
    alarm.sleep_memory[1] = prev_orientation_y
    
    if alarm_x or alarm_y:
        alarm.exit_and_deep_sleep_until_alarms(alarm_x, alarm_y)