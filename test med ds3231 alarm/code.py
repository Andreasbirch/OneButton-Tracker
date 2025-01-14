# Kode med wake pins
import board
import alarm
import time
from adafruit_ds3231 import DS3231
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=40000)
rtc = DS3231(i2c)

print("Woke up")

rtc.alarm