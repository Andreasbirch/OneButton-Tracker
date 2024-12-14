# Kode med wake pins
import board
import alarm
from digitalio import DigitalInOut, Direction, Pull
import time

WAKE_PIN = board.A0

button = DigitalInOut(board.D3)
button.direction = Direction.INPUT
button.pull = Pull.UP


wake = alarm.wake_alarm
print("Woke up")

if wake == None:
    print("First run, trigger when pin is {}".format(False))
    wake_alarm = alarm.pin.PinAlarm(WAKE_PIN, value=False, pull=True)
    alarm.exit_and_deep_sleep_until_alarms(wake_alarm)
else:
    wake_value = button.value
    # print("Alarm was triggered with a value {}".format(wake_value))
    if wake_value:
        print("I was triggered by lifting the button up ")
        wake_alarm = alarm.pin.PinAlarm(WAKE_PIN, value=False, pull=True) # Koden looper når knappen er holdt nede
    else: 
        print("I was triggered by pushing the button down")
        wake_alarm = alarm.pin.PinAlarm(WAKE_PIN, value=True)# Koden looper når knappen ikke er holdt nede
    # print("New alarm is triggered when pin value is {}".format(wake_alarm.value))
    time.sleep(.2)
    alarm.exit_and_deep_sleep_until_alarms(wake_alarm)