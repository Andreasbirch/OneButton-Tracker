import board
import alarm.time
import time
import digitalio
from analogio import AnalogIn
from logger import FileLogger, ConsoleLogger

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
usb_voltage = AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

logger = None

usb_voltage_rea = get_voltage(usb_voltage)
if get_voltage(usb_voltage) > 2:
    logger = ConsoleLogger()
else:
    logger = FileLogger("test.csv", headers=[
        "pre measurement"," post measurement"
    ])

sleep_time = 10 #seconds
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_time)

## Calculate an average battery voltage to ensure no spikes
def get_avg_voltage(pin, sample_size = 50):
    avg = 0
    for _ in range(sample_size):
        avg += get_voltage(pin)
    return avg / sample_size

for i in range(360):
    voltage_measurement = get_avg_voltage(vbat_voltage)

    logger.log([
        "{:f}".format(voltage_measurement)
    ])

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
while True:
    led.value = True