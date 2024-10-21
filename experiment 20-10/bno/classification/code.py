import board
import busio
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_ACTIVITY_CLASSIFIER
from logger import ConsoleLogger

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
logger = ConsoleLogger()

time.sleep(5)
while True:
    # accel_x, accel_y, accel_z = bno.acceleration
    clas = bno.activity_classification
    # logger.log("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    logger.log("Activity: " + clas['most_likely'])