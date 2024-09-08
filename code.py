import board
import digitalio
import time

sensor = digitalio.DigitalInOut(board.D5)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

current_val = True

while True:
    if sensor.value != current_val:
        print("State change")
        current_val = sensor.value
    led.value = sensor.value
    time.sleep(0.1)