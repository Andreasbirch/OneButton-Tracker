## This can all be pasted into the repl terminal
import board
import time
import busio
import adafruit_ds3231

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
rtc = adafruit_ds3231.DS3231(i2c)
## Year, Month, Day, Hour, Minute, Second, 0, -1, -1
rtc.datetime = time.struct_time((2024,10,10,0,18,30,0,-1,-1))