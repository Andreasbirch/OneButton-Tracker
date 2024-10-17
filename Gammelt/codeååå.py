import board
import time
from analogio import AnalogIn
import busio
import adafruit_ds3231

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
rtc = adafruit_ds3231.DS3231(i2c)

## Setup voltage reader
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

## Setup board write access
usb_voltage = AnalogIn(board.A1)
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
board_control = get_voltage(usb_voltage) < 2

if board_control:
    with open("/data.csv", "a+") as fp:
        mono_time = time.monotonic()

        #Measure battery as fast as possible
        battery = [] #Store battery in memory in order to avoid slow write times
        for i in range(0, 1000):
            battery.append((time.monotonic() - mono_time,
                            get_voltage(vbat_voltage),
                            get_voltage(usb_voltage)))
        
        for record in battery:
            fp.write('%d,%.5f,%.5f\n' % (record[0], record[1], record[2]))
            fp.flush


        #Measure battery 10 times per second
        battery = [] #Store battery in memory in order to avoid slow write times
        mono_time = time.monotonic()
        for i in range(0, 1000):
            battery.append((time.monotonic() - mono_time,
                            get_voltage(vbat_voltage),
                            get_voltage(usb_voltage)))
            time.sleep(0.1)
        
        for record in battery:
            fp.write('%d,%.5f,%.5f\n' % (record[0], record[1], record[2]))
            fp.flush


        #Measure battery once every second
        mono_time = time.monotonic()
        for i in range(0, 100):
            fp.write('%d,%.5f,%.5f\n' % 
                     (time.monotonic() - mono_time,
                     get_voltage(vbat_voltage),
                     get_voltage(usb_voltage)))
            time.sleep(1)


        #Measure battery once every 10 seconds
        mono_time = time.monotonic()
        for i in range(0, 100):
            fp.write('%d,%.5f,%.5f\n' % 
                     (time.monotonic() - mono_time,
                     get_voltage(vbat_voltage),
                     get_voltage(usb_voltage)))
            time.sleep(10)
else:
    print("Computer is in control")
    #Measure battery 10 times per second
    battery = [] #Store battery in memory in order to avoid slow write times
    mono_time = time.monotonic()
    for i in range(0, 100):
        battery.append((time.monotonic() - mono_time,
                        get_voltage(vbat_voltage),
                        get_voltage(usb_voltage)))
        time.sleep(0.1)
    
    for record in battery:
        print('%d,%.5f,%.5f\n' % (record[0], record[1], record[2]))