import board
import busio
import time
from adafruit_ds3231 import DS3231
from boardLogger import BoardLogger

logger = BoardLogger()

i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

while True:
    dt = rtc.datetime
    # logger.log(str(dt))
    time.sleep(.1)