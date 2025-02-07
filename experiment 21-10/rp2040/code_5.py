import time
import alarm, alarm.time
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 10)
alarm.light_sleep_until_alarms(time_alarm)