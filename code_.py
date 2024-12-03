import board
import boardLogger
from adafruit_ds3231 import DS3231
from adafruit_bno08x.i2c import BNO08X_I2C
import busio
import time
import math
from alarmhelper import Trigger, AlarmHelper
i2c = busio.I2C(board.SCL, board.SDA, frequency=40000)
# TILT_UP = board.D10
# TILT_FORWARD = board.D9
# WAKEPIN = board.A0
 
# button = DigitalInOut(TILT_UP)
# button.direction = Direction.INPUT
# button.pull = Pull.UP
 
# alarm.sleep_memory[0] = (alarm.sleep_memory[0] + 1) % 254
# print(alarm.sleep_memory[0], button.value)

# # Create an alarm that will trigger if button on pin IO9 is pressed.
# pin_alarm = alarm.pin.PinAlarm(pin=WAKEPIN, value=not button.value, pull=False)
 
# # Light sleep until one of the defined alarms wake us
# reason = alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
def std_dev(arr):
    mean = sum(arr) / len(arr)
    var  = sum(pow(x-mean,2) for x in arr) / len(arr)  # variance
    return mean, math.sqrt(var)

logger = boardLogger()

rtc = DS3231(i2c)
bno = BNO08X_I2C(i2c)

wake_source = AlarmHelper.wake_source()
log_obj = [rtc.datetime, wake_source]

print(wake_source)
alarm = AlarmHelper(Trigger.TILT_FORWARD, Trigger.TILT_UP, Trigger.TIME(10))
alarm.deep_sleep()

# if wake_source == Trigger.TIME:
#     snapshot = []
#     for i in range(100):
#         x, y, z = bno.acceleration
#         snapshot.append(math.sqrt(x**2 + y**2 + z**2)) ## Acceleration magnitude
#         time.sleep(.1)
#     mean, sd = std_dev(snapshot)
#     log_obj.append(mean, sd)
#     ## Skal der ændres i alarmerne alt efter hvor meget bevægelse der har været?
#     sleep_time = 10 * 60 if sd > .5 else 60
#     alarm = AlarmHelper(Trigger.TILT_FORWARD, Trigger.TILT_UP, Trigger.TIME(sleep_time))
# else:
#     ## Wake up and sample a snapshot
#     log_obj.append(['',''])
#     alarm = AlarmHelper(Trigger.TIME(10 * 60)) # If we woke from a tilt switch, we can wait atleast 10 minutes before we have to check again
#     ### todo: lav boardlogger om så log tager alle properties som argument. Er kun nødvendigt for fileloggeren, da kolonner skal matche header der
#     # logger.log([
#     #     time.mktime(rtc.datetime), # Unix epoch
#     #     alarm.wake_source()
#     # ])

## Sleep
logger.log(log_obj)
alarm.deep_sleep()