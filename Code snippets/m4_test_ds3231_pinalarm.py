#Test ds3231 alarm
import alarm.time
import time
import alarm
import alarm.pin
import busio
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_ds3231 import DS3231
i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)
dt = rtc.datetime
# Ser ud til at virke på while true, så den skal nok mappes op mod en digital pin på rp2040'eren
print("Woke up {}:{}:{}".format(dt.tm_hour, dt.tm_min, dt.tm_sec))
rtc.alarm1 = (time.struct_time((2017, 1, 1, 12, 10, 0, 0, -1, -1)), "hourly")
rtc.alarm1_interrupt = True
# if not rtc.alarm1:
#     rtc.alarm1 = (time.struct_time((dt.tm_year, dt.tm_mon, dt.tm_mday, 11, 34, 0, 6, 1, -1)), "minutely")

# while(True):
#     print("{} on {}:{}:{}".format(rtc.alarm1[1], rtc.alarm1[0].tm_hour, rtc.alarm1[0].tm_min, rtc.alarm1[0].tm_sec))
#     print(rtc.alarm1_status)
#     print(pin.value)
#     if rtc.alarm1_status:
#         rtc.alarm1_status = False
#     print()
#     time.sleep(1)

if rtc.alarm1_status:
    print("Alarm went off!")
    rtc.alarm1_status = False
    time.sleep(1)

print(rtc.alarm1)
print(rtc.alarm1_status)
alarm.exit_and_deep_sleep_until_alarms(alarm.pin.PinAlarm(board.A0, value=False, pull=True, edge=True))
