import alarm.time
import board
import alarm, alarm.pin
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
    FORWARD = "FORWARD"
    RIGHT = "RIGHT"
    BACKWARDS = "BACKWARDS"
    LEFT = "LEFT"


def GetOrientaion():
    tilt_readings = {'x': TILT_X.value, 'y': TILT_Y.value}
    orientation_x = Orientation.RIGHT if tilt_readings['x'] else Orientation.LEFT
    orientation_y = Orientation.BACKWARDS if tilt_readings['y'] else Orientation.FORWARD
    return orientation_x, orientation_y

def GetNextAlarms():
    orientation_x, orientation_y = GetOrientaion()
    print("Device is pointing {} and {}".format(orientation_x, orientation_y))
    
    if orientation_x == Orientation.LEFT:
        alarm_x = alarm.pin.PinAlarm(PIN_X, value=True, pull=True)
        wake_diretion_x = Orientation.RIGHT
    if orientation_x == Orientation.RIGHT:
        alarm_x = alarm.pin.PinAlarm(PIN_X, value=False, pull=True)
        wake_diretion_x = Orientation.LEFT
    
    if orientation_y == Orientation.FORWARD:
        alarm_y = alarm.pin.PinAlarm(PIN_Y, value=True, pull=True)
        wake_diretion_y = Orientation.BACKWARDS
    if orientation_y == Orientation.BACKWARDS:
        alarm_y = alarm.pin.PinAlarm(PIN_Y, value=False, pull=True)
        wake_diretion_y = Orientation.FORWARD
    print("Waking if tilted {} or {}".format(wake_diretion_x, wake_diretion_y))
    return alarm_x, alarm_y
    # else:
    #     return alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1)
    
