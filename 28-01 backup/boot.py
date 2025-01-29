import board
import storage
from os import stat
from analogio import AnalogIn

usb_voltage = AnalogIn(board.A1)

# Terminate the program if we're too close to full storage space
try:
    if stat("/data")[6] > 7_000_000:
        exit()
except OSError:
    pass
 
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

voltage_reading = get_voltage(usb_voltage)

board_control = voltage_reading < 2 # voltage reading won't be completely zero due to interference

# If the switch pin is not connected to ground CircuitPython can write to the drive
storage.remount("/", readonly=(not board_control))