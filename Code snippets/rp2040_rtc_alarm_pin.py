import board
import time
import alarm.pin
from adafruit_ds3231 import DS3231
i2c = board.I2C()
rtc = DS3231(i2c)

print(rtc.datetime)
rtc.alarm1_interrupt = True

if rtc.alarm1_status:
    print("Alarm!")
    rtc.alarm1_status = False
dt = rtc.datetime
rtc.alarm1 = (time.struct_time((dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, 0, 0, 0, -1, -1)), "hourly") # Wakes up once on the hour

alrm = alarm.pin.PinAlarm(board.D10, value=False, pull=True, edge=True)
alarm.exit_and_deep_sleep_until_alarms(alrm)