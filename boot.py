import board
import storage
from analogio import AnalogIn

usb_voltage = AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

voltage_reading = get_voltage(usb_voltage)
print(voltage_reading > 3)

board_control = voltage_reading < 2 # voltage reading won't be completely zero due to interference

# If the switch pin is not connected to ground CircuitPython can write to the drive
storage.remount("/", readonly=(not board_control))
print("Control of board is given to {}".format("board" if board_control else "computer"))