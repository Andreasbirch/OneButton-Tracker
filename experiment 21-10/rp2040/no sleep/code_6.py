import time
import alarm

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 1000) ## Deep sleep 1000 seconds
alarm.exit_and_deep_sleep_until_alarms(time_alarm)