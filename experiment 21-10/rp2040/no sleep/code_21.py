import board
import busio
from adafruit_ds3231 import DS3231

i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

while True:
    pass