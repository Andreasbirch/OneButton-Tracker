import board
import busio
import time
from adafruit_ds3231 import DS3231

i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

repeat_times = 10000
time_before = time.monotonic_ns()
for i in range(repeat_times):
    dt = rtc.datetime
time_after = time.monotonic_ns()

average_ms = (time_after - time_before) / 1_000_000 ## Difference from ns to ms
average_ms /= repeat_times ## Average
print(average_ms)