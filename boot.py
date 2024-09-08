"""CircuitPython Essentials Storage logging boot.py file"""
import storage
import board
from digitalio import DigitalInOut
switch = DigitalInOut(board.A1)

pc_control = switch.value
storage.remount("/", readonly=pc_control)