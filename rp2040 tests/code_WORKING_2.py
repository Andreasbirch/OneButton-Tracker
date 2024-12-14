# Kode med wake pins
import board
import alarm
from digitalio import DigitalInOut, Direction, Pull
import time

LEFT_PIN = board.A0
RIGHT_PIN = board.A1

left_button = DigitalInOut(board.D3)
left_button.direction = Direction.INPUT
left_button.pull = Pull.UP

right_button = DigitalInOut(board.D4)
right_button.direction = Direction.INPUT
right_button.pull = Pull.UP

wake = alarm.wake_alarm
print("Woke up")

if wake == None:
    print("First run, trigger when pin is {}".format(False))
    left_alarm = alarm.pin.PinAlarm(LEFT_PIN, value=False, pull=True)
    right_alarm = alarm.pin.PinAlarm(RIGHT_PIN, value=False, pull=True)
    alarm.exit_and_deep_sleep_until_alarms(left_alarm, right_alarm)
else:
    print("Woke up from {}".format(wake.pin))
    # print("Alarm was triggered with a value {}".format(wake_value))
    if left_button.value and right_button.value:
        print("I was triggered by lifting the button up ")
        left_alarm = alarm.pin.PinAlarm(LEFT_PIN, value=False, pull=True) # Koden looper når knappen er holdt nede
        right_alarm = alarm.pin.PinAlarm(RIGHT_PIN, value=False, pull=True) # Koden looper når knappen er holdt nede
    elif left_button.value:
        left_alarm = alarm.pin.PinAlarm(LEFT_PIN, value=False, pull=True) # Koden looper når knappen er holdt nede
        right_alarm = alarm.pin.PinAlarm(RIGHT_PIN, value=True)# Koden looper når knappen ikke er holdt nede
    elif right_button.value:
        right_alarm = alarm.pin.PinAlarm(RIGHT_PIN, value=False, pull=True) # Koden looper når knappen er holdt nede
        left_alarm = alarm.pin.PinAlarm(LEFT_PIN, value=True)# Koden looper når knappen ikke er holdt nede
    else: 
        print("I was triggered by pushing the button down")
        left_alarm = alarm.pin.PinAlarm(LEFT_PIN, value=True)# Koden looper når knappen ikke er holdt nede
        right_alarm = alarm.pin.PinAlarm(RIGHT_PIN, value=True)# Koden looper når knappen ikke er holdt nede
    # print("New alarm is triggered when pin value is {}".format(wake_alarm.value))
    time.sleep(.2)
    alarm.exit_and_deep_sleep_until_alarms(left_alarm, right_alarm) 