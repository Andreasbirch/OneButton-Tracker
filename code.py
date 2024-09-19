import board
from analogio import AnalogIn

usb_voltage = AnalogIn(board.A0)

def get_voltage(pin):
    return (pin * 3.3) / 65536 * 2

voltage_reading = get_voltage(usb_voltage)
print(voltage_reading)