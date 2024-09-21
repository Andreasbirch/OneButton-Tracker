import board
from analogio import AnalogIn

usb_voltage = AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

voltage_reading = get_voltage(usb_voltage)
print(voltage_reading > 3)