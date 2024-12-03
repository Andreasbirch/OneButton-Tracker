import alarm
import alarm.pin
import alarm.time
import time
import board
from digitalio import DigitalInOut, Direction, Pull

class Trigger:
    # class TIME:
    #     def __init__(self, seconds=None):
    #         self.seconds = seconds
    #     def __call__(self, seconds):
    #         return Trigger.TIME(seconds)
    TILT_UP: 1
    TILT_FORWARD: 2

TILT_UP_PIN = board.D10,
WAKE_PIN = board.A0
TILT_FORWARD_PIN = board.D11
# TILT_FORWARD_WAKE = board.D11

# class TiltTrigger:
#     def __init__(self, tilt_pin, wake_pin):
#         self.tilt_pin = tilt_pin
#         self.wake_pin = wake_pin
# class TimeTrigger:
#     def __init__(self, seconds):
#         self.seconds = seconds


class AlarmHelper():
    alarms = []
    def __init__(self, *triggers):
        for trigger in triggers:
            if trigger == Trigger.TIME:
                self.alarms.append(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + trigger.seconds))
            elif trigger == Trigger.TILT_UP:
                self.alarms.append(alarm.pin.PinAlarm(TILT_UP_WAKE, value=not TILT_UP_PIN.value, pull=False))
    def deep_sleep(self):
        alarm.exit_and_deep_sleep_until_alarms(self.alarms)
    def wake_source():
        wake_alarm = alarm.wake_alarm
        if wake_alarm == None:
            return None
        if isinstance(alarm.wake_alarm, alarm.time.TimeAlarm):
            return Trigger.TIME
        if isinstance(alarm.wake_alarm, alarm.pin.PinAlarm):
            return Trigger.TILT_UP if wake_alarm.pin == TILT_UP_PIN else Trigger.TILT_FORWARD 



