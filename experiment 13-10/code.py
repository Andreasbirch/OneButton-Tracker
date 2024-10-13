import board
from time import sleep
from analogio import AnalogIn
from logger import FileLogger, ConsoleLogger

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

# logger = FileLogger("data.csv", ["Voltage"])
logger = ConsoleLogger()

## Calculate an average battery voltage to ensure no spikes
def get_avg_voltage(pin, sample_size = 50):
    avg = 0
    for _ in range(sample_size):
        avg += get_voltage(pin)
    return avg / sample_size

while True:
    sample_size = 10
    
    average_pre_measurement_voltage = 0
    average_post_measurement_voltage = 0

    ## Make n samples, and take the average battery consumption of that
    for i in range(sample_size):
        ## Get battery reading before measurement
        average_pre_measurement_voltage += get_avg_voltage(vbat_voltage)

        ## Take measurement

        ## Get battery reading after measurement
        average_post_measurement_voltage += get_avg_voltage(vbat_voltage)

    average_pre_measurement_voltage = average_pre_measurement_voltage / sample_size
    average_post_measurement_voltage = average_post_measurement_voltage / sample_size

    logger.log([
        "{:.2f}".format(average_pre_measurement_voltage),
        "{:.2f}".format(average_post_measurement_voltage),
        "{:.2f}".format(average_pre_measurement_voltage - average_post_measurement_voltage),
    ])
    sleep(1)