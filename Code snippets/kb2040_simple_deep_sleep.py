# Simple example with deep sleep on an analog pin
import board
import alarm

print("Woke up")
alarm.exit_and_deep_sleep_until_alarms(alarm.pin.PinAlarm(board.D9, value=False, pull=True, edge=True))