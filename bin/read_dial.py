__author__ = 'jfindley'

import serial
s = serial.Serial("/dev/ttyACM1", 115200)


while True:
    data = s.readline().strip()

    if len(data) != 24:
        continue

    val = int(data[1:-3][::-1], 2)/100.0
    if data[-3] == '1':
        val = -val

    print val