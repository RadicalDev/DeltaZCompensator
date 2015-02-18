__author__ = 'jfindley'
import sys
import os
sys.path.append(os.path.join("..", "lib"))
from printer import OrionDelta
from dial_indicator import HF93295

if __name__ == "__main__":
    x_max = 0
    x_min = -75
    y_max = 0
    y_min = -75


    printer = OrionDelta("/dev/ttyACM0", 115200)
    printer.connect()
    #
    # dial = HF93295("/dev/ttyACM1", 115200)
    #
    #
    # data = open("../csv/zmap_2mm_z0.csv", 'r').readlines()
    # zmap = [[float(i) for i in line.strip().split(",")] for line in data]
    # for x, y, z in zmap:
    #     if x <= x_max and x >= x_min and y <= y_max and y >= y_min:
    #         cmd = "G1 S1 X{0} Y{1} Z{2} F600".format(x, y, z)
    #         printer.write(cmd)
    #         #measurement = dial.read()
    #         measurement = 0
    #         print "{0}, {1} [{2}] -> {3}".format(x, y, z, measurement)
    printer.write("G1 S1 X0 Y0 Z0 F2500")
    printer.write("G4 S5")
    for i in range(1, 10):
        cmd = "G1 S1 X-75 Y0 Z0 F500"
        printer.write(cmd)
        cmd = "G1 S1 X75 Y0 Z0 F500"
        printer.write(cmd)