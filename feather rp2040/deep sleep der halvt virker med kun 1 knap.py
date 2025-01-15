# Kode med wake pins
# Det ser umiddelbart ud til at virke, men er til tider ustabilt
import alarm.pin
import board
import alarm
from digitalio import DigitalInOut, Direction, Pull

print("Woke up")
btn = DigitalInOut(board.D12)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

btn_val = btn.value
btn.deinit()
if not btn_val:
    print("Button is pressed")
    alarm.exit_and_deep_sleep_until_alarms(alarm.pin.PinAlarm(board.D12, value=True, pull=False, edge=True)) 
else: 
    print("Button is released")
    alarm.exit_and_deep_sleep_until_alarms(alarm.pin.PinAlarm(board.D12, value=False, pull=True, edge=True)) 