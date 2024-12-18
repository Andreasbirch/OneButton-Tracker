import alarm
import board
import alarm.pin
import time
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn



# TILT_Y = DigitalInOut(board.D12)
# TILT_Y.direction = Direction.INPUT
# TILT_Y.pull = Pull.UP

# PIN_X = board.A2
# PIN_Y = board.A3
TILT_X = DigitalInOut(board.D13)
TILT_X.direction = Direction.INPUT
TILT_X.pull = Pull.UP


print(TILT_X.value)
alrm = alarm.pin.PinAlarm(board.A3, value=False, pull=True)

PIN_X = AnalogIn(board.A3)
print(AnalogIn(board.A2).value)
time.sleep(.1)
alarm.exit_and_deep_sleep_until_alarms(alrm)