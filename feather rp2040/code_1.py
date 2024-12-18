# import board
# import time
# from digitalio import DigitalInOut, Direction, Pull
# import alarm

# horizontal_tilt = DigitalInOut(board.D13)
# horizontal_tilt.direction = Direction.INPUT
# horizontal_tilt.pull = Pull.UP

# vertical_tilt = DigitalInOut(board.D12)
# vertical_tilt.direction = Direction.INPUT
# vertical_tilt.pull = Pull.UP

# horizontal_pin = board.A2
# vertical_pin = board.A3

# # while True:
# #     print(horizontal_tilt.value, vertical_tilt.value, horizontal_pin.value, vertical_pin.value)
# #     horizontal_tilt_value = horizontal_tilt.value
# #     horizontal_pin_value = horizontal_pin.value

# #     vertical_tilt_value = vertical_tilt.value
# #     vertical_pin_value = vertical_pin.value

# #     if horizontal_tilt_value != (horizontal_pin_value > 5000): ## Tilt switch and pin are disagreeing
# #         print("Horizontal error")
# #     if vertical_tilt_value != (vertical_pin_value > 5000): ## Tilt switch and pin are disagreeing
# #         print("Vertical error")
    
# #     print("Tilted {} and {}".format("right" if horizontal_tilt_value else "left", "backward" if vertical_tilt_value else "forward"))
# #     time.sleep(.5)
# wake = alarm.wake_alarm
# print("Woke up")

# if wake == None:
#     print("First run, trigger when pin is {}".format(False))
#     horizontal_alarm = alarm.pin.PinAlarm(horizontal_pin, value=False, pull=True)
#     vertical_alarm = alarm.pin.PinAlarm(vertical_pin, value=False, pull=True)
#     alarm.exit_and_deep_sleep_until_alarms(horizontal_alarm, vertical_alarm)
# else:
#     print("Woke up from {}".format(wake.pin))
#     # print("Alarm was triggered with a value {}".format(wake_value))
#     if horizontal_tilt.value and vertical_tilt.value:
#         print("I was triggered by lifting the button up ")
#         horizontal_alarm = alarm.pin.PinAlarm(horizontal_pin, value=False, pull=True) # Koden looper når knappen er holdt nede
#         vertical_alarm = alarm.pin.PinAlarm(vertical_pin, value=False, pull=True) # Koden looper når knappen er holdt nede
#     elif horizontal_tilt.value:
#         horizontal_alarm = alarm.pin.PinAlarm(horizontal_pin, value=False, pull=True) # Koden looper når knappen er holdt nede
#         vertical_alarm = alarm.pin.PinAlarm(vertical_pin, value=True)# Koden looper når knappen ikke er holdt nede
#     elif vertical_tilt.value:
#         vertical_alarm = alarm.pin.PinAlarm(vertical_pin, value=False, pull=True) # Koden looper når knappen er holdt nede
#         horizontal_alarm = alarm.pin.PinAlarm(horizontal_pin, value=True)# Koden looper når knappen ikke er holdt nede
#     else: 
#         print("I was triggered by pushing the button down")
#         horizontal_alarm = alarm.pin.PinAlarm(horizontal_pin, value=True)# Koden looper når knappen ikke er holdt nede
#         vertical_alarm = alarm.pin.PinAlarm(vertical_pin, value=True)# Koden looper når knappen ikke er holdt nede
#     # print("New alarm is triggered when pin value is {}".format(wake_alarm.value))
#     time.sleep(.2)
#     alarm.exit_and_deep_sleep_until_alarms(horizontal_alarm, vertical_alarm)


# Kode med wake pins
# import board
# import alarm
# from digitalio import DigitalInOut, Direction, Pull
# import time

# X_PIN = board.A2

# x_tilt = DigitalInOut(board.D13)
# x_tilt.direction = Direction.INPUT
# x_tilt.pull = Pull.UP


# wake = alarm.wake_alarm
# print("Woke up")

# if wake == None:
#     print("First run, trigger when pin is {}".format(False))
#     wake_alarm = alarm.pin.PinAlarm(X_PIN, value=False, pull=True)
#     alarm.exit_and_deep_sleep_until_alarms(wake_alarm)
# else:
#     wake_value = x_tilt.value
#     # print("Alarm was triggered with a value {}".format(wake_value))
#     if wake_value:
#         print("I was triggered by lifting the button up ")
#         wake_alarm = alarm.pin.PinAlarm(X_PIN, value=False, pull=True) # Koden looper når knappen er holdt nede
#     else: 
#         print("I was triggered by pushing the button down")
#         wake_alarm = alarm.pin.PinAlarm(X_PIN, value=True)# Koden looper når knappen ikke er holdt nede
#     # print("New alarm is triggered when pin value is {}".format(wake_alarm.value))
#     time.sleep(.2)
#     alarm.exit_and_deep_sleep_until_alarms(wake_alarm)


import AlarmHelper
import time
import alarm


# import analogio
# import board
# pin_x = analogio.AnalogIn(AlarmHelper.PIN_X)
# pin_y = analogio.AnalogIn(AlarmHelper.PIN_Y)
# while True:
#     time.sleep(.1)
#     print(pin_x.value, pin_y.value)


while True:
    time.sleep(.5)
    alarms = AlarmHelper.GetNextAlarms()
    print()
    if isinstance(alarms, tuple):
        alarm.exit_and_deep_sleep_until_alarms(alarms[0],alarms[1])
    else:
        alarm.exit_and_deep_sleep_until_alarms(alarms)