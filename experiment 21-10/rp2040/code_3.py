import board
from digitalio import DigitalInOut, Direction, Pull
from boardLogger import BoardLogger

logger = BoardLogger()


switch = DigitalInOut(board.D6)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

while True:
    v = switch.value