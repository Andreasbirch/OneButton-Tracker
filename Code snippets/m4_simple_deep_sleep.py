# Simple example with deep sleep on an analog wake pin, and a button
import board
import alarm
from digitalio import DigitalInOut, Direction, Pull

button = DigitalInOut(board.D9)
button.direction = Direction.INPUT
button.pull = Pull.UP

wake_pin = board.A0

print("Woke up")
alarm.exit_and_deep_sleep_until_alarms(alarm.pin.PinAlarm(wake_pin, value=not button.value, pull=True, edge=True))