import board
import time
from os import stat
from analogio import AnalogIn

vbat = AnalogIn(board.A2)
file_path = "/test_bat.csv"

print(stat(file_path)[6])

with open(file_path, 'a+') as file:
    file.write('{}\n'.format(time.time()))

while True:
    if stat(file_path)[6] > 5_000_000:
        with open(file_path, 'a+') as file:
            file.write('\n{}'.format(time.time()))
        exit()

    measurements = []
    for i in range(200):
        measurements.append(str(vbat.value))
    with open(file_path, 'a+') as file:
        file.write('\n'.join(measurements))