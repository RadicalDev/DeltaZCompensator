__author__ = 'jfindley'
import sys, os
sys.path.append(os.path.join("..", "lib"))
from generator import ZMapGenerator
from printer import *
from dial_indicator import *


if __name__ == "__main__":
    # Sample gcode
    gcode_dir = os.path.join("..", "gcode")
    gcode_in = os.path.join(gcode_dir, "test_kiss.gcode")
    gcode_out = os.path.join(gcode_dir, "test_kiss_zmapped.gcode")

    # CSV
    csv_dir = os.path.join("..", "csv")
    csv = os.path.join(csv_dir, "zmap_3mm.csv")

    # Printer capabilities
    speed_max_travel = 5000    # speed to go from home to zero
    speed_max_dot = 2000        # speed to go from point to point
    wait_time_home = 5          # time (seconds) to wait for all axes to home
    wait_time_xyz_zero = 10      # time (seconds) to wait for all axes to reach zero
    wait_time_point = 0.0         # time (seconds) to wait for printer to settle on point. If print head stutters, you're going too fast
    wait_time_row = 0.75           # time (seconds) to dwell on the end of a row
    z_height_row_change = 0    # how high to move print head before moving to start of next row

    # Build plate specification
    build_plate_radius = 60        # Orion build plate radius, Set to whatever it should be for yours

    # Calibration granularity
    point_spacing = 20          # size of point spacing in mm, less takes longer

    # COM Port, set to whatever RH uses.
    com_port = "/dev/ttyACM1"
    baud_rate = 115200

    com_port_di = "/dev/ttyACM0"
    baud_rate_di = 115200

    printer = OrionDelta(com_port, baud_rate)
    printer.connect()

    dial = HF93295(com_port_di, baud_rate_di)

    zm = ZMapGenerator(
        printer=printer,
        dial=dial,
        speed_max_travel=speed_max_travel,
        speed_max_dot=speed_max_dot,
        wait_time_home=wait_time_home,
        wait_time_xyz_zero=wait_time_xyz_zero,
        wait_time_point=wait_time_point,
        wait_time_row=wait_time_row,
        z_height_row_change=z_height_row_change,
        r=build_plate_radius,
        step_size=point_spacing,
        csv_file=csv,)

    zm.main(use_computed_offsets=True, recompute_offsets=True)
    zm.generate_buildplate_image()

    #zm.main(use_computed_offsets=True, recompute_offsets=True)
    #zm.generate_buildplate_image()