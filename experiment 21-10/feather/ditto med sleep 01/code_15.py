import board
import busio
import time
from adafruit_bno08x.i2c import BNO08X_I2C
from adafruit_bno08x import BNO_REPORT_STEP_COUNTER
from boardLogger import BoardLogger

logger = BoardLogger()

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_STEP_COUNTER)

while True:
    steps = bno.steps
    # logger.log(str(steps))
    time.sleep(.1)