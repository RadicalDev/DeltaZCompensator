__author__ = 'jfindley'
import sys
sys.path.append("../lib")
from printer import OrionDelta


if __name__ == "__main__":
    printer = OrionDelta("/dev/ttyACM0", 115200)
    printer.connect()

    while True:
        command = raw_input("Gcode: ")
        printer.write(command.upper())