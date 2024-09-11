import alarm.time
import alarm.pin
import alarm.touch
import board
import alarm
import time

print("Waking")
tilt_switch_alarm = alarm.pin.PinAlarm(board.A0, value=True, edge=True, pull=True)
# tilt_switch_alarm = alarm.touch.TouchAlarm(pin=board.A3)
print(alarm.wake_alarm)
alarm.exit_and_deep_sleep_until_alarms(tilt_switch_alarm)