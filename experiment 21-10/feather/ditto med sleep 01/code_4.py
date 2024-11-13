import time
from boardLogger import BoardLogger

logger = BoardLogger()

while True:
    logger.log(
        "1.23456, 1.23456, 1.23456, 123, still"
    )
    time.sleep(.01)