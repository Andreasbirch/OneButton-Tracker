import board
import alarm
from digitalio import DigitalInOut, Direction, Pull


TILT_UP = board.D10
TILT_FORWARD = board.D9
WAKE_UP = board.A0
WAKE_FORWARD = board.A1
 
button_up = DigitalInOut(TILT_UP)
button_up.direction = Direction.INPUT
button_up.pull = Pull.UP
 
button_forward = DigitalInOut(TILT_FORWARD)
button_forward.direction = Direction.INPUT
button_forward.pull = Pull.UP

wake = alarm.wake_alarm.pin
print(wake if wake is not None else "")

# Create an alarm that will trigger if button on pin IO9 is pressed.
pin_up_alarm = alarm.pin.PinAlarm(pin=WAKE_UP, value=not button_up.value, pull=False)
pin_forward_alarm = alarm.pin.PinAlarm(pin=WAKE_FORWARD, value=not button_forward.value, pull=False)

# Light sleep until one of the defined alarms wake us
reason = alarm.exit_and_deep_sleep_until_alarms(pin_up_alarm, pin_forward_alarm)