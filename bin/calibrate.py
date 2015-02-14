__author__ = 'jfindley'
import sys
import os
sys.path.append(os.path.join("..", "lib"))
from printer import Printer

if __name__ == "__main__":

    orion_towers = [
        (0, 0, 0),
        (-65, -35, 0),
        (-65, 35, 0),
        (0, 65, 0),
        (65, 35, 0),
        (65, -35, 0),
        (0, -65, 0),
        (0, 0, 0),
    ]

    port = "/dev/ttyACM0"
    rate = 115200
    p = Printer(port, rate)
    p.connect()
    p.write("G28")
    p.write("G1 X0 Y0 Z0")
    p.write("G4 S1")
    p.write("G1 X36 Y-35")
    p.write("G4 S1")
    for x, y, z in orion_towers:
        p.write("G1 X{0} Y{1} Z{2}".format(x, y, z))
        #p.write("G4 S1")
        #p.write("G1 Z{0}".format(z))
        p.write("G4 S5")
        #p.write("G1 Z25")
        #p.write("G4 S1")
    p.disconnect()
