import AlarmHelper
import time
import alarm

while True:
    alarm_x, alarm_y = AlarmHelper.GetNextAlarms()
    time.sleep(.5)
    alarm.exit_and_deep_sleep_until_alarms(alarm_x, alarm_y)