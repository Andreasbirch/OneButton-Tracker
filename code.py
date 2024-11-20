import board
from digitalio import DigitalInOut, Direction, Pull
import alarm.pin

BUTTON = board.D9
WAKEPIN = board.A0
 
button = DigitalInOut(BUTTON)
button.direction = Direction.INPUT
button.pull = Pull.UP
 
alarm.sleep_memory[0] = (alarm.sleep_memory[0] + 1) % 254
print(alarm.sleep_memory[0], button.value, alarm.wake_alarm.value)

# Create an alarm that will trigger if button on pin IO9 is pressed.
pin_alarm = alarm.pin.PinAlarm(pin=WAKEPIN, value=not button.value, pull=False)
 
# Light sleep until one of the defined alarms wake us
reason = alarm.exit_and_deep_sleep_until_alarms(pin_alarm)