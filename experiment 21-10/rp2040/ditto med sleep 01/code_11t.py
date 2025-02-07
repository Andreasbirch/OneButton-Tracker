import board
import busio
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)


repeat_times = 10000
time_before = time.monotonic_ns()
for i in range(repeat_times):
    accel_x, accel_y, accel_z = bno.acceleration
time_after = time.monotonic_ns()
average_ms = (time_after - time_before) / 1_000_000 ## Difference from ns to ms
average_ms /= repeat_times ## Average
print(average_ms)