import board
import busio
from adafruit_ds3231 import DS3231
from logger import ConsoleLogger

i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

logger = ConsoleLogger()

while True:
    logger.log(rtc)