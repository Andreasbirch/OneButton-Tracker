import board
import time
from digitalio import DigitalInOut, Direction, Pull

switch = DigitalInOut(board.D6)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

average_ms = 0
for i in range(100000):
    time_before = time.monotonic_ns()
    _ = switch.value
    time_after = time.monotonic_ns()
    average_ms += (time_after - time_before) / 1_000_000 # ns to ms, rounding

average_ms = average_ms/10000

print("Finished")
print(average_ms)