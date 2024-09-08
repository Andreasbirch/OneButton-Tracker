"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D5)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

board_control = not switch.value

# If the switch pin is not connected to ground CircuitPython can write to the drive
storage.remount("/", readonly=board_control)
print("Control of board is given to {}".format("board" if board_control else "computer"))
